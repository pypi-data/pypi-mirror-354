# -*- coding:utf-8 -*-
import datetime
import re
import time
from functools import wraps
import warnings
import pymysql
import pandas as pd
from mdbq.log import mylogger
from typing import Union, List, Dict, Optional, Any, Tuple, Set
from dbutils.pooled_db import PooledDB
import json
from collections import OrderedDict
import sys

warnings.filterwarnings('ignore')
logger = mylogger.MyLogger(
    name='uploader',
    logging_mode='file',
    log_level='info',
    log_file='uploader.log',
    log_format='json',
    max_log_size=50,
    backup_count=5,
    enable_async=False,  # 是否启用异步日志
    sample_rate=1,  # 采样50%的DEBUG/INFO日志
    sensitive_fields=[],  #  敏感字段列表
)


def count_decimal_places(num_str):
    """
    计算数字字符串的小数位数，支持科学计数法

    :param num_str: 数字字符串
    :return: 返回元组(整数位数, 小数位数)
    :raises: 无显式抛出异常，但正则匹配失败时返回(0, 0)
    """
    match = re.match(r'^[-+]?\d+(\.\d+)?([eE][-+]?\d+)?$', str(num_str))
    if match:
        # 如果是科学计数法
        match = re.findall(r'(\d+)\.(\d+)[eE][-+]?(\d+)$', str(num_str))
        if match:
            if len(match[0]) == 3:
                if int(match[0][2]) < len(match[0][1]):
                    # count_int 清除整数部分开头的 0 并计算整数位数
                    count_int = len(re.sub('^0+', '', str(match[0][0]))) + int(match[0][2])
                    # 计算小数位数
                    count_float = len(match[0][1]) - int(match[0][2])
                    return count_int, count_float
        # 如果是普通小数
        match = re.findall(r'(\d+)\.(\d+)$', str(num_str))
        if match:
            count_int = len(re.sub('^0+', '', str(match[0][0])))
            count_float = len(match[0][1])
            return count_int, count_float  # 计算小数位数
    return 0, 0


class StatementCache(OrderedDict):
    """
    基于OrderedDict实现的LRU缓存策略，用于缓存SQL语句
    
    这个类继承自OrderedDict，实现了最近最少使用(LRU)的缓存策略。
    当缓存达到最大容量时，会自动删除最早添加的项。
    """
    def __init__(self, maxsize=100):
        """
        初始化缓存

        :param maxsize: 最大缓存大小，默认为100条SQL语句
        """
        super().__init__()
        self.maxsize = maxsize

    def __setitem__(self, key, value):
        """
        重写设置项方法，实现LRU策略

        :param key: 缓存键
        :param value: 缓存值
        """
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            self.popitem(last=False)


