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
    
    # 测试配置
    BASE_URL = os.getenv("BASE_URL", "")

    
    OPEN_API_DOC_JSON_URL = os.getenv("OPEN_API_DOC_JSON_URL", "")
    
    # 服务器配置
    SERVER_NAME = os.getenv("SERVER_NAME", "OpenAPI2MCP-Server")
    
    # 连接字符串
    @property
    def CONNECTION_STRING(self):
        """Returns the base URL as a connection string."""
        """构建字符串"""
        return f"{self.BASE_URL}"

# 创建默认配置实例
config = Config()