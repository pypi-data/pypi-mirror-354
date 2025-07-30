# core.py
"""
核心模块，包含数据库连接和核心功能
使用纯 pytds 驱动连接 MSSQL
"""

import json
from typing import Dict, List, Optional, Union, Any
import pytds

from .app_config import config

# 数据库连接管理
connection = None

def _is_connection_closed(conn):
    """检查连接是否已关闭"""
    if conn is None:
        return True
    try:
        # 尝试执行一个简单的查询来检查连接状态
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return False
    except Exception:
        return True

def get_db_connection():
    """获取数据库连接，如果不存在则创建新连接"""
    global connection
    if connection is None or _is_connection_closed(connection):
        try:
            print("正在创建数据库连接...")
            print(f"连接到: {config.DB_HOST}:{config.DB_PORT}, 数据库: {config.DB_NAME}, 用户: {config.DB_USER}")
            
            # 使用 pytds 创建连接
            connection = pytds.connect(
                server=config.DB_HOST,
                port=int(config.DB_PORT),
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                timeout=30,  # 连接超时时间（秒）
                autocommit=True  # 自动提交，因为我们只做查询
            )
            
            # 测试连接
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                print(f"测试连接结果: {result}")
                
            print("数据库连接创建成功")
        except Exception as e:
            error_msg = f"数据库连接失败: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
    return connection

def execute_query(sql: str) -> Dict[str, Any]:
    """执行SQL查询并返回结果集
    
    Args:
        sql: SQL查询语句（必须是SELECT语句）
        
    Returns:
        包含查询结果的字典
    """
    try:
        print(f"执行SQL查询: {sql[:100]}{'...' if len(sql) > 100 else ''}")
        # 安全检查：确保只执行SELECT语句
        sql_lower = sql.lower().strip()
        if not sql_lower.startswith("select"):
            error_msg = "安全限制：只允许执行SELECT语句"
            print(f"{error_msg}, SQL: {sql}")
            return {
                "error": error_msg,
                "sql": sql
            }
            
        # 检查是否包含危险操作
        dangerous_keywords = ["insert", "update", "delete", "drop", "alter", "create", "truncate", "exec", "execute"]
        for keyword in dangerous_keywords:
            if f" {keyword} " in f" {sql_lower} ":
                error_msg = f"安全限制：查询中包含禁止的关键字 '{keyword}'"
                print(f"{error_msg}, SQL: {sql}")
                return {
                    "error": error_msg,
                    "sql": sql
                }
        
        conn = get_db_connection()
        
        with conn.cursor() as cursor:
            cursor.execute(sql)
            
            # 获取列名
            columns = [col[0] for col in cursor.description] if cursor.description else []
            
            # 获取所有结果
            rows = cursor.fetchall()
            
            # 转换结果为字典列表
            result_rows = []
            for row in rows:
                try:
                    # 创建字典，将列名和值对应
                    row_dict = {}
                    for i, col in enumerate(columns):
                        # 处理特殊类型
                        value = row[i]
                        if isinstance(value, bytes):
                            # 尝试解码 bytes
                            try:
                                value = value.decode('utf-8')
                            except:
                                value = str(value)
                        row_dict[col] = value
                    result_rows.append(row_dict)
                except Exception as row_err:
                    print(f"处理行数据时出错: {row_err}")
                    # 如果出错，添加原始值
                    result_rows.append({"error": str(row_err), "raw_data": str(row)})
        
        print(f"查询成功，返回 {len(result_rows)} 条记录")
        return {
            "columns": columns,
            "rows": result_rows,
            "row_count": len(result_rows)
        }
    except Exception as e:
        error_msg = f"查询执行失败: {str(e)}"
        print(f"{error_msg}, SQL: {sql}")
        return {
            "error": str(e),
            "sql": sql
        }

