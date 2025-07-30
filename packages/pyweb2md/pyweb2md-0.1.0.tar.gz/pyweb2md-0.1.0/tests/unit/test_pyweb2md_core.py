#!/usr/bin/env python3
"""
PyWeb2MD 核心功能单元测试

测试pyweb2md包的核心extract方法和相关功能。
专注于层级结构修复后的功能验证。

测试范围：
- extract() 核心API
- 层级结构提取和显示
- URL处理完整性
- 导航数据一致性
- 错误处理和边界情况

Author: API2Tool Test Team  
Created: 2025-06-11
Version: 1.0.0
"""

import sys
import os
import unittest
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
import re

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pyweb2md import extract


class TestExtractAPI(unittest.TestCase):
    """extract() 核心API测试"""
    
    def test_extract_function_exists(self):
        """测试extract函数是否存在且可调用"""
        self.assertTrue(callable(extract))
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_extract_basic_structure(self, mock_driver_manager):
        """测试extract返回的基本数据结构"""
        # Mock设置
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <nav><ul><li><a href="/test">Test Link</a></li></ul></nav>
                <main><h1>Test Content</h1><p>Test paragraph.</p></main>
            </body>
        </html>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        # 执行测试
        result = extract("https://example.com/test")
        
        # 验证返回结构
        self.assertIsInstance(result, dict)
        
        # 验证必要字段
        required_fields = ['url', 'title', 'content', 'navigation', 'metadata']
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, result, f"结果应包含 {field} 字段")
        
        # 验证metadata结构
        metadata = result.get('metadata', {})
        self.assertIn('success', metadata)
        self.assertIn('extraction_time', metadata)
        self.assertIn('processing_time', metadata)
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_extract_navigation_structure(self, mock_driver_manager):
        """测试extract的导航结构提取"""
        # Mock层级导航页面
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <html>
            <head><title>Navigation Test</title></head>
            <body>
                <nav class="sidebar">
                    <ul>
                        <li><a href="/overview">Overview</a>
                            <ul>
                                <li><a href="/overview/intro">Introduction</a></li>
                                <li><a href="/overview/start" class="current">Getting Started</a></li>
                                <li><a href="/overview/guide">User Guide</a></li>
                            </ul>
                        </li>
                        <li><a href="/api">API Reference</a></li>
                    </ul>
                </nav>
                <main><h1>Getting Started</h1></main>
            </body>
        </html>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/overview/start")
        
        # 验证导航数据结构
        navigation = result.get('navigation', {})
        self.assertIn('navigation_count', navigation)
        self.assertIn('navigations', navigation)
        
        # 验证层级结构
        if navigation.get('navigations'):
            nav = navigation['navigations'][0]
            self.assertIn('levels', nav)
            self.assertIn('items', nav)
            
            # 验证层级数大于1
            levels = nav.get('levels', 1)
            self.assertGreater(levels, 1, "应该检测到多层级结构")
            
            # 验证层级项目
            items = nav.get('items', [])
            hierarchical_items = [item for item in items if item.get('children')]
            self.assertGreater(len(hierarchical_items), 0, "应该有包含子项目的项目")
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_extract_content_integration(self, mock_driver_manager):
        """测试extract的内容和导航整合"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <html>
            <head><title>Integration Test</title></head>
            <body>
                <nav>
                    <ul>
                        <li><a href="/home">Home</a></li>
                        <li><a href="/current" class="active">Current Page</a></li>
                    </ul>
                </nav>
                <main>
                    <h1>Current Page</h1>
                    <p>This is the main content.</p>
                </main>
            </body>
        </html>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/current")
        
        # 验证内容整合
        content = result.get('content', '') or result.get('markdown', '')
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        
        # 验证导航信息已整合到内容中
        self.assertIn('页面导航概览', content)
        self.assertIn('当前页面', content)
    
    def test_extract_error_handling(self):
        """测试extract的错误处理"""
        # 测试无效URL
        with self.assertRaises(Exception):
            extract("not-a-valid-url")
        
        # 测试空URL
        with self.assertRaises(Exception):
            extract("")


class TestHierarchicalStructure(unittest.TestCase):
    """层级结构处理测试"""
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_hierarchy_detection(self, mock_driver_manager):
        """测试层级结构检测"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <nav>
            <ul>
                <li><a href="/level1">Level 1</a>
                    <ul>
                        <li><a href="/level1/level2a">Level 2A</a>
                            <ul>
                                <li><a href="/level1/level2a/level3">Level 3</a></li>
                            </ul>
                        </li>
                        <li><a href="/level1/level2b">Level 2B</a></li>
                    </ul>
                </li>
            </ul>
        </nav>
        <main><h1>Test</h1></main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/test")
        
        content = result.get('content', '') or result.get('markdown', '')
        
        # 验证层级结构在内容中的体现
        lines = content.split('\n')
        indented_lines = [line for line in lines if line.startswith('  ') and ('📁' in line or '📄' in line)]
        
        self.assertGreater(len(indented_lines), 0, "应该有缩进的层级结构显示")
        
        # 验证不同层级的缩进
        indent_levels = set()
        for line in indented_lines:
            indent_count = (len(line) - len(line.lstrip())) // 2
            indent_levels.add(indent_count)
        
        self.assertGreater(len(indent_levels), 1, "应该有多个不同的缩进层级")
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_hierarchy_display_format(self, mock_driver_manager):
        """测试层级结构显示格式"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <nav>
            <ul>
                <li><a href="/parent">Parent Item</a>
                    <ul>
                        <li><a href="/child1">Child Item 1</a></li>
                        <li><a href="/child2" class="current">Child Item 2</a></li>
                    </ul>
                </li>
            </ul>
        </nav>
        <main><h1>Child Item 2</h1></main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/child2")
        
        content = result.get('content', '') or result.get('markdown', '')
        
        # 验证层级结构格式
        self.assertIn('层级导航结构', content)
        self.assertIn('📁', content)  # 文件夹图标
        self.assertIn('📄', content)  # 文件图标
        self.assertIn('🎯', content)  # 当前页面标记
        
        # 验证当前页面标记格式
        self.assertIn('← 当前页面', content)


class TestURLIntegrity(unittest.TestCase):
    """URL完整性测试"""
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_no_url_truncation(self, mock_driver_manager):
        """测试URL不被截断"""
        long_url = "https://advertising.amazon.com/API/docs/en-us/guides/get-started/create-authorization-grant"
        
        mock_driver = MagicMock()
        mock_driver.page_source = f"""
        <nav>
            <ul>
                <li><a href="{long_url}">Very Long URL Link</a></li>
                <li><a href="/short">Short Link</a></li>
            </ul>
        </nav>
        <main><h1>Test</h1></main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/test")
        
        content = result.get('content', '') or result.get('markdown', '')
        
        # 验证长URL没有被截断
        self.assertIn(long_url, content, "长URL应该保持完整")
        self.assertNotIn('...', content, "不应该有省略号")
        
        # 统计截断链接数量
        truncated_count = content.count('...)')
        self.assertEqual(truncated_count, 0, "不应该有任何截断的链接")
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_absolute_url_conversion(self, mock_driver_manager):
        """测试相对URL转换为绝对URL"""
        base_url = "https://example.com/docs/api"
        
        mock_driver = MagicMock()
        mock_driver.current_url = base_url
        mock_driver.page_source = """
        <nav>
            <ul>
                <li><a href="/home">Absolute Path</a></li>
                <li><a href="./relative">Relative Path</a></li>
                <li><a href="../parent">Parent Path</a></li>
                <li><a href="https://external.com">External URL</a></li>
            </ul>
        </nav>
        <main><h1>Test</h1></main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract(base_url)
        
        content = result.get('content', '') or result.get('markdown', '')
        
        # 验证所有链接都是完整的URL格式
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for link_text, link_url in links:
            if not link_url.startswith('#'):  # 忽略锚点链接
                self.assertTrue(
                    link_url.startswith('http://') or link_url.startswith('https://'),
                    f"链接 '{link_url}' 应该是完整的URL"
                )


class TestNavigationConsistency(unittest.TestCase):
    """导航数据一致性测试"""
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_navigation_data_consistency(self, mock_driver_manager):
        """测试导航数据内部一致性"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <nav>
            <ul>
                <li><a href="/page1">Page 1</a></li>
                <li><a href="/page2" class="current">Page 2</a></li>
                <li><a href="/page3">Page 3</a></li>
            </ul>
        </nav>
        <main><h1>Page 2</h1></main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/page2")
        
        navigation = result.get('navigation', {})
        
        # 验证导航计数一致性
        nav_count = navigation.get('navigation_count', 0)
        navigations = navigation.get('navigations', [])
        self.assertEqual(len(navigations), nav_count, "导航数量统计应该一致")
        
        # 验证当前页面检测一致性
        if navigations:
            nav = navigations[0]
            items = nav.get('items', [])
            current_items = [item for item in items if item.get('is_current')]
            
            current_location = navigation.get('current_location', {})
            if current_items:
                self.assertTrue(current_location.get('found', False), "当前位置应该被正确检测")
            
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_content_navigation_sync(self, mock_driver_manager):
        """测试内容和导航信息同步"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <nav>
            <ul>
                <li><a href="/section1">Section 1</a></li>
                <li><a href="/section2" class="active">Section 2</a></li>
            </ul>
        </nav>
        <main>
            <h1>Section 2 Content</h1>
            <p>This is section 2.</p>
        </main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/section2")
        
        # 验证标题和导航的一致性
        title = result.get('title', '')
        content = result.get('content', '') or result.get('markdown', '')
        navigation = result.get('navigation', {})
        
        # 内容中应该包含当前页面标记
        self.assertIn('当前页面', content)
        
        # 导航数据中应该有当前页面信息
        current_location = navigation.get('current_location', {})
        self.assertTrue(current_location.get('found', False))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_no_navigation_page(self, mock_driver_manager):
        """测试没有导航的页面"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <html>
            <head><title>No Navigation Page</title></head>
            <body>
                <main>
                    <h1>Content Only</h1>
                    <p>This page has no navigation.</p>
                </main>
            </body>
        </html>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/no-nav")
        
        # 应该能正常处理
        self.assertIsInstance(result, dict)
        
        navigation = result.get('navigation', {})
        self.assertEqual(navigation.get('navigation_count', 0), 0)
        
        content = result.get('content', '') or result.get('markdown', '')
        self.assertGreater(len(content), 0)
    
    @patch('pyweb2md.utils.driver_manager.DriverManager')
    def test_single_level_navigation(self, mock_driver_manager):
        """测试单层级导航"""
        mock_driver = MagicMock()
        mock_driver.page_source = """
        <nav>
            <ul>
                <li><a href="/item1">Item 1</a></li>
                <li><a href="/item2">Item 2</a></li>
                <li><a href="/item3">Item 3</a></li>
            </ul>
        </nav>
        <main><h1>Flat Navigation Test</h1></main>
        """
        mock_driver_manager.return_value.__enter__.return_value.get_driver.return_value.__enter__.return_value = mock_driver
        
        result = extract("https://example.com/flat")
        
        # 应该能正常处理单层级导航
        navigation = result.get('navigation', {})
        self.assertGreater(navigation.get('navigation_count', 0), 0)
        
        if navigation.get('navigations'):
            nav = navigation['navigations'][0]
            levels = nav.get('levels', 1)
            self.assertEqual(levels, 1, "应该正确识别为单层级")


def run_core_tests():
    """运行所有核心功能测试"""
    # 设置日志
    logging.basicConfig(
        level=logging.WARNING,
        format='%(levelname)s: %(message)s'
    )
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestExtractAPI,
        TestHierarchicalStructure,
        TestURLIntegrity,
        TestNavigationConsistency,
        TestEdgeCases
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("🧪 PyWeb2MD 核心功能单元测试")
    print("=" * 60)
    print("🎯 测试范围: extract() API, 层级结构, URL完整性, 数据一致性")
    print("🎯 测试重点: 层级结构修复后的功能验证")
    print("🎯 严格遵循: API2Tool 测试管理规范")
    print("=" * 60)
    
    success = run_core_tests()
    
    print("=" * 60)
    if success:
        print("🎉 所有测试通过！")
        exit(0)
    else:
        print("❌ 部分测试失败，请检查输出")
        exit(1) 