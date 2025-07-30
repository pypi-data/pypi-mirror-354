import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class AppPathSettings(BaseSettings):
    """应用配置"""
    root_path: Optional[str|Path] = Field(Path(__file__).parent, title='项目根路径')
    # 数据存储路径
    data_dir: Optional[str] = Field(os.path.join(root_path, '.data'), title='数据存储路径')
    # 上传路径
    upload_dir: Optional[str] = Field(os.path.join(data_dir, '.upload'), title='上传路径')
    # 日志存储路径
    log_dir: Optional[str] = Field(os.path.join(root_path, '.log'), title='日志存储路径')
    # 临时存储路径
    temp_dir: Optional[str] = Field(os.path.join(root_path, '.temp'), title='临时存储路径')