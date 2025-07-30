"""
Web2MD - 主要的网页到Markdown转换器
整合所有核心模块提供完整的转换功能
"""

import time
from typing import Dict, Optional, Union
from ..utils.logger import get_logger
from ..utils.driver_manager import DriverManager
from ..config.defaults import DEFAULT_CONFIG, merge_config
from .extractor import ContentExtractor
from .converter import HTMLToMarkdownConverter
from .navigator import NavigationExtractor
# TokenCounter模块已移除


class Web2MD:
    """主要的Web2MD转换器类"""
    
    def __init__(self, config: Optional[dict] = None):
        """
        初始化Web2MD转换器
        
        Args:
            config (dict, optional): 用户配置，会与默认配置合并
        """
        self.logger = get_logger("Web2MD")
        self.config = merge_config(config)
        
        # 初始化核心组件
        self.driver_manager = DriverManager(self.config)
        self.content_extractor = ContentExtractor(self.config)
        self.html_converter = HTMLToMarkdownConverter(self.config)
        self.navigation_extractor = NavigationExtractor(self.config)
        # token_counter已移除
        
        self.logger.info("Web2MD转换器初始化完成")
    
    def convert_url(self, url: str, include_navigation: bool = True, 
                   include_metadata: bool = True) -> Dict:
        """
        转换URL为Markdown
        
        Args:
            url (str): 要转换的URL
            include_navigation (bool): 是否包含导航信息
            include_metadata (bool): 是否包含元数据
            
        Returns:
            dict: 转换结果
        """
        try:
            self.logger.info(f"开始转换URL: {url}")
            start_time = time.time()
            
            # 获取页面源码
            page_source = self._fetch_page_source(url)
            if not page_source:
                return self._error_result("无法获取页面内容", url)
            
            # 提取内容
            content_result = self.content_extractor.extract(page_source, url)
            
            # 转换为Markdown
            markdown_content = self.html_converter.convert(content_result.get('content', ''))
            
            # 构建基本结果
            result = {
                'success': True,
                'url': url,
                'title': content_result.get('title', ''),
                'markdown': markdown_content,
                'content_length': len(markdown_content),
                'processing_time': round(time.time() - start_time, 2)
            }
            
            # 添加导航信息
            if include_navigation:
                navigation_data = self.navigation_extractor.extract_navigation(page_source, url)
                result['navigation'] = navigation_data
            
            # 添加元数据
            if include_metadata:
                result['metadata'] = {
                    'description': content_result.get('description', ''),
                    'keywords': content_result.get('keywords', []),
                    'author': content_result.get('author', ''),
                    'published_date': content_result.get('published_date', ''),
                    'word_count': self._count_words(markdown_content),
                    # 'token_count': token_count功能已移除,
                    'extraction_stats': content_result.get('stats', {})
                }
            
            self.logger.info(f"URL转换完成: {result['processing_time']}秒")
            return result
            
        except Exception as e:
            self.logger.error(f"URL转换失败: {e}")
            return self._error_result(str(e), url)
    
    def convert_html(self, html_content: str, base_url: str = "", 
                    include_navigation: bool = True) -> Dict:
        """
        转换HTML内容为Markdown
        
        Args:
            html_content (str): HTML内容
            base_url (str): 基础URL
            include_navigation (bool): 是否包含导航信息
            
        Returns:
            dict: 转换结果
        """
        try:
            self.logger.info("开始转换HTML内容")
            start_time = time.time()
            
            if not html_content:
                return self._error_result("HTML内容为空", base_url)
            
            # 提取内容
            content_result = self.content_extractor.extract(html_content, base_url)
            
            # 转换为Markdown
            markdown_content = self.html_converter.convert(content_result.get('content', ''))
            
            # 构建结果
            result = {
                'success': True,
                'base_url': base_url,
                'title': content_result.get('title', ''),
                'markdown': markdown_content,
                'content_length': len(markdown_content),
                'processing_time': round(time.time() - start_time, 2)
            }
            
            # 添加导航信息
            if include_navigation:
                navigation_data = self.navigation_extractor.extract_navigation(html_content, base_url)
                result['navigation'] = navigation_data
            
            self.logger.info(f"HTML转换完成: {result['processing_time']}秒")
            return result
            
        except Exception as e:
            self.logger.error(f"HTML转换失败: {e}")
            return self._error_result(str(e), base_url)
    
    def extract_navigation_only(self, source: Union[str, str], base_url: str = "") -> Dict:
        """
        仅提取导航信息
        
        Args:
            source (str): URL或HTML内容
            base_url (str): 基础URL（当source为HTML时）
            
        Returns:
            dict: 导航信息
        """
        try:
            self.logger.info("开始提取导航信息")
            
            # 判断是URL还是HTML内容
            if source.startswith(('http://', 'https://')):
                # 是URL
                page_source = self._fetch_page_source(source)
                if not page_source:
                    return {'success': False, 'error': '无法获取页面内容'}
                
                navigation_data = self.navigation_extractor.extract_navigation(page_source, source)
                navigation_data['success'] = True
                navigation_data['url'] = source
            else:
                # 是HTML内容
                navigation_data = self.navigation_extractor.extract_navigation(source, base_url)
                navigation_data['success'] = True
                navigation_data['base_url'] = base_url
            
            return navigation_data
            
        except Exception as e:
            self.logger.error(f"导航提取失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_content_stats(self, content: str) -> Dict:
        """
        获取内容统计信息
        
        Args:
            content (str): 内容文本
            
        Returns:
            dict: 统计信息
        """
        return {
            'character_count': len(content),
            'word_count': self._count_words(content),
            'line_count': content.count('\n') + 1,
            # 'token_count': token_count功能已移除,
            'estimated_reading_time': self._estimate_reading_time(content)
        }
    
    def _fetch_page_source(self, url: str) -> Optional[str]:
        """获取页面源码"""
        try:
            with self.driver_manager.get_driver() as driver:
                self.logger.info(f"访问页面: {url}")
                driver.get(url)
                
                # 等待页面加载
                time.sleep(self.config['browser']['page_load_timeout'])
                
                return driver.page_source
                
        except Exception as e:
            self.logger.error(f"获取页面源码失败: {e}")
            return None
    
    def _error_result(self, error_message: str, url: str = "") -> Dict:
        """生成错误结果"""
        return {
            'success': False,
            'error': error_message,
            'url': url,
            'markdown': '',
            'processing_time': 0
        }
    
    def _count_words(self, text: str) -> int:
        """计算词数"""
        if not text:
            return 0
        
        # 简单的词数统计
        words = text.split()
        return len(words)
    
    def _estimate_reading_time(self, text: str) -> int:
        """估算阅读时间（分钟）"""
        word_count = self._count_words(text)
        # 假设每分钟阅读200词
        reading_time = max(1, round(word_count / 200))
        return reading_time
    
    def close(self):
        """关闭资源"""
        self.driver_manager.close()
        self.logger.info("Web2MD转换器已关闭")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# 便捷函数
def convert_url_to_markdown(url: str, config: Optional[dict] = None) -> Dict:
    """
    便捷函数：将URL转换为Markdown
    
    Args:
        url (str): 要转换的URL
        config (dict, optional): 配置参数
        
    Returns:
        dict: 转换结果
    """
    with Web2MD(config) as converter:
        return converter.convert_url(url)


def convert_html_to_markdown(html_content: str, base_url: str = "", 
                           config: Optional[dict] = None) -> Dict:
    """
    便捷函数：将HTML转换为Markdown
    
    Args:
        html_content (str): HTML内容
        base_url (str): 基础URL
        config (dict, optional): 配置参数
        
    Returns:
        dict: 转换结果
    """
    with Web2MD(config) as converter:
        return converter.convert_html(html_content, base_url)


def extract_navigation(source: str, base_url: str = "", 
                      config: Optional[dict] = None) -> Dict:
    """
    便捷函数：提取导航信息
    
    Args:
        source (str): URL或HTML内容
        base_url (str): 基础URL
        config (dict, optional): 配置参数
        
    Returns:
        dict: 导航信息
    """
    with Web2MD(config) as converter:
        return converter.extract_navigation_only(source, base_url) 