# app_config.py
"""
配置模块，用于管理应用程序配置
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类，用于管理应用程序配置"""
    
    # 数据库配置
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "master")
    DB_PORT = os.getenv("DB_PORT", "1433")
    
    # 服务器配置
    SERVER_NAME = os.getenv("SERVER_NAME", "JEWEI-MSSQL-Server")

# 创建默认配置实例
config = Config()