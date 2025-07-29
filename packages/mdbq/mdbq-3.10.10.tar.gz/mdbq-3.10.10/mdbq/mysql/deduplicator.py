# -*- coding:utf-8 -*-
import re
import time
from functools import wraps
import warnings
import pymysql
import os
from mdbq.log import mylogger
from typing import List, Dict, Optional, Any, Tuple
from dbutils.pooled_db import PooledDB
import threading
import concurrent.futures
from collections import defaultdict
import sys


warnings.filterwarnings('ignore')
logger = mylogger.MyLogger(
    name='deduplicator',
    logging_mode='both',
    log_level='info',
    log_file='deduplicator.log',
    log_format='json',
    max_log_size=50,
    backup_count=5,
    enable_async=False,  # 是否启用异步日志
    sample_rate=1,  # 采样DEBUG/INFO日志, 0.5表示50%的日志会被采样
    sensitive_fields=[],  #  敏感字段列表
)


class MySQLDeduplicator:
    """
    MySQL数据去重

    功能：
    1. 自动检测并删除MySQL数据库中的重复数据
    2. 支持全库扫描或指定表处理
    3. 支持多线程/多进程安全处理
    4. 完善的错误处理和日志记录

    使用示例：
    deduplicator = MySQLDeduplicator(
        username='root',
        password='password',
        host='localhost',
        port=3306
    )

    # 全库去重
    deduplicator.deduplicate_all()

    # 指定数据库去重(多线程)
    deduplicator.deduplicate_database('my_db', parallel=True)

    # 指定表去重(使用特定列)
    deduplicator.deduplicate_table('my_db', 'my_table', columns=['name', 'date'])

    # 关闭连接
    deduplicator.close()
    """

    def __init__(
            self,
            username: str,
            password: str,
            host: str = 'localhost',
            port: int = 3306,
            charset: str = 'utf8mb4',
            max_workers: int = 1,
            batch_size: int = 1000,
            skip_system_dbs: bool = True,
            max_retries: int = 3,
            retry_interval: int = 5,
            pool_size: int = 5,
            primary_key: str = 'id',
            date_range: Optional[List[str]] = None,
            recent_month: Optional[int] = None,
            date_column: str = '日期',
            exclude_columns: Optional[List[str]] = None
    ) -> None:
        """
        初始化去重处理器
        新增参数:
        :param date_range: 指定去重的日期区间 [start_date, end_date]，格式'YYYY-MM-DD'
        :param recent_month: 最近N个月的数据去重（与date_range互斥，优先生效）
        :param date_column: 时间列名，默认为'日期'
        :param exclude_columns: 去重时排除的列名列表，默认为['id', '更新时间']
        """
        # 连接池状态标志
        self._closed = False
        logger.debug('初始化MySQLDeduplicator', {
            'host': host, 'port': port, 'user': username, 'charset': charset,
            'max_workers': max_workers, 'batch_size': batch_size, 'pool_size': pool_size,
            'exclude_columns': exclude_columns
        })
        # 初始化连接池
        self.pool = PooledDB(
            creator=pymysql,
            host=host,
            port=port,
            user=username,
            password=password,
            charset=charset,
            maxconnections=pool_size,
            cursorclass=pymysql.cursors.DictCursor
        )

        # 配置参数
        self.max_workers = max(1, min(max_workers, 20))  # 限制最大线程数
        self.batch_size = batch_size
        self.skip_system_dbs = skip_system_dbs
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.primary_key = primary_key

        # 时间范围参数
        self.date_range = date_range
        self.recent_month = recent_month
        self.date_column = date_column
        self._dedup_start_date = None
        self._dedup_end_date = None
        # 不管 exclude_columns 是否传入, 'id' 一定会被排除
        default_exclude = {'id'}
        # exclude_columns 不传则排除: ['id', '更新时间']
        if not exclude_columns:
            self.exclude_columns = list(default_exclude | {'更新时间'})
        else:
            self.exclude_columns = list(set(exclude_columns) | default_exclude)
        # 解析时间范围
        if self.date_range and len(self.date_range) == 2:
            self._dedup_start_date, self._dedup_end_date = self.date_range
        elif self.recent_month:
            from datetime import datetime, timedelta
            today = datetime.today()
            month = today.month - self.recent_month
            year = today.year
            while month <= 0:
                month += 12
                year -= 1
            self._dedup_start_date = f"{year}-{month:02d}-01"
            self._dedup_end_date = today.strftime("%Y-%m-%d")

        # 线程安全控制
        self._lock = threading.Lock()
        self._processing_tables = set()  # 正在处理的表集合

        # 系统数据库列表
        self.SYSTEM_DATABASES = {'information_schema', 'mysql', 'performance_schema', 'sys'}

    def _get_connection(self) -> pymysql.connections.Connection:
        """从连接池获取连接"""
        if self._closed:
            logger.error('尝试获取连接但连接池已关闭')
            raise ConnectionError("连接池已关闭")
        try:
            conn = self.pool.connection()
            logger.debug("成功获取数据库连接")
            return conn
        except Exception as e:
            logger.error(f"获取数据库连接失败: {str(e)}", {'error_type': type(e).__name__})
            raise ConnectionError(f"连接数据库失败: {str(e)}")

    @staticmethod
    def _retry_on_failure(func: Any) -> Any:
        """重试装饰器"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            for attempt in range(self.max_retries + 1):
                try:
                    logger.debug(f'调用{func.__name__}，第{attempt+1}次尝试', {'args': args, 'kwargs': kwargs})
                    return func(self, *args, **kwargs)
                except (pymysql.OperationalError, pymysql.InterfaceError) as e:
                    last_exception = e
                    if attempt < self.max_retries:
                        wait_time = self.retry_interval * (attempt + 1)
                        logger.warning(
                            f"数据库操作失败，准备重试 (尝试 {attempt + 1}/{self.max_retries})",
                            {'error': str(e), 'wait_time': wait_time, 'func': func.__name__})
                        time.sleep(wait_time)
                        continue
                except Exception as e:
                    last_exception = e
                    logger.error(f"操作失败: {str(e)}", {'error_type': type(e).__name__, 'func': func.__name__})
                    break
            if last_exception:
                logger.error('重试后依然失败', {'func': func.__name__, 'last_exception': str(last_exception)})
                raise last_exception
            raise Exception("未知错误")
        return wrapper

    @_retry_on_failure
    def _get_databases(self) -> List[str]:
        """获取所有非系统数据库列表"""
        sql = "SHOW DATABASES"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                all_dbs = [row['Database'] for row in cursor.fetchall()]

                if self.skip_system_dbs:
                    return [db for db in all_dbs if db.lower() not in self.SYSTEM_DATABASES]
                return all_dbs

    @_retry_on_failure
    def _get_tables(self, database: str) -> List[str]:
        """获取指定数据库的所有表"""
        sql = "SHOW TABLES"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"USE `{database}`")
                cursor.execute(sql)
                return [row[f'Tables_in_{database}'] for row in cursor.fetchall()]

    @_retry_on_failure
    def _get_table_columns(self, database: str, table: str) -> List[str]:
        """获取表的列名(排除主键列)"""
        sql = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (database, table))
                return [row['COLUMN_NAME'] for row in cursor.fetchall()
                        if row['COLUMN_NAME'].lower() != self.primary_key.lower()]

    def _acquire_table_lock(self, database: str, table: str) -> bool:
        """获取表处理锁，防止并发处理同一张表"""
        key = f"{database}.{table}"

        with self._lock:
            if key in self._processing_tables:
                logger.debug(f"表 {key} 正在被其他线程处理，跳过")
                return False
            self._processing_tables.add(key)
            return True

    def _release_table_lock(self, database: str, table: str) -> None:
        """释放表处理锁"""
        key = f"{database}.{table}"

        with self._lock:
            if key in self._processing_tables:
                self._processing_tables.remove(key)

    def _deduplicate_table(
            self,
            database: str,
            table: str,
            columns: Optional[List[str]] = None,
            dry_run: bool = False
    ) -> Tuple[int, int]:
        """
        执行单表去重

        :param database: 数据库名
        :param table: 表名
        :param columns: 用于去重的列(为None时使用所有列)
        :param dry_run: 是否模拟运行(只统计不实际删除)
        :return: (重复行数, 删除行数)
        """
        if not self._acquire_table_lock(database, table):
            return (0, 0)
        temp_table = None
        try:
            # 获取原始数据总量
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    logger.debug('执行SQL', {'sql': f'SELECT COUNT(*) as cnt FROM `{database}`.`{table}`'})
                    cursor.execute(f"SELECT COUNT(*) as cnt FROM `{database}`.`{table}`")
                    total_count_row = cursor.fetchone()
                    total_count = total_count_row['cnt'] if total_count_row and 'cnt' in total_count_row else 0
            logger.info('执行', {"库": database, "表": table, "开始处理数据量": total_count, 'func': sys._getframe().f_code.co_name})
            # 获取实际列名
            all_columns = self._get_table_columns(database, table)
            logger.debug('获取表列', {'库': database, '表': table, 'all_columns': all_columns})
            # 检查是否需要按时间范围过滤
            use_time_filter = False
            time_col = self.date_column
            all_columns_lower = [col.lower() for col in all_columns]
            # 排除exclude_columns
            exclude_columns_lower = [col.lower() for col in getattr(self, 'exclude_columns', [])]
            # 统一列名小写做判断
            use_columns = columns or all_columns
            use_columns = [col for col in use_columns if col.lower() in all_columns_lower and col.lower() not in exclude_columns_lower]
            invalid_columns = set([col for col in (columns or []) if col.lower() not in all_columns_lower])
            if invalid_columns:
                logger.warning('不存在的列', {"库": database, "表": table, "不存在以下列": invalid_columns, 'func': sys._getframe().f_code.co_name})
            if not use_columns:
                logger.error('没有有效的去重列', {"库": database, "表": table})
                return (0, 0)
            # 统一用反引号包裹
            column_list = ', '.join([f'`{col}`' for col in use_columns])
            temp_table = f"temp_{table}_dedup_{os.getpid()}_{threading.get_ident()}"
            temp_table = re.sub(r'[^a-zA-Z0-9_]', '_', temp_table)[:60]
            pk = self.primary_key
            # 主键判断也用小写
            if pk.lower() not in all_columns_lower and pk != 'id':
                logger.error('', {"不存在主键列": database, "表": table, "主键列不存在": pk})
                return (0, 0)
            # 找到实际主键名
            pk_real = next((c for c in all_columns if c.lower() == pk.lower()), pk)
            # 构造where条件
            where_time = ''
            if use_time_filter:
                where_time = f"WHERE `{time_col}` >= '{self._dedup_start_date}' AND `{time_col}` <= '{self._dedup_end_date}'"
            create_temp_sql = f"""
            CREATE TABLE `{database}`.`{temp_table}` AS
            SELECT MIN(`{pk_real}`) as `min_id`, {column_list}, COUNT(*) as `dup_count`
            FROM `{database}`.`{table}`
            {where_time}
            GROUP BY {column_list}
            HAVING COUNT(*) > 1
            """
            drop_temp_sql = f"DROP TABLE IF EXISTS `{database}`.`{temp_table}`"
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    logger.debug('创建临时表SQL', {'sql': create_temp_sql})
                    cursor.execute(create_temp_sql)
                    logger.debug('统计临时表重复组SQL', {'sql': f'SELECT COUNT(*) as cnt FROM `{database}`.`{temp_table}`'})
                    cursor.execute(f"SELECT COUNT(*) as cnt FROM `{database}`.`{temp_table}`")
                    dup_count_row = cursor.fetchone()
                    dup_count = dup_count_row['cnt'] if dup_count_row and 'cnt' in dup_count_row else 0
                    if dup_count == 0:
                        logger.info('没有重复数据', {"库": database, "表": table, "数据量": total_count, "时间范围": [self._dedup_start_date, self._dedup_end_date] if use_time_filter else None, "实际去重列": use_columns})
                        logger.debug('删除临时表SQL', {'sql': drop_temp_sql})
                        cursor.execute(drop_temp_sql)
                        conn.commit()
                        return (0, 0)
                    affected_rows = 0
                    if not dry_run:
                        # 分批删除，避免锁表
                        while True:
                            delete_dup_sql = f"""
                            DELETE FROM `{database}`.`{table}`
                            WHERE `{pk_real}` NOT IN (
                                SELECT `min_id` FROM `{database}`.`{temp_table}`
                            ) {'AND' if use_time_filter else ''} {f'`{time_col}` >= \'{self._dedup_start_date}\' AND `{time_col}` <= \'{self._dedup_end_date}\'' if use_time_filter else ''}
                            AND ({' AND '.join([f'`{col}` IS NOT NULL' for col in use_columns])})
                            LIMIT {self.batch_size}
                            """
                            logger.debug('执行删除重复数据SQL', {'sql': delete_dup_sql})
                            cursor.execute(delete_dup_sql)
                            batch_deleted = cursor.rowcount
                            affected_rows += batch_deleted
                            conn.commit()
                            if batch_deleted < self.batch_size:
                                break
                        logger.info('操作删除', {"库": database, "表": table, "数据量": total_count, "重复组数": dup_count, "实际删除": affected_rows, "时间范围": [self._dedup_start_date, self._dedup_end_date] if use_time_filter else None, "实际去重列": use_columns})
                    else:
                        logger.debug('dry_run模式，不执行删除', {"库": database, "表": table, "重复组数": dup_count, "时间范围": [self._dedup_start_date, self._dedup_end_date] if use_time_filter else None})
                        affected_rows = 0
                    logger.debug('删除临时表SQL', {'sql': drop_temp_sql})
                    cursor.execute(drop_temp_sql)
                    conn.commit()
                    return (dup_count, affected_rows)
        except Exception as e:
            logger.error('异常', {"库": database, "表": table, "异常": str(e), 'func': sys._getframe().f_code.co_name, 'traceback': repr(e)})
            # 异常时也要清理临时表
            if temp_table:
                try:
                    with self._get_connection() as conn:
                        with conn.cursor() as cursor:
                            drop_temp_sql = f"DROP TABLE IF EXISTS `{database}`.`{temp_table}`"
                            cursor.execute(drop_temp_sql)
                            conn.commit()
                except Exception as drop_e:
                    logger.error('异常时清理临时表失败', {"库": database, "表": table, "异常": str(drop_e)})
            return (0, 0)
        finally:
            self._release_table_lock(database, table)

    def deduplicate_table(
            self,
            database: str,
            table: str,
            columns: Optional[List[str]] = None,
            dry_run: bool = False
    ) -> Tuple[int, int]:
        """
        对指定表进行去重

        :param database: 数据库名
        :param table: 表名
        :param columns: 用于去重的列(为None时使用所有列)
        :param dry_run: 是否模拟运行(只统计不实际删除)
        :return: (重复行数, 删除行数)
        """
        try:
            if not self._check_table_exists(database, table):
                logger.warning('表不存在', {"库": database, "表": table, "warning": "跳过"})
                return (0, 0)
            logger.info('单表开始', {"库": database, "表": table, "参数": {"指定去重列": columns, "模拟运行": dry_run, '排除列': self.exclude_columns}})
            result = self._deduplicate_table(database, table, columns, dry_run)
            logger.info('单表完成', {"库": database, "表": table, "结果[重复, 删除]": result})
            return result
        except Exception as e:
            logger.error('发生全局错误', {"库": database, "表": table, 'func': sys._getframe().f_code.co_name, "发生全局错误": str(e)})
            return (0, 0)

    def deduplicate_database(
            self,
            database: str,
            tables: Optional[List[str]] = None,
            columns_map: Optional[Dict[str, List[str]]] = None,
            dry_run: bool = False,
            parallel: bool = False
    ) -> Dict[str, Tuple[int, int]]:
        """
        对指定数据库的所有表进行去重

        :param database: 数据库名
        :param tables: 要处理的表列表(为None时处理所有表)
        :param columns_map: 各表使用的去重列 {表名: [列名]}
        :param dry_run: 是否模拟运行
        :param parallel: 是否并行处理
        :return: 字典 {表名: (重复行数, 删除行数)}
        """
        results = {}
        try:
            if not self._check_database_exists(database):
                logger.warning('数据库不存在', {"库": database})
                return results
            target_tables = tables or self._get_tables(database)
            logger.debug('获取目标表', {'库': database, 'tables': target_tables})
            if not target_tables:
                logger.info('数据库中没有表', {"库": database, "操作": "跳过"})
                return results
            logger.info('库统计', {"库": database, "表数量": len(target_tables), "表列表": target_tables})
            if parallel and self.max_workers > 1:
                logger.debug('并行处理表', {'库': database, 'max_workers': self.max_workers})
                # 使用线程池并行处理
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=self.max_workers
                ) as executor:
                    futures = {}
                    for table in target_tables:
                        columns = columns_map.get(table) if columns_map else None
                        logger.debug('提交表去重任务', {'库': database, '表': table, 'columns': columns})
                        futures[executor.submit(
                            self.deduplicate_table,
                            database, table, columns, dry_run
                        )] = table
                    for future in concurrent.futures.as_completed(futures):
                        table = futures[future]
                        try:
                            dup_count, affected_rows = future.result()
                            results[table] = (dup_count, affected_rows)
                        except Exception as e:
                            logger.error('异常', {"库": database, "表": table, "error": str(e), 'traceback': repr(e)})
                            results[table] = (0, 0)
            else:
                logger.debug('串行处理表', {'库': database})
                # 串行处理
                for table in target_tables:
                    columns = columns_map.get(table) if columns_map else None
                    dup_count, affected_rows = self.deduplicate_table(
                        database, table, columns, dry_run
                    )
                    results[table] = (dup_count, affected_rows)
            total_dup = sum(r[0] for r in results.values())
            total_del = sum(r[1] for r in results.values())
            logger.info('单库完成', {"库": database, "重复组数": total_dup, "总删除行数": total_del, "详细结果": results})
            return results
        except Exception as e:
            logger.error('发生全局错误', {"库": database, 'func': sys._getframe().f_code.co_name, "error": str(e), 'traceback': repr(e)})
            return results

    def deduplicate_all(
            self,
            databases: Optional[List[str]] = None,
            tables_map: Optional[Dict[str, List[str]]] = None,
            columns_map: Optional[Dict[str, Dict[str, List[str]]]] = None,
            dry_run: bool = False,
            parallel: bool = False
    ) -> Dict[str, Dict[str, Tuple[int, int]]]:
        """
        对所有数据库进行去重

        :param databases: 要处理的数据库列表(为None时处理所有非系统数据库)
        :param tables_map: 各数据库要处理的表 {数据库名: [表名]}
        :param columns_map: 各表使用的去重列 {数据库名: {表名: [列名]}}
        :param dry_run: 是否模拟运行
        :param parallel: 是否并行处理
        :return: 嵌套字典 {数据库名: {表名: (重复行数, 删除行数)}}
        """
        all_results = defaultdict(dict)
        try:
            target_dbs = databases or self._get_databases()
            logger.debug('获取目标数据库', {'databases': target_dbs})
            if not target_dbs:
                logger.warning('没有可处理的数据库')
                return all_results
            logger.info('全局开始', {"数据库数量": len(target_dbs), "数据库列表": target_dbs, "参数": {"模拟运行": dry_run, "并行处理": parallel, '排除列': self.exclude_columns}})
            if parallel and self.max_workers > 1:
                # 使用线程池并行处理多个数据库
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=self.max_workers
                ) as executor:
                    futures = {}
                    for db in target_dbs:
                        tables = tables_map.get(db) if tables_map else None
                        db_columns_map = columns_map.get(db) if columns_map else None
                        futures[executor.submit(
                            self.deduplicate_database,
                            db, tables, db_columns_map, dry_run, False
                        )] = db
                    for future in concurrent.futures.as_completed(futures):
                        db = futures[future]
                        try:
                            db_results = future.result()
                            all_results[db] = db_results
                        except Exception as e:
                            logger.error('异常', {"库": db, "error": str(e), 'traceback': repr(e)})
                            all_results[db] = {}
            else:
                # 串行处理数据库
                for db in target_dbs:
                    tables = tables_map.get(db) if tables_map else None
                    db_columns_map = columns_map.get(db) if columns_map else None
                    db_results = self.deduplicate_database(
                        db, tables, db_columns_map, dry_run, parallel
                    )
                    all_results[db] = db_results
            total_dup = sum(
                r[0] for db in all_results.values()
                for r in db.values()
            )
            total_del = sum(
                r[1] for db in all_results.values()
                for r in db.values()
            )
            logger.info('全局完成', {"总重复组数": total_dup, "总删除行数": total_del, "详细结果": dict(all_results)})
            return all_results
        except Exception as e:
            logger.error('异常', {"error": str(e), 'traceback': repr(e)})
            return all_results

    @_retry_on_failure
    def _check_database_exists(self, database: str) -> bool:
        """检查数据库是否存在"""
        sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (database,))
                return bool(cursor.fetchone())

    @_retry_on_failure
    def _check_table_exists(self, database: str, table: str) -> bool:
        """检查表是否存在"""
        sql = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        """

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (database, table))
                return bool(cursor.fetchone())

    def close(self) -> None:
        """关闭连接池"""
        try:
            if hasattr(self, 'pool') and self.pool and not self._closed:
                self.pool.close()
                self._closed = True
                logger.info("数据库连接池已关闭")
            else:
                logger.info('连接池已关闭或不存在')
        except Exception as e:
            logger.error(f"关闭连接池时出错", {'error_type': type(e).__name__, 'error': str(e)})

    def __enter__(self) -> 'MySQLDeduplicator':
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        self.close()


def main():
    deduplicator = MySQLDeduplicator(
        username='root',
        password='pwd',
        host='localhost',
        port=3306
    )

    # 全库去重(单线程)
    deduplicator.deduplicate_all(dry_run=False, parallel=False)

    # # 指定数据库去重(多线程)
    # logger.info('调用deduplicate_database')
    # deduplicator.deduplicate_database('my_db', dry_run=False, parallel=True)

    # # 指定表去重(使用特定列)
    # deduplicator.deduplicate_table('my_db', 'my_table', columns=['name', 'date'], dry_run=False)

    # 关闭连接
    deduplicator.close()

if __name__ == '__main__':
    # main()
    pass
