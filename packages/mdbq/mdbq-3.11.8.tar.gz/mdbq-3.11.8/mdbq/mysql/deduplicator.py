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
from datetime import datetime
import uuid


warnings.filterwarnings('ignore')
logger = mylogger.MyLogger(
    name='deduplicator',
    logging_mode='file',
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
            exclude_columns: Optional[List[str]] = None,
            exclude_databases: Optional[List[str]] = None,
            exclude_tables: Optional[Dict[str, List[str]]] = None,
            duplicate_keep_mode: str = 'keep_one'
    ) -> None:
        """
        初始化去重处理器
        :param date_range: 指定去重的日期区间 [start_date, end_date]，格式'YYYY-MM-DD'
        :param recent_month: 最近N个月的数据去重（与date_range互斥，优先生效）
        :param date_column: 时间列名，默认为'日期'
        :param exclude_columns: 去重时排除的列名列表，默认为['id', '更新时间']
        :param exclude_databases: 排除的数据库名列表
        :param exclude_tables: 排除的表名字典 {数据库名: [表名, ...]}
        :param duplicate_keep_mode: 'keep_one'（默认，重复组保留一条），'remove_all'（全部删除重复组）
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
        # 解析时间范围并智能校正date_range
        if self.date_range and len(self.date_range) == 2:
            try:
                start, end = self.date_range
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                if start_dt > end_dt:
                    logger.warning(
                        "date_range顺序不正确，自动交换开始和结束日期。",
                        {"start": start, "end": end}
                    )
                    start_dt, end_dt = end_dt, start_dt
                self._dedup_start_date = start_dt.strftime("%Y-%m-%d")
                self._dedup_end_date = end_dt.strftime("%Y-%m-%d")
            except Exception as e:
                logger.error(
                    "date_range参数格式错误，应为['YYYY-MM-DD', 'YYYY-MM-DD']，已忽略时间范围。",
                    {"date_range": self.date_range, "error": str(e)}
                )
                self._dedup_start_date = None
                self._dedup_end_date = None
        elif self.recent_month:
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

        # 排除数据库和表的逻辑
        self.exclude_databases = set([db.lower() for db in exclude_databases]) if exclude_databases else set()
        self.exclude_tables = {k.lower(): set([t.lower() for t in v]) for k, v in (exclude_tables or {}).items()}

        self.duplicate_keep_mode = duplicate_keep_mode if duplicate_keep_mode in ('keep_one', 'remove_all') else 'keep_one'

    def _get_connection(self) -> pymysql.connections.Connection:
        """
        从连接池获取一个数据库连接。
        
        Returns:
            pymysql.connections.Connection: 数据库连接对象。
        Raises:
            ConnectionError: 如果连接池已关闭或获取连接失败。
        """
        if self._closed:
            logger.error('尝试获取连接但连接池已关闭')
            raise ConnectionError("连接池已关闭")
        try:
            conn = self.pool.connection()
            return conn
        except Exception as e:
            logger.error(f"获取数据库连接失败: {str(e)}", {'error_type': type(e).__name__})
            raise ConnectionError(f"连接数据库失败: {str(e)}")

    @staticmethod
    def _retry_on_failure(func: Any) -> Any:
        """
        装饰器：为数据库操作方法提供自动重试机制。
        仅捕获pymysql的连接相关异常，重试指定次数后抛出最后一次异常。
        
        Args:
            func (Any): 被装饰的函数。
        Returns:
            Any: 被装饰函数的返回值。
        Raises:
            Exception: 多次重试后依然失败时抛出。
        """
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
        """
        获取所有非系统数据库列表，排除exclude_databases。
        
        Returns:
            List[str]: 数据库名列表。
        """
        sql = "SHOW DATABASES"
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                all_dbs = [row['Database'] for row in cursor.fetchall()]
                # 排除系统库和用户指定的库
                filtered = [db for db in all_dbs if db.lower() not in self.SYSTEM_DATABASES and db.lower() not in self.exclude_databases] if self.skip_system_dbs else [db for db in all_dbs if db.lower() not in self.exclude_databases]
                return filtered

    @_retry_on_failure
    def _get_tables(self, database: str) -> List[str]:
        """
        获取指定数据库的所有表名。
        
        Args:
            database (str): 数据库名。
        Returns:
            List[str]: 表名列表。
        """
        sql = "SHOW TABLES"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"USE `{database}`")
                cursor.execute(sql)
                return [row[f'Tables_in_{database}'] for row in cursor.fetchall()]

    @_retry_on_failure
    def _get_table_columns(self, database: str, table: str) -> List[str]:
        """
        获取指定表的所有列名（排除主键列）。
        
        Args:
            database (str): 数据库名。
            table (str): 表名。
        Returns:
            List[str]: 列名列表。
        """
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
        """
        获取表处理锁，防止并发处理同一张表。
        
        Args:
            database (str): 数据库名。
            table (str): 表名。
        Returns:
            bool: 是否成功获取锁。
        """
        key = f"{database}.{table}"

        with self._lock:
            if key in self._processing_tables:
                logger.debug(f"表 {key} 正在被其他线程处理，跳过")
                return False
            self._processing_tables.add(key)
            return True

    def _release_table_lock(self, database: str, table: str) -> None:
        """
        释放表处理锁。
        
        Args:
            database (str): 数据库名。
            table (str): 表名。
        """
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
        执行单表去重。
        
        Args:
            database (str): 数据库名。
            table (str): 表名。
            columns (Optional[List[str]]): 用于去重的列名列表（为None时使用所有列）。
            dry_run (bool): 是否为模拟运行（只统计不实际删除）。
        Returns:
            Tuple[int, int]: (重复组数, 实际删除行数)。
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
            temp_table = self._make_safe_table_name(table, prefix=f"temp_", suffix=f"_dedup_{os.getpid()}_{threading.get_ident()}")
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
                            if self.duplicate_keep_mode == 'remove_all':
                                # 删除所有重复组的所有记录
                                delete_dup_sql = f"""
                                DELETE FROM `{database}`.`{table}`
                                WHERE ({', '.join([f'`{col}`' for col in use_columns])}) IN (
                                    SELECT {column_list} FROM `{database}`.`{temp_table}`
                                ) {'AND' if use_time_filter else ''} {f'`{time_col}` >= \'{self._dedup_start_date}\' AND `{time_col}` <= \'{self._dedup_end_date}\'' if use_time_filter else ''}
                                LIMIT {self.batch_size}
                                """
                            else:
                                # 修正：只删除重复组中不是min_id的行，唯一数据不动
                                delete_dup_sql = f"""
                                DELETE FROM `{database}`.`{table}` t
                                WHERE EXISTS (
                                    SELECT 1 FROM `{database}`.`{temp_table}` tmp
                                    WHERE
                                        {' AND '.join([f't.`{col}` <=> tmp.`{col}`' for col in use_columns])}
                                        AND t.`{pk_real}` <> tmp.`min_id`
                                )
                                {'AND' if use_time_filter else ''} {f't.`{time_col}` >= \'{self._dedup_start_date}\' AND t.`{time_col}` <= \'{self._dedup_end_date}\'' if use_time_filter else ''}
                                LIMIT {self.batch_size}
                                """
                            logger.debug('执行删除重复数据SQL', {'sql': delete_dup_sql})
                            cursor.execute(delete_dup_sql)
                            batch_deleted = cursor.rowcount
                            affected_rows += batch_deleted
                            conn.commit()
                            if batch_deleted < self.batch_size:
                                break
                        logger.info('操作删除', {"库": database, "表": table, "数据量": total_count, "重复组数": dup_count, "实际删除": affected_rows, "时间范围": [self._dedup_start_date, self._dedup_end_date] if use_time_filter else None, "实际去重列": use_columns, "去重模式": self.duplicate_keep_mode})
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
        对指定表进行去重。
        
        Args:
            database (str): 数据库名。
            table (str): 表名。
            columns (Optional[List[str]]): 用于去重的列名列表（为None时使用所有列）。
            dry_run (bool): 是否为模拟运行（只统计不实际删除）。
        Returns:
            Tuple[int, int]: (重复组数, 实际删除行数)。
        """
        if database.lower() in self.exclude_tables and table.lower() in self.exclude_tables[database.lower()]:
            logger.info('表被排除', {"库": database, "表": table, "操作": "跳过"})
            return (0, 0)
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
        对指定数据库的所有表进行去重。
        
        Args:
            database (str): 数据库名。
            tables (Optional[List[str]]): 要处理的表列表（为None时处理所有表）。
            columns_map (Optional[Dict[str, List[str]]]): 各表使用的去重列 {表名: [列名]}。
            dry_run (bool): 是否为模拟运行。
            parallel (bool): 是否并行处理。
        Returns:
            Dict[str, Tuple[int, int]]: {表名: (重复组数, 实际删除行数)}。
        """
        results = {}
        try:
            if not self._check_database_exists(database):
                logger.warning('数据库不存在', {"库": database})
                return results
            target_tables = tables or self._get_tables(database)
            exclude_tbls = self.exclude_tables.get(database.lower(), set())
            target_tables = [t for t in target_tables if t.lower() not in exclude_tbls]
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
        对所有数据库进行去重。
        
        Args:
            databases (Optional[List[str]]): 要处理的数据库列表。如果为 None，则处理所有非系统数据库。
            tables_map (Optional[Dict[str, List[str]]]): 指定每个数据库要处理的表，格式为 {数据库名: [表名, ...]}。如果为 None，则处理所有表。
            columns_map (Optional[Dict[str, Dict[str, List[str]]]]): 指定每个表去重时使用的列，格式为 {数据库名: {表名: [列名, ...]}}。如果为 None，则使用所有列。
            dry_run (bool): 是否为模拟运行模式。为 True 时只统计重复行数，不实际删除。
            parallel (bool): 是否并行处理多个数据库。为 True 时使用线程池并发处理。
        Returns:
            Dict[str, Dict[str, Tuple[int, int]]]: 嵌套字典，格式为 {数据库名: {表名: (重复组数, 实际删除行数)}}。
        """
        all_results: Dict[str, Dict[str, Tuple[int, int]]] = defaultdict(dict)
        try:
            target_dbs: List[str] = databases or self._get_databases()
            target_dbs = [db for db in target_dbs if db.lower() not in self.exclude_databases]
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
                    futures: Dict[concurrent.futures.Future, str] = {}
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
        """
        检查数据库是否存在。
        
        Args:
            database (str): 数据库名。
        Returns:
            bool: 数据库是否存在。
        """
        sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (database,))
                return bool(cursor.fetchone())

    @_retry_on_failure
    def _check_table_exists(self, database: str, table: str) -> bool:
        """
        检查表是否存在。
        
        Args:
            database (str): 数据库名。
            table (str): 表名。
        Returns:
            bool: 表是否存在。
        """
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
        """
        关闭连接池。
        
        Returns:
            None
        """
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
        """
        上下文管理器进入方法。
        
        Returns:
            MySQLDeduplicator: 实例自身。
        """
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """
        上下文管理器退出方法，自动关闭连接池。
        
        Args:
            exc_type (Optional[type]): 异常类型。
            exc_val (Optional[BaseException]): 异常值。
            exc_tb (Optional[Any]): 异常追踪。
        Returns:
            None
        """
        self.close()

    def reorder_id_column(
        self,
        database: str,
        table: Optional[str] = None,
        id_column: str = "id",
        dry_run: bool = False,
        auto_drop_backup: bool = True
    ) -> Any:
        """
        安全重排指定表或指定库下所有表的id列为顺序自增（1,2,3...）。
        Args:
            database (str): 数据库名
            table (Optional[str]): 表名，None时批量处理该库所有表
            id_column (str): id列名，默认"id"
            dry_run (bool): 是否为模拟运行
            auto_drop_backup (bool): 校验通过后自动删除备份表
        Returns:
            bool 或 dict: 单表时bool，批量时{表名: bool}
        """
        if not table:
            # 批量模式，对库下所有表执行
            try:
                all_tables = self._get_tables(database)
            except Exception as e:
                logger.error('获取库下所有表失败', {"库": database, "异常": str(e)})
                return {}
            results = {}
            for tbl in all_tables:
                try:
                    res = self.reorder_id_column(database, tbl, id_column, dry_run, auto_drop_backup)
                    results[tbl] = res
                except Exception as e:
                    logger.error('批量id重排异常', {"库": database, "表": tbl, "异常": str(e)})
                    results[tbl] = False
            logger.info('批量id重排完成', {"库": database, "结果": results})
            return results
        # 单表模式
        table_quoted = f"`{database}`.`{table}`"
        if not self._acquire_table_lock(database, table):
            logger.warning('表级锁获取失败，跳过id重排', {"库": database, "表": table})
            return False
        try:
            # 检查表是否存在
            if not self._check_table_exists(database, table):
                logger.warning('表不存在，跳过id重排', {"库": database, "表": table})
                return False
            # 检查id列是否存在
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT COLUMN_NAME, COLUMN_KEY
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
                    """, (database, table))
                    columns_info = cursor.fetchall()
                    columns = [row['COLUMN_NAME'] for row in columns_info]
                    id_is_pk = any(row['COLUMN_NAME'].lower() == id_column.lower() and row['COLUMN_KEY'] in ('PRI', 'UNI') for row in columns_info)
            if id_column not in columns:
                logger.warning('表无id列，跳过id重排', {"库": database, "表": table})
                return False
            # 检查主键是否为单列id
            pk_cols = [row['COLUMN_NAME'] for row in columns_info if row['COLUMN_KEY'] == 'PRI']
            if len(pk_cols) != 1 or pk_cols[0].lower() != id_column.lower():
                logger.warning('主键不是单列id，跳过id重排', {"库": database, "表": table, "主键列": pk_cols})
                return False
            # 检查外键约束
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND REFERENCED_TABLE_NAME IS NOT NULL
                    """, (database, table))
                    if cursor.fetchone():
                        logger.warning('表存在外键约束，跳过id重排', {"库": database, "表": table})
                        return False
            # 获取表结构
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SHOW CREATE TABLE {table_quoted}")
                    create_table_sql = cursor.fetchone()['Create Table']
            logger.info('开始id重排', {"库": database, "表": table, "重排列": id_column, "dry_run": dry_run, "DDL警告": "MySQL DDL操作不可回滚，建议提前备份！"})
            if dry_run:
                logger.info('dry_run模式，打印原表结构', {"库": database, "表": table, "建表语句": create_table_sql})
                return True
            temp_table = self._make_safe_table_name(table, prefix=f"temp_", suffix=f"_reorderid_{os.getpid()}_{threading.get_ident()}")
            temp_table_quoted = f"`{database}`.`{temp_table}`"
            backup_table = self._make_safe_table_name(table, prefix="backup_", suffix=f"_{int(time.time())}_{uuid.uuid4().hex[:8]}")
            backup_table_quoted = f"`{database}`.`{backup_table}`"
            try:
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        # 1. 创建临时表，结构同原表
                        try:
                            cursor.execute(f"CREATE TABLE {temp_table_quoted} LIKE {table_quoted}")
                        except Exception as e:
                            logger.error('创建临时表失败', {"库": database, "表": table, "异常": str(e)})
                            return False
                        # 2. 插入数据，id列用ROW_NUMBER重排（MySQL 8+）
                        all_cols = ','.join([f'`{col}`' for col in columns])
                        all_cols_noid = ','.join([f'`{col}`' for col in columns if col != id_column])
                        insert_sql = f"""
                            INSERT INTO {temp_table_quoted} ({all_cols})
                            SELECT ROW_NUMBER() OVER (ORDER BY `{id_column}` ASC) as `{id_column}`, {all_cols_noid}
                            FROM {table_quoted}
                        """
                        try:
                            cursor.execute(insert_sql)
                        except Exception as e:
                            logger.error('插入重排数据失败', {"库": database, "表": table, "异常": str(e)})
                            try:
                                cursor.execute(f"DROP TABLE IF EXISTS {temp_table_quoted}")
                            except Exception as drop_e:
                                logger.error('插入失败后删除临时表失败', {"库": database, "表": table, "异常": str(drop_e)})
                            return False
                        # 如果id不是主键，尝试加主键（如不冲突）
                        if not id_is_pk:
                            try:
                                cursor.execute(f"ALTER TABLE {temp_table_quoted} ADD PRIMARY KEY(`{id_column}`)")
                            except Exception as e:
                                logger.warning('id列加主键失败，可能已存在其他主键', {"库": database, "表": table, "异常": str(e)})
                        # 3. 原表重命名为备份，临时表重命名为正式表
                        try:
                            cursor.execute(f"RENAME TABLE {table_quoted} TO {backup_table_quoted}, {temp_table_quoted} TO {table_quoted}")
                        except Exception as e:
                            logger.error('RENAME TABLE失败', {"库": database, "表": table, "异常": str(e)})
                            # 回滚：删除临时表
                            try:
                                cursor.execute(f"DROP TABLE IF EXISTS {temp_table_quoted}")
                            except Exception as drop_e:
                                logger.error('RENAME失败后删除临时表失败', {"库": database, "表": table, "异常": str(drop_e)})
                            return False
                        # 4. 校验新表和备份表数据量一致
                        try:
                            cursor.execute(f"SELECT COUNT(*) as cnt FROM {table_quoted}")
                            new_cnt = cursor.fetchone()['cnt']
                            cursor.execute(f"SELECT COUNT(*) as cnt FROM {backup_table_quoted}")
                            old_cnt = cursor.fetchone()['cnt']
                        except Exception as e:
                            logger.error('校验数据量失败', {"库": database, "表": table, "异常": str(e)})
                            return False
                        if new_cnt != old_cnt:
                            logger.error('id重排后数据量不一致，自动回滚', {"库": database, "表": table, "新表": new_cnt, "备份表": old_cnt})
                            # 回滚：恢复原表
                            try:
                                cursor.execute(f"DROP TABLE {table_quoted}")
                                cursor.execute(f"RENAME TABLE {backup_table_quoted} TO {table_quoted}")
                            except Exception as e:
                                logger.error('回滚恢复原表失败', {"库": database, "表": table, "异常": str(e)})
                            return False
                        logger.info('id重排成功且数据量一致', {"库": database, "表": table, "新表": new_cnt, "备份表": old_cnt, "备份表名": backup_table})
                        # 5. 可选：自动删除备份表
                        if auto_drop_backup:
                            try:
                                cursor.execute(f"DROP TABLE {backup_table_quoted}")
                                logger.info('已自动删除备份表', {"库": database, "表": table, "备份表名": backup_table})
                            except Exception as e:
                                logger.error('自动删除备份表失败', {"库": database, "表": table, "异常": str(e)})
                        return True
            except Exception as e:
                logger.error('id重排异常，准备回滚', {"库": database, "表": table, "异常": str(e)})
                # 回滚：如临时表存在则删掉，恢复原表结构
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(f"DROP TABLE IF EXISTS {temp_table_quoted}")
                        except Exception as drop_e:
                            logger.error('回滚时删除临时表失败', {"库": database, "表": table, "异常": str(drop_e)})
                        # 恢复原表（如备份表存在）
                        try:
                            with self._get_connection() as conn2:
                                with conn2.cursor() as cursor2:
                                    if self._check_table_exists(database, backup_table):
                                        cursor2.execute(f"DROP TABLE IF EXISTS {table_quoted}")
                                        cursor2.execute(f"RENAME TABLE {backup_table_quoted} TO {table_quoted}")
                                        logger.info('已自动恢复原表', {"库": database, "表": table, "备份表名": backup_table})
                        except Exception as recover_e:
                            logger.error('回滚时恢复原表失败', {"库": database, "表": table, "异常": str(recover_e)})
                return False
        finally:
            self._release_table_lock(database, table)

    @staticmethod
    def _make_safe_table_name(base: str, prefix: str = '', suffix: str = '', max_length: int = 64) -> str:
        """
        生成安全的MySQL表名，确保总长度不超过max_length字节。
        :param base: 原始表名
        :param prefix: 前缀
        :param suffix: 后缀
        :param max_length: 最大长度，默认64
        :return: 安全表名
        """
        # 只允许字母数字下划线
        base = re.sub(r'[^a-zA-Z0-9_]', '_', base)
        prefix = re.sub(r'[^a-zA-Z0-9_]', '_', prefix)
        suffix = re.sub(r'[^a-zA-Z0-9_]', '_', suffix)
        remain = max_length - len(prefix) - len(suffix)
        if remain < 1:
            # 前后缀太长，直接截断
            return (prefix + suffix)[:max_length]
        return f"{prefix}{base[:remain]}{suffix}"[:max_length]


def main():
    deduplicator = MySQLDeduplicator(
        username='root',
        password='pwd',
        host='localhost',
        port=3306
    )

    # 全库去重(单线程)
    deduplicator.deduplicate_all(dry_run=False, parallel=True)

    # # 指定数据库去重(多线程)
    # deduplicator.deduplicate_database('my_db', dry_run=False, parallel=False)

    # # 指定表去重(使用特定列)
    # deduplicator.deduplicate_table('my_db', 'my_table', columns=['name', 'date'], dry_run=False)

    # # 重排id列
    # deduplicator.reorder_id_column('my_db', 'my_table', 'id', dry_run=False, auto_drop_backup=True)

    # 关闭连接
    deduplicator.close()

if __name__ == '__main__':
    main()
    pass
