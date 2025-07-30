import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """数据库配置"""
    db_host: Optional[str] = Field(os.getenv("DB_HOST", "127.0.0.1"), title='数据库主机')
    db_port: Optional[int] = Field(os.getenv("DB_PORT", 5432), title='数据库端口')
    db_name: Optional[str] = Field(os.getenv("DB_NAME", "test-db"), title='数据库名称')
    db_user: Optional[str] = Field(os.getenv("DB_USER", "root"), title='数据库用户名')
    db_password: Optional[str] = Field(os.getenv("DB_PASSWORD", "123456"), title='数据库密码')

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def db_async_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
