import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from feng_tools.base.config.AppInfoSetting import AppInfoSetting
from feng_tools.base.config.AppPathSettings import AppPathSettings
from feng_tools.base.config.DatabaseSettings import DatabaseSettings


class AppSettings(AppInfoSetting, DatabaseSettings, AppPathSettings):
    """应用配置"""
    root_path: Optional[str | Path] = Field(Path(__file__).parent, title='项目根路径')
    # env配置文件
    env_file: Optional[str | Path] = Field(os.path.join(root_path, ".env"), title='env配置文件')
    # 静态资源路径
    static_dir: Optional[str] = Field(os.path.join(root_path, 'resource', 'static'), title='静态资源路径')
    # 模板文件路径
    templates_dir: Optional[str] = Field(os.path.join(root_path, 'resource', 'templates'), title='模板文件路径')

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding='utf-8',
        # 其他配置...
    )