class MySQLUploader:
    """
    MySQL数据上传工具类
    
    提供了一系列方法用于将数据上传到MySQL数据库，支持自动建表、分表、数据验证等功能。
    使用连接池管理数据库连接，提供错误重试机制。
    """
    def __init__(
            self,
            username: str,
            password: str,
            host: str = 'localhost',
            port: int = 3306,
            charset: str = 'utf8mb4',
            collation: str = 'utf8mb4_0900_ai_ci',
            max_retries: int = 10,
            retry_interval: int = 10,
            pool_size: int = 5,
            connect_timeout: int = 10,
            read_timeout: int = 30,
            write_timeout: int = 30,
            ssl: Optional[Dict] = None
    ):
        """
        初始化MySQL上传器

        :param username: 数据库用户名
        :param password: 数据库密码
        :param host: 数据库主机地址，默认为localhost
        :param port: 数据库端口，默认为3306
        :param charset: 字符集，默认为utf8mb4
        :param collation: 排序规则，默认为utf8mb4_0900_ai_ci，对大小写不敏感，utf8mb4_0900_as_cs/utf8mb4_bin: 对大小写敏感
        :param max_retries: 最大重试次数，默认为10
        :param retry_interval: 重试间隔(秒)，默认为10
        :param pool_size: 连接池大小，默认为5
        :param connect_timeout: 连接超时(秒)，默认为10
        :param read_timeout: 读取超时(秒)，默认为30
        :param write_timeout: 写入超时(秒)，默认为30
        :param ssl: SSL配置字典，默认为None
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.charset = charset
        self.collation = collation
        self.max_retries = max(max_retries, 1)
        self.retry_interval = max(retry_interval, 1)
        self.pool_size = max(pool_size, 1)
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.write_timeout = write_timeout
        self.base_excute_col = ['id', '更新时间']  # 排重插入数据时始终排除该列
        self.case_sensitive = False  # 是否保持大小写敏感，默认为False(转为小写)
        self.ssl = ssl
        self._prepared_statements = StatementCache(maxsize=100)
        self._max_cached_statements = 100  # 用于控制 StatementCache 类中缓存的 SQL 语句数量，最多缓存 100 条 SQL 语句
        self._table_metadata_cache = {}
        self.metadata_cache_ttl = 300  # 5分钟缓存时间

        # 创建连接池
        self.pool = self._create_connection_pool()

    def _create_connection_pool(self) -> PooledDB:
        """
        创建数据库连接池

        :return: PooledDB连接池实例
        :raises ConnectionError: 当连接池创建失败时抛出
        """
        if hasattr(self, 'pool') and self.pool is not None and self._check_pool_health():
            return self.pool
        self.pool = None
        pool_params = {
            'creator': pymysql,
            'host': self.host,
            'port': self.port,
            'user': self.username,
            'password': self.password,
            'charset': self.charset,
            'cursorclass': pymysql.cursors.DictCursor,
            'maxconnections': self.pool_size,
            'ping': 7,
            'connect_timeout': self.connect_timeout,
            'read_timeout': self.read_timeout,
            'write_timeout': self.write_timeout,
            'autocommit': False
        }
        if self.ssl:
            required_keys = {'ca', 'cert', 'key'}
            if not all(k in self.ssl for k in required_keys):
                error_msg = 'SSL配置必须包含ca、cert和key'
                logger.error(error_msg)
                raise ValueError(error_msg)
            pool_params['ssl'] = {
                'ca': self.ssl['ca'],
                'cert': self.ssl['cert'],
                'key': self.ssl['key'],
                'check_hostname': self.ssl.get('check_hostname', False)
            }
        try:
            pool = PooledDB(**pool_params)
            logger.info('连接池创建成功', {'连接池': self.pool_size, 'host': self.host, 'port': self.port})
            return pool
        except Exception as e:
            self.pool = None
            logger.error('连接池创建失败', {'error': str(e), 'host': self.host, 'port': self.port})
            raise ConnectionError(f'连接池创建失败: {str(e)}')

    def _execute_with_retry(self, func):
        """
        带重试机制的装饰器，用于数据库操作

        :param func: 被装饰的函数
        :return: 装饰后的函数
        :raises: 可能抛出原始异常或最后一次重试的异常
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            operation = func.__name__
            logger.debug(f'开始执行操作: {operation}', {'max_retries': self.max_retries})
            for attempt in range(self.max_retries):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        logger.info('操作成功(重试后)', {'operation': operation, 'attempts': attempt + 1})
                    else:
                        logger.debug('操作成功', {'operation': operation})
                    return result
                except (pymysql.OperationalError, pymysql.err.MySQLError) as e:
                    last_exception = e
                    error_details = {
                        'operation': operation,
                        'error_code': e.args[0] if e.args else None,
                        'error_message': e.args[1] if len(e.args) > 1 else None,
                        'attempt': attempt + 1,
                        'max_retries': self.max_retries
                    }
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_interval * (attempt + 1)
                        error_details['wait_time'] = wait_time
                        logger.warning('数据库操作失败，准备重试', error_details)
                        time.sleep(wait_time)
                        try:
                            self.pool = self._create_connection_pool()
                            logger.info('成功重新建立数据库连接')
                        except Exception as reconnect_error:
                            logger.error('重连失败', {'error': str(reconnect_error)})
                    else:
                        logger.error('操作最终失败', error_details)
                except pymysql.IntegrityError as e:
                    logger.error('完整性约束错误', {
                        'operation': operation,
                        'error_code': e.args[0] if e.args else None,
                        'error_message': e.args[1] if len(e.args) > 1 else None
                    })
                    raise e
                except Exception as e:
                    last_exception = e
                    logger.error('发生意外错误', {
                        'operation': operation,
                        'error_type': type(e).__name__,
                        'error_message': str(e),
                        'error_args': e.args if hasattr(e, 'args') else None
                    })
                    break
            raise last_exception if last_exception else Exception('发生未知错误')
        return wrapper

    def _get_connection(self) -> pymysql.connections.Connection:
        """
        从连接池获取数据库连接

        :return: 数据库连接对象
        :raises ConnectionError: 当获取连接失败时抛出
        """
        try:
            conn = self.pool.connection()
            logger.debug('获取数据库连接', {'host': self.host, 'port': self.port})
            return conn
        except Exception as e:
            logger.error('获取数据库连接失败', {'error': str(e)})
            raise ConnectionError(f'连接数据库失败: {str(e)}')

    def _check_database_exists(self, db_name: str) -> bool:
        """
        检查数据库是否存在

        :param db_name: 数据库名称
        :return: 存在返回True，否则返回False
        :raises: 可能抛出数据库相关异常
        """
        db_name = self._validate_identifier(db_name)
        sql = 'SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s'
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (db_name,))
                    exists = bool(cursor.fetchone())
                    logger.debug('数据库存在检查', {'库': db_name, '存在': exists})
                    return exists
        except Exception as e:
            logger.error('检查数据库是否存在时出错', {'库': db_name, '错误': str(e)})
            raise

    def _create_database(self, db_name: str) -> None:
        """
        创建数据库

        :param db_name: 要创建的数据库名称
        :raises: 可能抛出数据库相关异常
        """
        db_name = self._validate_identifier(db_name)
        sql = f'CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET {self.charset} COLLATE {self.collation}'
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                logger.info('数据库已创建', {'库': db_name})
        except Exception as e:
            logger.error('无法创建数据库', {'库': db_name, '错误': str(e)})
            conn.rollback()
            raise

    def _get_partition_table_name(self, table_name: str, date_value: str, partition_by: str) -> str:
        """
        获取分表名称

        :param table_name: 基础表名
        :param date_value: 日期值
        :param partition_by: 分表方式 ('year' 或 'month')
        :return: 分表名称
        :raises ValueError: 如果日期格式无效或分表方式无效
        """
        try:
            date_obj = self._validate_datetime(date_value, True)
        except ValueError:
            logger.error('无效的日期格式', {'表': table_name, '日期值': date_value})
            raise ValueError(f"`{table_name}` 无效的日期格式: `{date_value}`")
        if partition_by == 'year':
            return f"{table_name}_{date_obj.year}"
        elif partition_by == 'month':
            return f"{table_name}_{date_obj.year}_{date_obj.month:02d}"
        else:
            logger.error('分表方式无效', {'表': table_name, '分表方式': partition_by})
            raise ValueError("分表方式必须是 'year' 或 'month' 或 'None'")

    def _validate_identifier(self, identifier: str) -> str:
        """
        验证并清理数据库标识符(表名、列名等)

        :param identifier: 要验证的标识符
        :return: 清理后的安全标识符
        :raises ValueError: 当标识符无效时抛出
        """
        if not identifier or not isinstance(identifier, str):
            logger.error('无效的标识符', {'标识符': identifier})
            raise ValueError(f"无效的标识符: `{identifier}`")
        if not self.case_sensitive:
            identifier = identifier.lower()
        cleaned = re.sub(r'[^ -\w\u4e00-\u9fff$]', '_', identifier)
        cleaned = re.sub(r'_+', '_', cleaned).strip('_')
        if not cleaned:
            logger.error('无法清理异常标识符', {'原始标识符': identifier})
            raise ValueError(f"无法清理异常标识符: `{identifier}`")
        mysql_keywords = {
            'select', 'insert', 'update', 'delete', 'from', 'where', 'and', 'or',
            'not', 'like', 'in', 'is', 'null', 'true', 'false', 'between'
        }
        if cleaned.lower() in mysql_keywords:
            logger.debug('存在MySQL保留字', {'标识符': cleaned})
            return f"`{cleaned}`"
        return cleaned

    def _check_table_exists(self, db_name: str, table_name: str) -> bool:
        """
        检查表是否存在

        :param db_name: 数据库名
        :param table_name: 表名
        :return: 存在返回True，否则返回False
        :raises: 可能抛出数据库相关异常
        """
        cache_key = f"{db_name}.{table_name}"
        if cache_key in self._table_metadata_cache:
            cached_time, result = self._table_metadata_cache[cache_key]
            if time.time() - cached_time < self.metadata_cache_ttl:
                logger.debug('表存在缓存命中', {'库': db_name, '表': table_name, '存在': result})
                return result
        db_name = self._validate_identifier(db_name)
        table_name = self._validate_identifier(table_name)
        sql = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (db_name, table_name))
                    result = bool(cursor.fetchone())
        except Exception as e:
            logger.error('检查数据表是否存在时发生未知错误', {'库': db_name, '表': table_name, '错误': str(e)})
            raise
        self._table_metadata_cache[cache_key] = (time.time(), result)
        logger.debug('表存在检查', {'库': db_name, '表': table_name, '存在': result})
        return result

    def _create_table(
            self,
            db_name: str,
            table_name: str,
            set_typ: Dict[str, str],
            primary_keys: Optional[List[str]] = None,
            date_column: Optional[str] = None,
            indexes: Optional[List[str]] = None,
            allow_null: bool = False
    ) -> None:
        """
        创建数据表

        :param db_name: 数据库名
        :param table_name: 表名
        :param set_typ: 列名和数据类型字典 {列名: 数据类型}
        :param primary_keys: 主键列列表，可选
        :param date_column: 日期列名，可选，如果存在将设置为索引
        :param indexes: 需要创建索引的列列表，可选
        :param allow_null: 是否允许空值，默认为False
        :raises: 可能抛出数据库相关异常
        """
        db_name = self._validate_identifier(db_name)
        table_name = self._validate_identifier(table_name)
        if not set_typ:
            logger.error('建表时未指定set_typ', {'库': db_name, '表': table_name})
            raise ValueError('set_typ 未指定')
        column_defs = ["`id` INT NOT NULL AUTO_INCREMENT"]
        for col_name, col_type in set_typ.items():
            if col_name.lower() == 'id':
                continue
            safe_col_name = self._validate_identifier(col_name)
            col_def = f"`{safe_col_name}` {col_type}"
            if not allow_null and not col_type.lower().startswith('json'):
                col_def += " NOT NULL"
            column_defs.append(col_def)
        if primary_keys:
            if 'id' not in [pk.lower() for pk in primary_keys]:
                primary_keys = ['id'] + primary_keys
        else:
            primary_keys = ['id']
        safe_primary_keys = [self._validate_identifier(pk) for pk in primary_keys]
        primary_key_sql = f", PRIMARY KEY (`{'`,`'.join(safe_primary_keys)}`)"
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (
            {','.join(column_defs)}
            {primary_key_sql}
        ) ENGINE=InnoDB DEFAULT CHARSET={self.charset} COLLATE={self.collation}
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    logger.info('数据表已创建', {'库': db_name, '表': table_name})
                index_statements = []
                if date_column and date_column in set_typ:
                    safe_date_col = self._validate_identifier(date_column)
                    index_statements.append(
                        f"ALTER TABLE `{db_name}`.`{table_name}` ADD INDEX `idx_{safe_date_col}` (`{safe_date_col}`)"
                    )
                if indexes:
                    for idx_col in indexes:
                        if idx_col in set_typ:
                            safe_idx_col = self._validate_identifier(idx_col)
                            index_statements.append(
                                f"ALTER TABLE `{db_name}`.`{table_name}` ADD INDEX `idx_{safe_idx_col}` (`{safe_idx_col}`)"
                            )
                if index_statements:
                    with conn.cursor() as cursor:
                        for stmt in index_statements:
                            cursor.execute(stmt)
                            logger.debug('执行索引语句', {'SQL': stmt})
                conn.commit()
                logger.info('索引已添加', {'库': db_name, '表': table_name, '索引': indexes})
        except Exception as e:
            logger.error('建表失败', {'库': db_name, '表': table_name, '错误': str(e)})
            conn.rollback()
            raise

    def _validate_datetime(self, value: str, date_type: bool = False) -> Any:
        """
        验证并标准化日期时间格式

        :param value: 日期时间值
        :param date_type: 是否返回日期类型(True)或字符串(False)
        :return: 标准化后的日期时间字符串或日期对象
        :raises ValueError: 当日期格式无效时抛出
        """
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d',
            '%Y%m%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y/%-m/%-d',  # 2023/1/8
            '%Y-%m-%-d',  # 2023-01-8
            '%Y-%-m-%-d'  # 2023-1-8
        ]
        for fmt in formats:
            try:
                if date_type:
                    result = pd.to_datetime(datetime.datetime.strptime(value, fmt).strftime('%Y-%m-%d'))
                    logger.debug('日期格式化成功', {'原始': value, '格式': fmt, '结果': str(result)})
                    return result
                else:
                    result = datetime.datetime.strptime(value, fmt).strftime('%Y-%m-%d %H:%M:%S')
                    logger.debug('日期格式化成功', {'原始': value, '格式': fmt, '结果': str(result)})
                    return result
            except ValueError:
                continue
        logger.error('无效的日期格式', {'值': value})
        raise ValueError(f"无效的日期格式: `{value}`")

    def _validate_value(self, value: Any, column_type: str, allow_null: bool) -> Any:
        """
        根据列类型验证并转换数据值

        :param value: 要验证的值
        :param column_type: 列的数据类型
        :param allow_null: 是否允许空值
        :return: 转换后的值
        :raises ValueError: 当值转换失败时抛出
        """
        if value is None:
            if not allow_null:
                logger.warning('字段值为None但不允许空值', {'字段类型': column_type})
                return 'none'
            return None
        try:
            column_type_lower = column_type.lower()
            if isinstance(value, str) and value.strip().endswith('%'):
                try:
                    percent_str = value.strip().replace('%', '')
                    percent_value = float(percent_str)
                    decimal_value = percent_value / 100
                    logger.debug('百分比字符串转小数', {'原始': value, '结果': decimal_value})
                    return decimal_value
                except ValueError:
                    logger.warning('百分比字符串转小数失败', {'原始': value})
            elif 'int' in column_type_lower:
                if isinstance(value, str):
                    value = value.replace(',', '').strip()
                    try:
                        return int(float(value))
                    except ValueError:
                        logger.error('字符串转整数失败', {'值': value})
                        raise ValueError(f"`{value}` -> 无法转为整数")
                return int(value) if value is not None else None
            elif any(t in column_type_lower for t in ['float', 'double', 'decimal']):
                if isinstance(value, str):
                    value = value.replace(',', '')
                return float(value) if value is not None else None
            elif 'date' in column_type_lower or 'time' in column_type_lower:
                if isinstance(value, (datetime.datetime, pd.Timestamp)):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, str):
                    try:
                        return self._validate_datetime(value)
                    except ValueError as e:
                        logger.error('无效日期格式', {'值': value, '错误': str(e)})
                        raise ValueError(f"无效日期格式: `{value}` -> {str(e)}")
                return str(value)
            elif 'char' in column_type_lower or 'text' in column_type_lower:
                if isinstance(value, str):
                    return value.replace('\\', '\\\\').replace("'", "\\'")
                return str(value)
            elif 'json' in column_type_lower:
                return json.dumps(value) if value is not None else None
            else:
                return value
        except (ValueError, TypeError) as e:
            logger.error('数据类型转换异常', {'值': value, '目标类型': column_type, '错误': str(e)})
            raise ValueError(f"转换异常 -> 无法将 `{value}` 的数据类型转为: `{column_type}` -> {str(e)}")

    def _get_table_columns(self, db_name: str, table_name: str) -> Dict[str, str]:
        """
        获取表的列名和数据类型

        :param db_name: 数据库名
        :param table_name: 表名
        :return: 列名和数据类型字典 {列名: 数据类型}
        :raises: 可能抛出数据库相关异常
        """
        db_name = self._validate_identifier(db_name)
        table_name = self._validate_identifier(table_name)
        sql = """
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (db_name, table_name))
                    set_typ = {row['COLUMN_NAME'].lower(): row['DATA_TYPE'] for row in cursor.fetchall()}
                    logger.debug('获取表的列信息', {'库': db_name, '表': table_name, '列信息': set_typ})
                    return set_typ
        except Exception as e:
            logger.error('无法获取表列信息', {'库': db_name, '表': table_name, '错误': str(e)})
            raise

    def _upload_to_table(
            self,
            db_name: str,
            table_name: str,
            data: List[Dict],
            set_typ: Dict[str, str],
            primary_keys: Optional[List[str]],
            check_duplicate: bool,
            duplicate_columns: Optional[List[str]],
            allow_null: bool,
            auto_create: bool,
            date_column: Optional[str],
            indexes: Optional[List[str]],
            batch_id: Optional[str] = None,
            update_on_duplicate: bool = False,
            transaction_mode: str = "batch"
    ):
        """实际执行表上传的方法"""
        # 检查表是否存在
        if not self._check_table_exists(db_name, table_name):
            if auto_create:
                self._create_table(db_name, table_name, set_typ, primary_keys, date_column, indexes,
                                   allow_null=allow_null)
            else:
                logger.error('数据表不存在', {
                    '库': db_name,
                    '表': table_name,
                    'func': sys._getframe().f_code.co_name,
                })
                raise ValueError(f"数据表不存在: `{db_name}`.`{table_name}`")

        # 获取表结构并验证
        table_columns = self._get_table_columns(db_name, table_name)
        if not table_columns:
            logger.error('获取列失败', {
                '库': db_name,
                '表': table_name,
                '列': self._shorten_for_log(table_columns),
                'func': sys._getframe().f_code.co_name,
            })
            raise ValueError(f"获取列失败 `{db_name}`.`{table_name}`")

        # 验证数据列与表列匹配
        for col in set_typ:
            if col not in table_columns:
                logger.error('列不存在', {
                    '库': db_name,
                    '表': table_name,
                    '列': col,
                    'func': sys._getframe().f_code.co_name,
                })
                raise ValueError(f"列不存在: `{col}` -> `{db_name}`.`{table_name}`")

        # 插入数据
        self._insert_data(
            db_name, table_name, data, set_typ,
            check_duplicate, duplicate_columns,
            batch_id=batch_id,
            update_on_duplicate=update_on_duplicate,
            transaction_mode=transaction_mode
        )

    def _infer_data_type(self, value: Any) -> str:
        """
        根据值推断合适的MySQL数据类型

        :param value: 要推断的值
        :return: MySQL数据类型字符串
        """
        if value is None or str(value).lower() in ['', 'none', 'nan']:
            return 'VARCHAR(255)'  # 默认字符串类型

        # 检查是否是百分比字符串
        if isinstance(value, str):
            if value.endswith('%'):
                return 'DECIMAL(10,4)'  # 百分比统一使用DECIMAL(10,4)

        if isinstance(value, bool):
            return 'TINYINT(1)'
        elif isinstance(value, int):
            # if -128 <= value <= 127:
            #     return 'TINYINT'
            # elif -32768 <= value <= 32767:
            #     return 'SMALLINT'
            # elif -8388608 <= value <= 8388607:
            #     return 'MEDIUMINT'
            if -2147483648 <= value <= 2147483647:
                return 'INT'
            else:
                return 'BIGINT'
        elif isinstance(value, float):
            # 计算小数位数
            num_str = str(value)
            _, decimal_places = count_decimal_places(num_str)
            return f'DECIMAL(20,{min(decimal_places, 6)})'  # 限制最大6位小数
        elif isinstance(value, (datetime.datetime, pd.Timestamp)):
            return 'DATETIME'
        elif isinstance(value, datetime.date):
            return 'DATE'
        elif isinstance(value, (list, dict)):
            return 'JSON'
        elif isinstance(value, str):
            # 尝试判断是否是日期时间
            try:
                self._validate_datetime(value)
                return 'DATETIME'
            except ValueError:
                pass

            # 根据字符串长度选择合适类型
            length = len(value)
            if length <= 255:
                return 'VARCHAR(255)'
            elif length <= 65535:
                return 'TEXT'
            elif length <= 16777215:
                return 'MEDIUMTEXT'
            else:
                return 'LONGTEXT'
        else:
            return 'VARCHAR(255)'

    def normalize_column_names(self, data: Union[pd.DataFrame, List[Dict[str, Any]]]) -> Union[
        pd.DataFrame, List[Dict[str, Any]]]:
        """
        1. pandas：规范化列名
        2. 字典列表：规范化每个字典的键

        参数：
            data: 输入数据，支持两种类型：
                  - pandas.DataFrame：将规范化其列名
                  - List[Dict[str, Any]]：将规范化列表中每个字典的键
        """
        if isinstance(data, pd.DataFrame):
            data.columns = [self._validate_identifier(col) for col in data.columns]
            return data
        elif isinstance(data, list):
            return [{self._validate_identifier(k): v for k, v in item.items()} for item in data]
        return data

    def _prepare_data(
            self,
            data: Union[Dict, List[Dict], pd.DataFrame],
            set_typ: Dict[str, str],
            allow_null: bool = False
    ) -> Tuple[List[Dict], Dict[str, str]]:
        """
        准备要上传的数据，验证并转换数据类型

        :param data: 输入数据，可以是字典、字典列表或DataFrame
        :param set_typ: 列名和数据类型字典 {列名: 数据类型}
        :param allow_null: 是否允许空值
        :return: 元组(准备好的数据列表, 过滤后的列类型字典)
        :raises ValueError: 当数据验证失败时抛出
        """
        # 统一数据格式为字典列表
        if isinstance(data, pd.DataFrame):
            try:
                # 将列名转为小写
                data.columns = [col.lower() for col in data.columns]
                data = data.replace({pd.NA: None}).to_dict('records')
            except Exception as e:
                logger.error('数据转字典时发生错误', {
                    'error': str(e),
                    'data': self._shorten_for_log(data),
                    'func': sys._getframe().f_code.co_name,
                })
                raise ValueError(f"数据转字典时发生错误: {e}")
        elif isinstance(data, dict):
            data = [{k.lower(): v for k, v in data.items()}]
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # 将列表中的每个字典键转为小写
            data = [{k.lower(): v for k, v in item.items()} for item in data]
        else:
            logger.error('数据结构必须是字典、列表、字典列表或dataframe', {
                'data': self._shorten_for_log(data),
                'func': sys._getframe().f_code.co_name,
            })
            raise ValueError("数据结构必须是字典、列表、字典列表或dataframe")

        # 统一处理原始数据中列名的特殊字符
        data = self.normalize_column_names(data)

        # 将set_typ的键转为小写
        set_typ = {k.lower(): v for k, v in set_typ.items()}

        # 获取数据中实际存在的列名
        data_columns = set()
        if data and len(data) > 0:
            data_columns = set(data[0].keys())

        # 过滤set_typ，只保留数据中存在的列
        filtered_set_typ = {}
        for col in data_columns:
            if col in set_typ:
                filtered_set_typ[col] = set_typ[col]
            else:
                # 如果列不在set_typ中，尝试推断类型
                sample_values = [row[col] for row in data if col in row and row[col] is not None][:10]
                if sample_values:
                    inferred_type = self._infer_data_type(sample_values[0])
                    filtered_set_typ[col] = inferred_type
                    logger.debug(f"自动推断列 `{col}` 的数据类型为: `{inferred_type}`")
                else:
                    # 没有样本值，使用默认类型
                    filtered_set_typ[col] = 'VARCHAR(255)'
                    logger.debug(f"列 `{col}` 使用默认数据类型: VARCHAR(255)")

        prepared_data = []
        for row_idx, row in enumerate(data, 1):
            prepared_row = {}
            for col_name in filtered_set_typ:
                # 跳过id列，不允许外部传入id
                if col_name.lower() == 'id':
                    continue

                if col_name not in row:
                    if not allow_null:
                        error_msg = f"行号:{row_idx} -> 缺失列: `{col_name}`"
                        logger.error(error_msg, {'row': self._shorten_for_log(row)})
                        raise ValueError(error_msg)
                    prepared_row[col_name] = None
                else:
                    try:
                        prepared_row[col_name] = self._validate_value(row[col_name], filtered_set_typ[col_name], allow_null)
                    except ValueError as e:
                        logger.error('数据验证失败', {
                            '列': col_name,
                            '行': row_idx,
                            '报错': str(e),
                            'row': self._shorten_for_log(row),
                            'func': sys._getframe().f_code.co_name,
                        })
                        raise ValueError(f"行:{row_idx}, 列:`{col_name}`-> 报错: {str(e)}")
            prepared_data.append(prepared_row)

        return prepared_data, filtered_set_typ

    def upload_data(
            self,
            db_name: str,
            table_name: str,
            data: Union[Dict, List[Dict], pd.DataFrame],
            set_typ: Dict[str, str],
            primary_keys: Optional[List[str]] = None,
            check_duplicate: bool = False,
            duplicate_columns: Optional[List[str]] = None,
            allow_null: bool = False,
            partition_by: Optional[str] = None,
            partition_date_column: str = '日期',
            auto_create: bool = True,
            indexes: Optional[List[str]] = None,
            update_on_duplicate: bool = False,
            transaction_mode: str = "batch"
    ):
        """
        上传数据到数据库的主入口方法

        :param db_name: 数据库名
        :param table_name: 表名
        :param data: 要上传的数据，支持字典、字典列表或DataFrame格式
        :param set_typ: 列名和数据类型字典 {列名: 数据类型}
        :param primary_keys: 主键列列表，可选
        :param check_duplicate: 是否检查重复数据，默认为False
        :param duplicate_columns: 用于检查重复的列，可选
        :param allow_null: 是否允许空值，默认为False
        :param partition_by: 分表方式('year'或'month')，可选
        :param partition_date_column: 用于分表的日期列名，默认为'日期'
        :param auto_create: 表不存在时是否自动创建，默认为True
        :param indexes: 需要创建索引的列列表，可选
        :param update_on_duplicate: 遇到重复数据时是否更新旧数据，默认为False
        :param transaction_mode: 事务模式，可选值：
            - 'row'     : 逐行提交事务（错误隔离性好）
            - 'batch'   : 整批提交事务（性能最优）
            - 'hybrid'  : 混合模式（每N行提交，平衡性能与安全性）
        :raises: 可能抛出各种验证和数据库相关异常
        """
        # upload_start = time.time()
        initial_row_count = len(data) if hasattr(data, '__len__') else 1

        batch_id = f"batch_{int(time.time() * 1000)}"
        success_flag = False

        logger.info("开始上传", {
            '库': db_name,
            '表': table_name,
            '批次': batch_id,
            '传入': len(data) if hasattr(data, '__len__') else 1,
            '参数': {
                '主键': primary_keys,
                '去重': check_duplicate,
                '去重列': duplicate_columns,
                '允许空值': allow_null,
                '分表方式': partition_by,
                '分表列': partition_date_column,
                # '自动建表': auto_create,
                '索引': indexes,
                '更新旧数据': update_on_duplicate,
                '事务模式': transaction_mode
            },
            '数据样例': self._shorten_for_log(data, 2)
        })

        try:
            # 验证参数
            if partition_by:
                partition_by = str(partition_by).lower()
                if partition_by not in ['year', 'month']:
                    logger.error('分表方式必须是 "year" 或 "month" 或 "None', {
                        '库': db_name,
                        '表': table_name,
                        '批次': batch_id,
                        '分表方式': partition_by,
                        'func': sys._getframe().f_code.co_name,
                    })
                    raise ValueError("分表方式必须是 'year' 或 'month' 或 'None'")

            # 准备数据
            prepared_data, filtered_set_typ = self._prepare_data(data, set_typ, allow_null)

            # 检查数据库是否存在
            if not self._check_database_exists(db_name):
                if auto_create:
                    self._create_database(db_name)
                else:
                    logger.error('数据库不存在', {
                        '库': db_name,
                        'func': sys._getframe().f_code.co_name,
                    })
                    raise ValueError(f"数据库不存在: `{db_name}`")

            # 处理分表逻辑
            if partition_by:
                partitioned_data = {}
                for row in prepared_data:
                    try:
                        if partition_date_column not in row:
                            logger.error('异常缺失列',{
                                '库': db_name,
                                '表': table_name,
                                '批次': batch_id,
                                '缺失列': partition_date_column,
                                'row': self._shorten_for_log(row),
                                'func': sys._getframe().f_code.co_name,
                            })
                            continue  # 跳过当前行

                        part_table = self._get_partition_table_name(
                            table_name,
                            str(row[partition_date_column]),
                            partition_by
                        )
                        if part_table not in partitioned_data:
                            partitioned_data[part_table] = []
                        partitioned_data[part_table].append(row)
                    except Exception as e:
                        logger.error('分表处理异常', {
                            '库': db_name,
                            '表': table_name,
                            'row_data': self._shorten_for_log(row),
                            'error': str(e),
                            'func': sys._getframe().f_code.co_name,
                        })
                        continue  # 跳过当前行

                # 对每个分表执行上传
                for part_table, part_data in partitioned_data.items():
                    try:
                        self._upload_to_table(
                            db_name, part_table, part_data, filtered_set_typ,
                            primary_keys, check_duplicate, duplicate_columns,
                            allow_null, auto_create, partition_date_column,
                            indexes, batch_id, update_on_duplicate, transaction_mode
                        )
                    except Exception as e:
                        logger.error('分表上传异常', {
                            '库': db_name,
                            '表': table_name,
                            '分表': part_table,
                            'error': str(e),
                            '数据样例': self._shorten_for_log(part_data, 2),
                            'func': sys._getframe().f_code.co_name,
                        })
                        continue  # 跳过当前分表，继续处理其他分表
            else:
                # 不分表，直接上传
                self._upload_to_table(
                    db_name, table_name, prepared_data, filtered_set_typ,
                    primary_keys, check_duplicate, duplicate_columns,
                    allow_null, auto_create, partition_date_column,
                    indexes, batch_id, update_on_duplicate, transaction_mode
                )

            success_flag = True

        except Exception as e:
            logger.error('上传过程发生全局错误', {
                '库': db_name,
                '表': table_name,
                'error': str(e),
                'error_type': type(e).__name__,
                '数据样例': self._shorten_for_log(data, 2),
                'func': sys._getframe().f_code.co_name,
            })
        finally:
            logger.info("存储完成", {
                '库': db_name,
                '表': table_name,
                '批次': batch_id,
                'finish': success_flag,
                # '耗时': round(time.time() - upload_start, 2),
                '数据行': initial_row_count
            })

    def _insert_data(
            self,
            db_name: str,
            table_name: str,
            data: List[Dict],
            set_typ: Dict[str, str],
            check_duplicate: bool,
            duplicate_columns: Optional[List[str]],
            batch_id: Optional[str] = None,
            update_on_duplicate: bool = False,
            transaction_mode: str = "batch"
    ):
        """
        实际执行数据插入的方法

        :param db_name: 数据库名
        :param table_name: 表名
        :param data: 要插入的数据列表
        :param set_typ: 列名和数据类型字典 {列名: 数据类型}
        :param check_duplicate: 是否检查重复数据
        :param duplicate_columns: 用于检查重复的列，可选
        :param batch_id: 批次ID用于日志追踪，可选
        :param update_on_duplicate: 遇到重复数据时是否更新旧数据，默认为False
        :param transaction_mode: 事务模式，可选值：
            - 'row'     : 逐行提交事务（错误隔离性好）
            - 'batch'   : 整批提交事务（性能最优）
            - 'hybrid'  : 混合模式（每N行提交，平衡性能与安全性）
        """
        if not data:
            return

        # 验证事务模式
        transaction_mode = self._validate_transaction_mode(transaction_mode)

        # 准备SQL语句
        sql = self._prepare_insert_sql(
            db_name, table_name, set_typ,
            check_duplicate, duplicate_columns,
            update_on_duplicate
        )

        # 执行批量插入
        total_inserted, total_skipped, total_failed = self._execute_batch_insert(
            db_name, table_name, data, set_typ,
            sql, check_duplicate, duplicate_columns,
            batch_id, transaction_mode,
            update_on_duplicate
        )

        logger.info('插入完成', {
            '库': db_name,
            '表': table_name,
            '总计': len(data),
            '插入': total_inserted,
            '跳过': total_skipped,
            '失败': total_failed,
            '事务模式': transaction_mode,
        })

    def _validate_transaction_mode(self, mode: str) -> str:
        """验证并标准化事务模式"""
        valid_modes = ('row', 'batch', 'hybrid')
        if mode.lower() not in valid_modes:
            logger.error('事务模式参数错误', {
                '错误值': mode,
                '可选值': valid_modes,
                '自动使用默认模式': 'batch',
                'func': sys._getframe().f_code.co_name,
            })
            return 'batch'
        return mode.lower()

    def _build_simple_insert_sql(self, db_name, table_name, columns, update_on_duplicate):
        safe_columns = [self._validate_identifier(col) for col in columns]
        placeholders = ','.join(['%s'] * len(safe_columns))

        sql = f"""
            INSERT INTO `{db_name}`.`{table_name}` 
            (`{'`,`'.join(safe_columns)}`) 
            VALUES ({placeholders})
        """

        # 情况2：不检查重复但允许更新
        if update_on_duplicate:
            update_clause = ", ".join([f"`{col}` = VALUES(`{col}`)"
                                     for col in columns])
            sql += f" ON DUPLICATE KEY UPDATE {update_clause}"

        return sql

    def _build_duplicate_check_sql(self, db_name, table_name, all_columns,
                                   duplicate_columns, update_on_duplicate, set_typ):
        if duplicate_columns is None:
            duplicate_columns = []
        duplicate_columns = [_item for _item in duplicate_columns if _item.lower() not in self.base_excute_col]
        safe_columns = [self._validate_identifier(col) for col in all_columns]
        placeholders = ','.join(['%s'] * len(safe_columns))

        # 确定排重列（排除id和更新时间列）
        dup_cols = duplicate_columns if duplicate_columns else all_columns

        # 构建排重条件
        conditions = []
        for col in dup_cols:
            col_type = set_typ.get(col, '').lower()
            if col_type.startswith('decimal'):
                scale = self._get_decimal_scale(col_type)
                conditions.append(f"ROUND(`{col}`, {scale}) = ROUND(%s, {scale})")
            else:
                conditions.append(f"`{col}` = %s")

        # 情况3/5：允许更新
        if update_on_duplicate:
            update_clause = ", ".join([f"`{col}` = VALUES(`{col}`)"
                                       for col in all_columns])
            sql = f"""
                INSERT INTO `{db_name}`.`{table_name}` 
                (`{'`,`'.join(safe_columns)}`) 
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_clause}
            """
        else:
            # 情况4/6：不允许更新
            sql = f"""
                INSERT INTO `{db_name}`.`{table_name}` 
                (`{'`,`'.join(safe_columns)}`) 
                SELECT {placeholders}
                FROM DUAL
                WHERE NOT EXISTS (
                    SELECT 1 FROM `{db_name}`.`{table_name}`
                    WHERE {' AND '.join(conditions)}
                )
            """
        return sql

    def _get_decimal_scale(self, decimal_type: str) -> int:
        """
        从DECIMAL类型定义中提取小数位数

        :param decimal_type: DECIMAL类型字符串，如'DECIMAL(10,4)'
        :return: 小数位数
        :raises: 无显式抛出异常，但解析失败时返回默认值2
        """
        try:
            # 匹配DECIMAL类型中的精度和小数位数
            match = re.match(r'decimal\((\d+),\s*(\d+)\)', decimal_type.lower())
            if match:
                return int(match.group(2))
        except (ValueError, AttributeError, IndexError):
            pass

        # 默认返回2位小数
        return 2

    def _prepare_insert_sql(
            self,
            db_name: str,
            table_name: str,
            set_typ: Dict[str, str],
            check_duplicate: bool,
            duplicate_columns: Optional[List[str]],
            update_on_duplicate: bool
    ) -> str:
        """
        准备插入SQL语句

        1. 当 check_duplicate=False 时，忽略 duplicate_columns 和 update_on_duplicate 参数，直接插入全部data。
        2. 当 check_duplicate=False 且 update_on_duplicate=True 时，由于 check_duplicate=False，直接插入全部data。
        3. 当 check_duplicate=True 且 duplicate_columns=[] 且 update_on_duplicate=True 时，获取数据库所有列（但排除`id`和`更新时间`列），按这些列（不含`id`和`更新时间`）排重插入，遇到重复数据时更新旧数据。
        4. 当 check_duplicate=True 且 duplicate_columns=[] 且 update_on_duplicate=False 时，获取数据库所有列（但排除`id`和`更新时间`列），按这些列（不含`id`和`更新时间`）排重插入，不考虑是否更新旧数据。
        5. 当 check_duplicate=True 且 duplicate_columns 指定了排重列且 update_on_duplicate=True 时，按 duplicate_columns 指定的列（但排除`id`和`更新时间`）排重插入，遇到重复数据时更新旧数据。
        6. 当 check_duplicate=True 且 duplicate_columns 指定了排重列且 update_on_duplicate=False 时，按 duplicate_columns 指定的列（但排除`id`和`更新时间`）排重插入，不考虑是否更新旧数据。

        """
        # 获取所有列名（排除id）
        all_columns = [col for col in set_typ.keys()
                       if col.lower() != 'id']

        # 情况1-2：不检查重复
        if not check_duplicate:
            return self._build_simple_insert_sql(db_name, table_name, all_columns,
                                                 update_on_duplicate)

        # 确定排重列（排除id和更新时间列）
        dup_cols = duplicate_columns if duplicate_columns else [
            col for col in all_columns
            if col.lower() not in self.base_excute_col
        ]

        # 情况3-6：检查重复
        return self._build_duplicate_check_sql(db_name, table_name, all_columns,
                                               dup_cols, update_on_duplicate, set_typ)

    def _execute_batch_insert(
            self,
            db_name: str,
            table_name: str,
            data: List[Dict],
            set_typ: Dict[str, str],
            sql: str,
            check_duplicate: bool,
            duplicate_columns: Optional[List[str]],
            batch_id: Optional[str],
            transaction_mode: str,
            update_on_duplicate: bool = False
    ) -> Tuple[int, int, int]:
        """执行批量插入操作"""

        def get_optimal_batch_size(total_rows: int) -> int:
            # 根据数据量调整批量大小
            if total_rows <= 100:
                return total_rows
            elif total_rows <= 1000:
                return 500
            elif total_rows <= 10000:
                return 1000
            else:
                return 2000
        
        batch_size = get_optimal_batch_size(len(data))
        
        # 获取所有列名（排除id列）
        all_columns = [col for col in set_typ.keys()
                       if col.lower() != 'id']

        total_inserted = 0
        total_skipped = 0
        total_failed = 0

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                for i in range(0, len(data), batch_size):
                    batch = data[i:i + batch_size]
                    batch_inserted, batch_skipped, batch_failed = self._process_batch(
                        conn, cursor, db_name, table_name, batch, all_columns,
                        sql, check_duplicate, duplicate_columns, batch_id,
                        transaction_mode, update_on_duplicate
                    )

                    # 更新总统计
                    total_inserted += batch_inserted
                    total_skipped += batch_skipped
                    total_failed += batch_failed

        return total_inserted, total_skipped, total_failed

    def _process_batch(
            self,
            conn,
            cursor,
            db_name: str,
            table_name: str,
            batch: List[Dict],
            all_columns: List[str],
            sql: str,
            check_duplicate: bool,
            duplicate_columns: Optional[List[str]],
            batch_id: Optional[str],
            transaction_mode: str,
            update_on_duplicate: bool = False
    ) -> Tuple[int, int, int]:
        """
        处理单个批次的数据插入

        :param conn: 数据库连接对象
        :param cursor: 数据库游标对象
        :param db_name: 数据库名
        :param table_name: 表名
        :param batch: 当前批次的数据（字典列表）
        :param all_columns: 需要插入的所有列名
        :param sql: 执行的SQL语句
        :param check_duplicate: 是否检查重复
        :param duplicate_columns: 排重列
        :param batch_id: 批次ID
        :param transaction_mode: 事务模式
        :param update_on_duplicate: 遇到重复时是否更新
        :return: (插入数, 跳过数, 失败数)
        """
        batch_inserted = 0
        batch_skipped = 0
        batch_failed = 0
        batch_size = len(batch)
        logger.debug('批次插入开始', {
            '库': db_name,
            '表': table_name,
            '批次ID': batch_id,
            '批次大小': batch_size,
            '事务模式': transaction_mode,
            'SQL预览': sql[:200],
            '排重': check_duplicate,
            '排重列': duplicate_columns,
            '允许更新': update_on_duplicate,
            '数据样例': self._shorten_for_log(batch, 2)
        })
        if transaction_mode == 'batch':
            try:
                for row_idx, row in enumerate(batch, 1):
                    result = self._process_single_row(
                        db_name, table_name, cursor, row, all_columns, sql,
                        check_duplicate, duplicate_columns, update_on_duplicate
                    )
                    if result == 'inserted':
                        batch_inserted += 1
                    elif result == 'skipped':
                        batch_skipped += 1
                    else:
                        batch_failed += 1
                conn.commit()
                logger.debug('批次插入成功', {
                    '库': db_name,
                    '表': table_name,
                    '批次ID': batch_id,
                    '插入': batch_inserted,
                    '跳过': batch_skipped,
                    '失败': batch_failed
                })
            except Exception as e:
                conn.rollback()
                batch_failed += len(batch)
                logger.error('批次插入失败', {
                    '库': db_name,
                    '表': table_name,
                    '批次ID': batch_id,
                    '错误': str(e),
                    'SQL预览': sql[:200],
                    '数据样例': self._shorten_for_log(batch, 2)
                })
        else:  # row 或 hybrid 模式
            for row_idx, row in enumerate(batch, 1):
                try:
                    result = self._process_single_row(
                        db_name, table_name, cursor, row, all_columns, sql,
                        check_duplicate, duplicate_columns, update_on_duplicate
                    )
                    if result == 'inserted':
                        batch_inserted += 1
                    elif result == 'skipped':
                        batch_skipped += 1
                    else:
                        batch_failed += 1
                    conn.commit()
                    logger.debug('单行插入成功', {
                        '库': db_name,
                        '表': table_name,
                        '批次ID': batch_id,
                        '行号': row_idx,
                        '插入状态': result
                    })
                except Exception as e:
                    conn.rollback()
                    batch_failed += 1
                    logger.error('单行插入失败', {
                        '库': db_name,
                        '表': table_name,
                        '批次ID': batch_id,
                        '行号': row_idx,
                        '错误': str(e),
                        'SQL预览': sql[:200],
                        '数据': self._shorten_for_log(row)
                    })
        logger.debug('批次插入结束', {
            '库': db_name,
            '表': table_name,
            '批次ID': batch_id,
            '插入': batch_inserted,
            '跳过': batch_skipped,
            '失败': batch_failed,
            '数据样例': self._shorten_for_log(batch, 2)
        })
        return batch_inserted, batch_skipped, batch_failed

    def _process_single_row(
            self,
            db_name: str,
            table_name: str,
            cursor,
            row: Dict,
            all_columns: List[str],
            sql: str,
            check_duplicate: bool,
            duplicate_columns: Optional[List[str]],
            update_on_duplicate: bool = False
    ) -> str:
        """
        处理单行数据插入

        :param db_name: 数据库名
        :param table_name: 表名
        :param cursor: 数据库游标对象
        :param row: 单行数据（字典）
        :param all_columns: 需要插入的所有列名
        :param sql: 执行的SQL语句
        :param check_duplicate: 是否检查重复
        :param duplicate_columns: 排重列
        :param update_on_duplicate: 遇到重复时是否更新
        :return: 'inserted' | 'skipped' | 'failed'
        """
        try:
            # 构造参数
            values = [row.get(col) for col in all_columns]
            if check_duplicate:
                # 需要为 WHERE NOT EXISTS 语句补充参数
                if not update_on_duplicate:
                    # duplicate_columns 为空时，默认用所有列（排除id/更新时间）
                    dup_cols = duplicate_columns if duplicate_columns else [col for col in all_columns if col.lower() not in self.base_excute_col]
                    values = values + [row.get(col) for col in dup_cols]
            cursor.execute(sql, values)
        except Exception as e:
            logger.error('单行插入失败', {
                '库': db_name,
                '表': table_name,
                'row': self._shorten_for_log(row),
                '错误': str(e)
            })
            return 'failed'
        return 'inserted'

    def close(self) -> None:
        """
        关闭连接池并清理资源
        这个方法会安全地关闭数据库连接池，并清理相关资源。
        建议结束时手动调用此方法。
        :raises: 可能抛出关闭连接时的异常
        """
        try:
            if hasattr(self, 'pool') and self.pool is not None:
                try:
                    self.pool.close()
                except Exception as e:
                    logger.warning('关闭连接池时出错', {'error': str(e)})
                self.pool = None
                logger.info('连接池关闭', {'uploader.py': '连接池关闭'})
        except Exception as e:
            logger.error('关闭连接池失败', {'error': str(e)})
            raise

    def _check_pool_health(self) -> bool:
        """
        检查连接池健康状态
        :return: 连接池健康返回True，否则返回False
        """
        conn = None
        try:
            conn = self.pool.connection()
            conn.ping(reconnect=True)
            logger.debug('连接池健康检查通过')
            return True
        except Exception as e:
            logger.warning('连接池健康检查失败', {'error': str(e)})
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    logger.warning('关闭连接时出错', {'error': str(e)})

    def retry_on_failure(max_retries: int = 3, delay: int = 1):
        """
        通用重试装饰器
        :param max_retries: 最大重试次数
        :param delay: 重试间隔（秒）
        :return: 装饰器
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except (pymysql.OperationalError, pymysql.InterfaceError) as e:
                        last_exception = e
                        logger.warning('操作失败，准备重试', {'attempt': attempt + 1, 'error': str(e)})
                        if attempt < max_retries - 1:
                            time.sleep(delay * (attempt + 1))
                            continue
                        logger.error(f'操作重试 {max_retries} 次后失败', {'error': str(e)})
                        raise
                    except Exception as e:
                        logger.error('操作失败', {'error': str(e)})
                        raise
                raise last_exception if last_exception else logger.error('操作重试失败，未知错误')
            return wrapper
        return decorator

    def _shorten_for_log(self, obj: Any, maxlen: int = 200) -> Any:
        """
        日志安全截断工具：对字符串、列表、字典等做长度限制，避免日志过长。
        :param obj: 原始对象
        :param maxlen: 最大长度/元素数
        :return: 截断后的对象
        """
        if isinstance(obj, str):
            return obj[:maxlen] + ("..." if len(obj) > maxlen else "")
        elif isinstance(obj, list):
            return obj[:maxlen] + (["..."] if len(obj) > maxlen else [])
        elif isinstance(obj, dict):
            short = {k: self._shorten_for_log(v, maxlen) for i, (k, v) in enumerate(obj.items()) if i < maxlen}
            if len(obj) > maxlen:
                short['...'] = f"total_keys={len(obj)}"
            return short
        elif hasattr(obj, 'shape') and hasattr(obj, 'head'):
            # pandas DataFrame
            return f"DataFrame shape={obj.shape}, head={obj.head(1).to_dict()}"
        return obj
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """
    示例：
    1. 创建上传器实例
    2. 定义数据表结构
    3. 准备测试数据
    4. 上传数据到数据库
    5. 关闭连接
    """
    uploader = MySQLUploader(
        username='root',
        password='pw',
        host='localhost',
        port=3306,
    )

    # 定义列和数据类型
    set_typ = {
        'name': 'VARCHAR(255)',
        'age': 'INT',
        'salary': 'DECIMAL(10,2)',
        '日期': 'DATE',
        'shop': None,
    }

    # 准备数据
    data = [
        {'日期': '2023-01-8', 'name': 'JACk', 'AGE': '24', 'salary': 555.1545},
        {'日期': '2023-01-15', 'name': 'Alice', 'AGE': 35, 'salary': '100'},
        {'日期': '2023-01-15', 'name': 'Alice', 'AGE': 30, 'salary': 0.0},
        {'日期': '2023-02-20', 'name': 'Bob', 'AGE': 25, 'salary': 45000.75}
    ]

    # 上传数据
    uploader.upload_data(
        db_name='测试库',
        table_name='测试表',
        data=data,
        set_typ=set_typ,  # 定义列和数据类型
        primary_keys=[],  # 创建唯一主键
        check_duplicate=False,  # 检查重复数据
        duplicate_columns=[],  # 指定排重的组合键
        allow_null=False,  # 允许插入空值
        partition_by='year',  # 按月分表
        partition_date_column='日期',  # 用于分表的日期列名，默认为'日期'
        auto_create=True,  # 表不存在时自动创建, 默认参数不要更改
        indexes=[],  # 指定索引列
        transaction_mode='row',  # 事务模式
    )

    uploader.close()


if __name__ == '__main__':
    # main()
    pass
