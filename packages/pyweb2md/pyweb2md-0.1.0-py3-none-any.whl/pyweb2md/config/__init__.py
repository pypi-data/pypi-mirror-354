"""
配置模块
包含默认配置和配置管理
"""

from .defaults import DEFAULT_CONFIG, merge_config

__all__ = [
    "DEFAULT_CONFIG",
    "merge_config"
] 