"""
URL处理工具
从原有的WebScraper._get_full_url()函数迁移而来，增强了功能
"""

from urllib.parse import urljoin, urlparse
from typing import Optional
from .logger import get_logger


class URLProcessor:
    """URL处理器类，负责处理各种URL格式化和验证"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        初始化URL处理器
        
        Args:
            base_url (str, optional): 基础URL，用于相对路径解析
        """
        self.base_url = base_url
        self.logger = get_logger("URLProcessor")
    
    def get_full_url(self, href: str, current_url: Optional[str] = None) -> str:
        """
        获取完整URL，添加host部分
        
        这是从原WebScraper._get_full_url()迁移的核心逻辑
        
        Args:
            href (str): 链接地址
            current_url (str, optional): 当前页面URL，优先于base_url使用
            
        Returns:
            str: 完整的URL
        """
        if not href:
            return href
        
        # 如果已经是完整URL，直接返回
        if href.startswith(('http://', 'https://')):
            return href
        
        # 确定要使用的基础URL
        base_to_use = current_url or self.base_url
        
        if base_to_use:
            try:
                # 使用urllib.parse.urljoin处理相对路径
                return urljoin(base_to_use, href)
            except Exception as e:
                self.logger.warning(f"URL拼接失败: {e}, href: {href}, base: {base_to_use}")
        
        # 默认返回原始href
        return href
    
    def validate_url(self, url: str) -> bool:
        """验证URL格式是否有效"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def extract_domain(self, url: str) -> str:
        """从URL中提取域名"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return ""


# 便捷函数
def get_full_url(href: str, base_url: str) -> str:
    """便捷函数：获取完整URL"""
    processor = URLProcessor(base_url)
    return processor.get_full_url(href)


def validate_url(url: str) -> bool:
    """便捷函数：验证URL"""
    processor = URLProcessor()
    return processor.validate_url(url) 