def get_table_info(table_name: str, schema: Optional[str] = None) -> Dict[str, Any]:
    """获取指定表的结构信息
    
    Args:
        table_name: 表名
        schema: 数据库模式名，默认为 'dbo'
        
    Returns:
        包含表结构信息的字典
    """
    try:
        # 使用默认 schema 如果未指定
        current_schema = schema if schema else 'dbo'
        
        print(f"获取表结构信息: {current_schema}.{table_name}")
        conn = get_db_connection()
        
        # 查询列信息
        columns_sql = f"""
        SELECT 
            COLUMN_NAME AS column_name,
            DATA_TYPE AS data_type,
            CHARACTER_MAXIMUM_LENGTH AS max_length,
            NUMERIC_PRECISION AS precision,
            NUMERIC_SCALE AS scale,
            IS_NULLABLE AS is_nullable,
            COLUMN_DEFAULT AS default_value
        FROM 
            INFORMATION_SCHEMA.COLUMNS
        WHERE 
            TABLE_NAME = '{table_name}' 
            AND TABLE_SCHEMA = '{current_schema}'
        ORDER BY 
            ORDINAL_POSITION
        """

        # 查询主键信息
        primary_keys_sql = f"""
        SELECT 
            cu.COLUMN_NAME AS column_name
        FROM 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE cu 
                ON tc.CONSTRAINT_NAME = cu.CONSTRAINT_NAME
                AND tc.TABLE_SCHEMA = cu.TABLE_SCHEMA
        WHERE 
            tc.TABLE_NAME = '{table_name}' 
            AND tc.TABLE_SCHEMA = '{current_schema}'
            AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
        ORDER BY 
            cu.ORDINAL_POSITION
        """

        # 查询外键信息
        foreign_keys_sql = f"""
        SELECT 
            fk.name AS fk_name,
            COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS column_name,
            OBJECT_NAME(fkc.referenced_object_id) AS referenced_table,
            COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS referenced_column
        FROM 
            sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc 
                ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables t 
                ON fkc.parent_object_id = t.object_id
            INNER JOIN sys.schemas s 
                ON t.schema_id = s.schema_id
        WHERE 
            t.name = '{table_name}' 
            AND s.name = '{current_schema}'
        ORDER BY 
            fk.name, fkc.constraint_column_id
        """

        # 查询索引信息
        indexes_sql = f"""
        SELECT
            i.name AS index_name,
            CASE WHEN i.is_unique = 1 THEN 'UNIQUE' ELSE 'NON_UNIQUE' END AS index_type,
            i.is_unique AS is_unique,
            i.is_primary_key AS is_primary_key,
            i.is_unique_constraint AS is_unique_constraint,
            STUFF((
                SELECT ',' + c.name
                FROM sys.index_columns ic
                JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id
                ORDER BY ic.key_ordinal
                FOR XML PATH('')
            ), 1, 1, '') AS columns
        FROM
            sys.indexes i
            JOIN sys.tables t ON i.object_id = t.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE
            t.name = '{table_name}' 
            AND s.name = '{current_schema}'
            AND i.type > 0
        ORDER BY
            i.name
        """

        # 执行查询并处理结果
        columns = []
        with conn.cursor() as cursor:
            cursor.execute(columns_sql)
            for row in cursor.fetchall():
                column = {
                    "name": row[0],
                    "type": row[1],
                    "max_length": row[2],
                    "precision": row[3],
                    "scale": row[4],
                    "is_nullable": row[5] == "YES",
                    "default_value": row[6]
                }
                columns.append(column)

        # 获取主键
        primary_keys = []
        with conn.cursor() as cursor:
            cursor.execute(primary_keys_sql)
            primary_keys = [row[0] for row in cursor.fetchall()]

        # 获取外键
        foreign_keys = []
        with conn.cursor() as cursor:
            cursor.execute(foreign_keys_sql)
            for row in cursor.fetchall():
                fk = {
                    "name": row[0],
                    "column": row[1],
                    "referenced_table": row[2],
                    "referenced_column": row[3]
                }
                foreign_keys.append(fk)

        # 获取索引
        indexes = []
        with conn.cursor() as cursor:
            cursor.execute(indexes_sql)
            for row in cursor.fetchall():
                index = {
                    "name": row[0],
                    "type": row[1],
                    "is_unique": bool(row[2]),
                    "is_primary_key": bool(row[3]),
                    "is_unique_constraint": bool(row[4]),
                    "columns": row[5].split(",") if row[5] else []
                }
                indexes.append(index)

        return {
            "columns": columns,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys,
            "indexes": indexes
        }
    except Exception as e:
        error_msg = f"获取表结构失败: {str(e)}"
        print(error_msg)
        return {
            "error": str(e)
        }

