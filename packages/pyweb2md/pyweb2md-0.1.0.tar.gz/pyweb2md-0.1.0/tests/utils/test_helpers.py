#!/usr/bin/env python3
"""
测试辅助函数

提供通用的测试工具函数，简化测试代码编写。

Author: API2Tool
Created: 2025-06-06
"""

import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import Mock, patch


class TestHelper:
    """通用测试辅助类"""
    
    @staticmethod
    def create_temp_directory() -> Path:
        """创建临时测试目录"""
        temp_dir = Path(tempfile.mkdtemp(prefix="api2tool_test_"))
        return temp_dir
    
    @staticmethod
    def cleanup_temp_directory(temp_dir: Path):
        """清理临时测试目录"""
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    
    @staticmethod
    def wait_for_condition(condition_func, timeout=10, interval=0.1):
        """等待条件满足"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    
    @staticmethod
    def create_mock_config(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建模拟配置"""
        default_config = {
            'browser': 'chrome',
            'headless': True,
            'wait_timeout': 3,
            'timeout': 60,
            'mobile_mode': False,
            'user_agent': None
        }
        
        if overrides:
            default_config.update(overrides)
        
        return default_config
    
    @staticmethod
    def create_mock_scrape_options(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建模拟抓取选项"""
        default_options = {
            'wait_time': 3,
            'extract_links': True,
            'extract_images': False,
            'follow_redirects': True
        }
        
        if overrides:
            default_options.update(overrides)
        
        return default_options
    
    @staticmethod
    def assert_valid_scraping_result(result: Dict[str, Any]):
        """验证抓取结果的基本结构"""
        required_keys = ['url', 'content', 'structured_info', 'metadata']
        for key in required_keys:
            assert key in result, f"抓取结果缺少必需字段: {key}"
        
        # 验证内容不为空
        assert len(result['content']) > 0, "抓取内容不能为空"
        
        # 验证metadata结构
        metadata = result['metadata']
        assert 'success' in metadata, "metadata缺少success字段"
        assert metadata['success'] is True, "抓取应该成功"
    
    @staticmethod
    def assert_valid_navigation_structure(nav_structure: list):
        """验证导航结构的基本格式"""
        assert isinstance(nav_structure, list), "导航结构应该是列表"
        
        if nav_structure:
            nav_item = nav_structure[0]
            required_fields = ['display_name', 'nav_type', 'items']
            for field in required_fields:
                assert field in nav_item, f"导航项缺少必需字段: {field}"


class MockWebDriver:
    """模拟WebDriver用于测试"""
    
    def __init__(self, page_source="<html><body>Test Page</body></html>"):
        self.page_source = page_source
        self.current_url = "https://example.com"
        self.title = "Test Page"
        self._quit_called = False
    
    def get(self, url):
        """模拟访问页面"""
        self.current_url = url
    
    def quit(self):
        """模拟关闭浏览器"""
        self._quit_called = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()


class NetworkMocker:
    """网络请求模拟器"""
    
    def __init__(self):
        self.responses = {}
        self.call_count = {}
    
    def add_response(self, url: str, response_data: Any):
        """添加模拟响应"""
        self.responses[url] = response_data
        self.call_count[url] = 0
    
    def get_response(self, url: str) -> Any:
        """获取模拟响应"""
        if url in self.responses:
            self.call_count[url] += 1
            return self.responses[url]
        raise ValueError(f"No mock response configured for URL: {url}")
    
    def get_call_count(self, url: str) -> int:
        """获取调用次数"""
        return self.call_count.get(url, 0)
    
    def reset(self):
        """重置所有模拟数据"""
        self.responses.clear()
        self.call_count.clear()


def skip_if_no_network():
    """跳过网络依赖的测试装饰器"""
    import socket
    
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            try:
                # 尝试连接到一个公共DNS服务器
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                return test_func(*args, **kwargs)
            except OSError:
                import pytest
                pytest.skip("网络不可用，跳过测试")
        return wrapper
    return decorator


def timeout_test(seconds=30):
    """测试超时装饰器"""
    import signal
    
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(f"测试超时: {test_func.__name__} 超过 {seconds} 秒")
            
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            
            try:
                return test_func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorator 