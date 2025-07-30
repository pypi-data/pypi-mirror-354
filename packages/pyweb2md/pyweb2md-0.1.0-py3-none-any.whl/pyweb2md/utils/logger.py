"""
简化的日志系统
使用Python标准logging模块，替代原有的复杂logger系统
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    获取logger实例
    
    Args:
        name (str): logger名称
        level (str): 日志级别
        
    Returns:
        logging.Logger: logger实例
    """
    logger = logging.getLogger(f"pyweb2md.{name}")
    
    # 避免重复设置handler
    if logger.handlers:
        return logger
    
    # 设置日志级别
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # 创建handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # 设置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # 添加handler
    logger.addHandler(handler)
    
    return logger


def configure_logging(level: str = "INFO", format_string: Optional[str] = None):
    """
    配置全局日志设置
    
    Args:
        level (str): 全局日志级别
        format_string (str): 自定义格式字符串
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=format_string,
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def disable_logging():
    """禁用日志输出"""
    logging.disable(logging.CRITICAL)


def enable_logging():
    """启用日志输出"""
    logging.disable(logging.NOTSET) 