import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Union, Dict, Any, List
import os
from io import StringIO
import sqlite3
import glob

class CSV2SQL:
    """CSV 到 SQL 转换器类"""
    
    def __init__(self):
        self.supported_db_types = {
            'mysql': 'mysql',
            'postgresql': 'postgresql',
            'sqlite': 'sqlite',
            'oracle': 'oracle',
            'mssql': 'mssql+pyodbc'
        }
    
    def _get_sql_type(self, dtype: str, db_type: str) -> str:
        """根据数据类型和数据库类型返回对应的 SQL 类型"""
        type_mapping = {
            'mysql': {
                'int64': 'BIGINT',
                'int32': 'INT',
                'float64': 'DOUBLE',
                'float32': 'FLOAT',
                'object': 'TEXT',
                'datetime64[ns]': 'DATETIME',
                'bool': 'BOOLEAN'
            },
            'postgresql': {
                'int64': 'BIGINT',
                'int32': 'INTEGER',
                'float64': 'DOUBLE PRECISION',
                'float32': 'REAL',
                'object': 'TEXT',
                'datetime64[ns]': 'TIMESTAMP',
                'bool': 'BOOLEAN'
            },
            'sqlite': {
                'int64': 'INTEGER',
                'int32': 'INTEGER',
                'float64': 'REAL',
                'float32': 'REAL',
                'object': 'TEXT',
                'datetime64[ns]': 'TEXT',
                'bool': 'INTEGER'
            },
            'oracle': {
                'int64': 'NUMBER(19)',
                'int32': 'NUMBER(10)',
                'float64': 'BINARY_DOUBLE',
                'float32': 'BINARY_FLOAT',
                'object': 'CLOB',
                'datetime64[ns]': 'TIMESTAMP',
                'bool': 'NUMBER(1)'
            },
            'mssql': {
                'int64': 'BIGINT',
                'int32': 'INT',
                'float64': 'FLOAT',
                'float32': 'REAL',
                'object': 'NVARCHAR(MAX)',
                'datetime64[ns]': 'DATETIME2',
                'bool': 'BIT'
            }
        }
        
        return type_mapping[db_type].get(str(dtype), 'TEXT')
    
    def _generate_create_table(self, df: pd.DataFrame, table_name: str, 
                             db_type: str, charset: Optional[str] = None) -> str:
        """生成建表语句"""
        columns = []
        for col_name, dtype in df.dtypes.items():
            sql_type = self._get_sql_type(dtype, db_type)
            columns.append(f"`{col_name}` {sql_type}")
        
        create_table = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
        create_table += ",\n".join(f"    {col}" for col in columns)
        create_table += "\n)"
        
        if charset and db_type in ['mysql', 'postgresql']:
            create_table += f" CHARACTER SET {charset}"
        
        return create_table + ";"
    
    def _generate_insert_statements(self, df: pd.DataFrame, table_name: str) -> str:
        """生成插入语句"""
        columns = df.columns.tolist()
        values = []
        
        for _, row in df.iterrows():
            row_values = []
            for val in row:
                if pd.isna(val):
                    row_values.append('NULL')
                elif isinstance(val, (int, float)):
                    row_values.append(str(val))
                else:
                    escaped_val = str(val).replace("'", "''")
                    row_values.append(f"'{escaped_val}'")
            values.append(f"({', '.join(row_values)})")
        
        if not values:
            return ""
        
        insert = f"INSERT INTO `{table_name}` (`{'`, `'.join(columns)}`) VALUES\n"
        insert += ",\n".join(values) + ";"
        return insert
    
    def convert_file(self, input_file: str, output_file: str, 
                    db_type: str = 'mysql', table_name: Optional[str] = None,
                    charset: Optional[str] = None) -> None:
        """转换 CSV 文件到 SQL 文件或数据库"""
        if db_type not in self.supported_db_types:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        if not table_name:
            table_name = os.path.splitext(os.path.basename(input_file))[0]
        
        df = pd.read_csv(input_file)
        
        if db_type == 'sqlite':
            # 创建 SQLite 数据库
            conn = sqlite3.connect(output_file)
            cursor = conn.cursor()
            
            # 创建表
            create_table = self._generate_create_table(df, table_name, db_type)
            cursor.execute(create_table)
            
            # 插入数据
            for _, row in df.iterrows():
                placeholders = ','.join(['?' for _ in row])
                columns = ','.join([f'`{col}`' for col in df.columns])
                sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(row))
            
            conn.commit()
            conn.close()
        else:
            # 生成 SQL 文件
            create_table = self._generate_create_table(df, table_name, db_type, charset)
            insert_statements = self._generate_insert_statements(df, table_name)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(create_table + "\n\n")
                f.write(insert_statements)
    
    def convert_string(self, csv_content: str, db_type: str = 'mysql',
                      table_name: str = 'table_name', 
                      charset: Optional[str] = None) -> str:
        """转换 CSV 字符串到 SQL 字符串"""
        if db_type not in self.supported_db_types:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        df = pd.read_csv(StringIO(csv_content))
        
        create_table = self._generate_create_table(df, table_name, db_type, charset)
        insert_statements = self._generate_insert_statements(df, table_name)
        
        return f"{create_table}\n\n{insert_statements}"

    def convert_multiple_files(self, input_files: Union[str, List[str]], 
                             output_file: str,
                             db_type: str = 'mysql',
                             table_name_pattern: Optional[str] = None,
                             charset: Optional[str] = None) -> None:
        """转换多个 CSV 文件到数据库
        
        Args:
            input_files: CSV 文件路径或文件路径列表，支持通配符（如 '*.csv'）
            output_file: 输出文件路径
            db_type: 数据库类型
            table_name_pattern: 表名模式，如果为 None 则使用文件名作为表名
            charset: 字符集
        """
        if isinstance(input_files, str):
            # 如果输入是字符串，可能是单个文件或通配符
            if '*' in input_files or '?' in input_files:
                input_files = glob.glob(input_files)
            else:
                input_files = [input_files]
        
        if not input_files:
            raise ValueError("没有找到匹配的 CSV 文件")
        
        if db_type == 'sqlite':
            # 创建 SQLite 数据库连接
            conn = sqlite3.connect(output_file)
            cursor = conn.cursor()
            
            try:
                for input_file in input_files:
                    # 获取表名
                    if table_name_pattern:
                        table_name = table_name_pattern.format(
                            filename=os.path.splitext(os.path.basename(input_file))[0]
                        )
                    else:
                        table_name = os.path.splitext(os.path.basename(input_file))[0]
                    
                    # 读取 CSV 文件
                    df = pd.read_csv(input_file)
                    
                    # 创建表
                    create_table = self._generate_create_table(df, table_name, db_type)
                    cursor.execute(create_table)
                    
                    # 插入数据
                    for _, row in df.iterrows():
                        placeholders = ','.join(['?' for _ in row])
                        columns = ','.join([f'`{col}`' for col in df.columns])
                        sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                        cursor.execute(sql, tuple(row))
                    
                    print(f"已导入文件: {input_file} -> 表: {table_name}")
                
                conn.commit()
            finally:
                conn.close()
        else:
            # 对于其他数据库类型，生成 SQL 文件
            with open(output_file, 'w', encoding='utf-8') as f:
                for input_file in input_files:
                    # 获取表名
                    if table_name_pattern:
                        table_name = table_name_pattern.format(
                            filename=os.path.splitext(os.path.basename(input_file))[0]
                        )
                    else:
                        table_name = os.path.splitext(os.path.basename(input_file))[0]
                    
                    # 读取 CSV 文件
                    df = pd.read_csv(input_file)
                    
                    # 生成 SQL
                    create_table = self._generate_create_table(df, table_name, db_type, charset)
                    insert_statements = self._generate_insert_statements(df, table_name)
                    
                    # 写入文件
                    f.write(f"-- 文件: {input_file}\n")
                    f.write(f"-- 表名: {table_name}\n")
                    f.write(create_table + "\n\n")
                    f.write(insert_statements + "\n\n")
                    
                    print(f"已处理文件: {input_file} -> 表: {table_name}")
