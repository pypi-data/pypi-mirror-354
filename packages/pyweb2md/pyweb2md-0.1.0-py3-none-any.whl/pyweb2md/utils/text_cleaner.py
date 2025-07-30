"""
文本清理工具
从原有的WebScraper._clean_nav_text()等函数迁移而来，统一处理各种文本清理需求
"""

import re
import unicodedata
from typing import Optional
from .logger import get_logger


class TextCleaner:
    """文本清理器类，提供各种文本清理和格式化功能"""
    
    def __init__(self):
        self.logger = get_logger("TextCleaner")
    
    def clean_nav_text(self, text: str, max_length: int = 60) -> str:
        """
        清理导航文本，移除多余空白和换行
        
        这是从原WebScraper._clean_nav_text()迁移的核心逻辑
        
        Args:
            text (str): 要清理的文本
            max_length (int): 最大长度，超过则截断
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""
        
        # 移除多余的空白和换行符
        text = ' '.join(text.split())
        
        # 截断过长的文本
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
            
        return text
    
    def clean_general_text(self, 
                          text: str,
                          remove_extra_whitespace: bool = True,
                          remove_html: bool = False,
                          normalize_unicode: bool = True) -> str:
        """
        通用文本清理功能
        
        Args:
            text (str): 要清理的文本
            remove_extra_whitespace (bool): 是否移除多余空白
            remove_html (bool): 是否移除HTML标签
            normalize_unicode (bool): 是否规范化Unicode字符
            
        Returns:
            str: 清理后的文本
        """
        if not isinstance(text, str):
            return str(text)
        
        # 规范化Unicode字符
        if normalize_unicode:
            text = unicodedata.normalize('NFKC', text)
        
        # 移除HTML标签
        if remove_html:
            text = re.sub(r'<[^>]+>', '', text)
        
        # 移除多余的空白字符
        if remove_extra_whitespace:
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
        
        return text
    
    def clean_content_text(self, text: str) -> str:
        """
        清理正文内容
        
        Args:
            text (str): 要清理的正文
            
        Returns:
            str: 清理后的正文
        """
        if not text:
            return ""
        
        # 移除控制字符
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # 规范化空白字符
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def clean_markdown_text(self, content: str) -> str:
        """
        从Markdown内容中提取纯文本
        
        Args:
            content (str): Markdown内容
            
        Returns:
            str: 提取的纯文本
        """
        if not content:
            return ""
        
        text = content
        
        # 移除代码块
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'^    .+$', '', text, flags=re.MULTILINE)
        
        # 移除标题语法
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # 移除链接和图片语法
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # 移除列表语法
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        
        # 移除引用语法
        text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
        
        # 移除粗体和斜体语法
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # 移除行内代码
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        return self.clean_general_text(text)
    
    def truncate_url(self, url: str, max_length: int = 80) -> str:
        """
        截断过长的URL以便显示
        
        这是从原WebScraper._truncate_url()迁移的逻辑
        
        Args:
            url (str): 要截断的URL
            max_length (int): 最大长度
            
        Returns:
            str: 截断后的URL
        """
        if not url:
            return ""
        
        # 如果URL太长，截断中间部分
        if len(url) > max_length:
            # 保留开头和结尾
            keep_each = (max_length - 3) // 2  # 3是"..."的长度
            start = url[:keep_each]
            end = url[-keep_each:]
            return f"{start}...{end}"
        
        return url
    
    def extract_urls(self, content: str) -> list:
        """
        从文本中提取URL
        
        Args:
            content (str): 包含URL的文本
            
        Returns:
            list: 提取的URL列表
        """
        # URL正则模式
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+'
        
        urls = []
        for match in re.finditer(url_pattern, content):
            url = match.group(0)
            urls.append({
                'url': url,
                'type': 'https' if url.startswith('https') else 'http' if url.startswith('http') else 'www',
                'position': match.start(),
                'length': len(url)
            })
        
        return urls
    
    def extract_emails(self, content: str) -> list:
        """
        从文本中提取邮箱地址
        
        Args:
            content (str): 包含邮箱的文本
            
        Returns:
            list: 提取的邮箱列表
        """
        # 邮箱正则模式
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        emails = []
        for match in re.finditer(email_pattern, content):
            email = match.group(0)
            emails.append({
                'email': email,
                'domain': email.split('@')[1] if '@' in email else '',
                'position': match.start(),
                'length': len(email)
            })
        
        return emails


# 便捷函数
def clean_nav_text(text: str, max_length: int = 60) -> str:
    """便捷函数：清理导航文本"""
    cleaner = TextCleaner()
    return cleaner.clean_nav_text(text, max_length)


def clean_text(text: str, **kwargs) -> str:
    """便捷函数：通用文本清理"""
    cleaner = TextCleaner()
    return cleaner.clean_general_text(text, **kwargs)


def truncate_url(url: str, max_length: int = 80) -> str:
    """便捷函数：截断URL"""
    cleaner = TextCleaner()
    return cleaner.truncate_url(url, max_length) 