def list_show_tables(schema: Optional[str] = None) -> Dict[str, Any]:
    """列出数据库中的所有表
    
    Args:
        schema: 数据库模式名，默认为 'dbo'
        
    Returns:
        包含表列表的字典
    """
    try:
        # 使用默认 schema 如果未指定
        current_schema = schema if schema else 'dbo'
        
        print(f"列出数据库模式 '{current_schema}' 中的所有表")
        conn = get_db_connection()
        
        # MSSQL查询表信息
        sql = f"""
        SELECT
            t.name AS table_name,
            CAST(ep.value AS NVARCHAR(255)) AS description,
            s.name AS schema_name
        FROM
            sys.tables t
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            LEFT JOIN sys.extended_properties ep ON ep.major_id = t.object_id 
                AND ep.minor_id = 0 
                AND ep.name = 'MS_Description'
        WHERE
            s.name = '{current_schema}'
        ORDER BY
            t.name
        """
        
        tables = []
        with conn.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor.fetchall():
                table = {
                    "table_name": row[0],
                    "description": row[1] if row[1] else "",
                    "schema_name": row[2]
                }
                tables.append(table)
        
        print(f"成功获取 {len(tables)} 个表")
        return {
            "tables": tables,
            "count": len(tables)
        }
    except Exception as e:
        error_msg = f"列出表失败: {str(e)}"
        print(f"{error_msg}, 模式: {schema if schema else 'dbo'}")
        return {
            "error": str(e),
            "schema": schema if schema else 'dbo'
        }

def get_database_info() -> Dict[str, Any]:
    """获取数据库基本信息
    
    Returns:
        包含数据库信息的字典
    """
    try:
        print("获取数据库基本信息")
        conn = get_db_connection()
        
        info = {}
        
        with conn.cursor() as cursor:
            # 获取数据库版本信息
            cursor.execute("SELECT @@VERSION")
            version_result = cursor.fetchone()
            info["version"] = version_result[0] if version_result else None
            
            # 获取当前数据库名称
            cursor.execute("SELECT DB_NAME()")
            db_name_result = cursor.fetchone()
            info["database_name"] = db_name_result[0] if db_name_result else None
            
            # 获取数据库列表
            cursor.execute("""
                SELECT name 
                FROM sys.databases 
                WHERE state_desc = 'ONLINE'
                ORDER BY name
            """)
            schemas = [row[0] for row in cursor.fetchall()]
            info["schemas"] = schemas
            
            # 获取当前数据库的所有模式
            cursor.execute("""
                SELECT name 
                FROM sys.schemas 
                WHERE schema_id < 16000
                ORDER BY name
            """)
            database_schemas = [row[0] for row in cursor.fetchall()]
            info["database_schemas"] = database_schemas
        
        info["connection"] = {
            "host": config.DB_HOST,
            "port": config.DB_PORT,
            "database": config.DB_NAME,
            "user": config.DB_USER
        }
        
        print(f"成功获取数据库信息: {info['database_name']}")
        return info
    except Exception as e:
        error_msg = f"获取数据库信息失败: {str(e)}"
        print(error_msg)
        return {
            "error": str(e)
        }