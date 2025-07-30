"""
PyWeb2MD: 将网页内容转换为Markdown格式的Python包

专为LLM应用优化的智能网页抓取和内容提取工具。
"""

__version__ = "0.1.0"
__author__ = "kian_liu"
__description__ = "Convert web pages to Markdown with intelligent navigation extraction"

from .core.extractor import Web2MD
from .core.converter import HTMLToMarkdownConverter
from .core.batch_scraper import BatchScraper

# 主要API接口
__all__ = [
    "Web2MD",
    "HTMLToMarkdownConverter",
    "BatchScraper"
]

# 便捷的默认接口
def extract(url, **kwargs):
    """
    便捷函数：从URL提取Markdown内容
    
    Args:
        url (str): 要抓取的网页URL
        **kwargs: 其他配置参数
        
    Returns:
        dict: 包含content、navigation、metadata等的结果字典
    """
    extractor = Web2MD(**kwargs)
    return extractor.extract(url) 