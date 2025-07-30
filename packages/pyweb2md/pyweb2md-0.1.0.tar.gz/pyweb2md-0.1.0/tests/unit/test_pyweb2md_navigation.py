#!/usr/bin/env python3
"""
PyWeb2MD 导航功能单元测试

测试pyweb2md包中导航提取和层级结构处理的各个功能点。
严格遵循项目测试管理规范。

测试范围：
- NavigationExtractor 导航提取功能
- 层级结构分析
- 智能导航命名
- URL处理和链接完整性
- HTMLToMarkdownConverter 转换功能
- ContentExtractor 内容整合功能

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
from bs4 import BeautifulSoup

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pyweb2md.core.navigator import NavigationExtractor
from pyweb2md.core.converter import HTMLToMarkdownConverter
from pyweb2md.core.extractor import Web2MD
from pyweb2md.config.defaults import DEFAULT_CONFIG
from pyweb2md.utils.logger import get_logger


class TestNavigationExtractor(unittest.TestCase):
    """NavigationExtractor 核心功能测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.logger = get_logger(cls.__name__)
        cls.config = DEFAULT_CONFIG.copy()
        
    def setUp(self):
        """每个测试方法的初始化"""
        self.extractor = NavigationExtractor(self.config)
        
    def test_initialization(self):
        """测试NavigationExtractor初始化"""
        self.assertIsNotNone(self.extractor)
        self.assertIsNotNone(self.extractor.config)
        self.assertIsNotNone(self.extractor.logger)
        self.assertIsNotNone(self.extractor.text_cleaner)
    
    def test_simple_navigation_extraction(self):
        """测试简单导航结构提取"""
        test_html = """
        <nav class="main-nav">
            <ul>
                <li><a href="/home">首页</a></li>
                <li><a href="/products" class="current">产品</a></li>
                <li><a href="/about">关于我们</a></li>
            </ul>
        </nav>
        """
        
        result = self.extractor.extract_navigation(test_html)
        
        # 验证基本结构
        self.assertIn('navigation_count', result)
        self.assertIn('navigations', result)
        self.assertGreater(result['navigation_count'], 0)
        
        # 验证导航项目
        if result['navigations']:
            nav = result['navigations'][0]
            self.assertIn('items', nav)
            self.assertIn('display_name', nav)
            self.assertGreater(len(nav['items']), 0)
            
            # 验证链接项目结构
            for item in nav['items']:
                self.assertIn('text', item)
                self.assertIn('href', item)
                self.assertIn('is_current', item)
    
    def test_hierarchical_navigation_extraction(self):
        """测试层级导航结构提取"""
        test_html = """
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
        """
        
        result = self.extractor.extract_navigation(test_html)
        
        self.assertGreater(result['navigation_count'], 0)
        
        if result['navigations']:
            nav = result['navigations'][0]
            
            # 验证层级数
            self.assertGreater(nav.get('levels', 1), 1, "应该检测到多层级结构")
            
            # 验证层级项目结构
            items = nav.get('items', [])
            hierarchical_items = [item for item in items if item.get('children')]
            self.assertGreater(len(hierarchical_items), 0, "应该有包含子项目的项目")
            
            # 验证子项目结构
            parent_item = hierarchical_items[0]
            children = parent_item.get('children', [])
            self.assertGreater(len(children), 0, "父项目应该包含子项目")
            
            # 验证子项目字段
            for child in children:
                self.assertIn('text', child)
                self.assertIn('href', child)
                self.assertIn('level', child)
                self.assertGreater(child['level'], 1)
    
    def test_current_page_detection(self):
        """测试当前页面检测功能"""
        test_html = """
        <nav>
            <ul>
                <li><a href="/page1">Page 1</a></li>
                <li><a href="/page2" class="current">Page 2</a></li>
                <li><a href="/page3" aria-current="page">Page 3</a></li>
            </ul>
        </nav>
        """
        
        result = self.extractor.extract_navigation(test_html)
        
        if result['navigations']:
            nav = result['navigations'][0]
            items = nav.get('items', [])
            
            current_items = [item for item in items if item.get('is_current')]
            self.assertGreater(len(current_items), 0, "应该检测到当前页面标记")
            
            # 验证当前页面检测方式
            current_item = current_items[0]
            self.assertTrue(current_item['is_current'])
    
    def test_smart_navigation_naming(self):
        """测试智能导航命名功能"""
        test_html = """
        <nav class="documentation-nav" aria-label="Documentation Navigation">
            <ul>
                <li><a href="/docs">Docs Home</a></li>
            </ul>
        </nav>
        """
        
        result = self.extractor.extract_navigation(test_html)
        
        if result['navigations']:
            nav = result['navigations'][0]
            display_name = nav.get('display_name', '')
            
            # 应该使用智能命名，而不是通用的"导航区域"
            self.assertNotEqual(display_name, '导航区域')
            self.assertTrue(len(display_name) > 0)
    
    def test_empty_navigation_handling(self):
        """测试空导航处理"""
        test_html = """
        <div>
            <p>没有导航的页面内容</p>
        </div>
        """
        
        result = self.extractor.extract_navigation(test_html)
        
        self.assertEqual(result['navigation_count'], 0)
        self.assertEqual(len(result['navigations']), 0)
    
    def test_malformed_html_handling(self):
        """测试错误HTML处理"""
        test_html = """
        <nav>
            <ul>
                <li><a href="/test">Test</a>
                <!-- 未闭合的标签 -->
            </ul>
        </nav>
        """
        
        # 应该不抛出异常
        try:
            result = self.extractor.extract_navigation(test_html)
            self.assertIsInstance(result, dict)
        except Exception as e:
            self.fail(f"处理错误HTML时不应该抛出异常: {e}")


class TestHTMLToMarkdownConverter(unittest.TestCase):
    """HTMLToMarkdownConverter 转换功能测试"""
    
    def setUp(self):
        """每个测试方法的初始化"""
        self.converter = HTMLToMarkdownConverter()
    
    def test_basic_html_conversion(self):
        """测试基本HTML转换"""
        test_html = """
        <h1>标题</h1>
        <p>段落内容</p>
        <ul>
            <li>列表项1</li>
            <li>列表项2</li>
        </ul>
        """
        
        result = self.converter.convert(test_html)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        # 验证Markdown格式
        self.assertIn('#', result)  # 标题
        self.assertIn('-', result)  # 列表
    
    def test_link_conversion(self):
        """测试链接转换"""
        test_html = '<a href="https://example.com">示例链接</a>'
        
        result = self.converter.convert(test_html)
        
        self.assertIn('[示例链接]', result)
        self.assertIn('(https://example.com)', result)
    
    def test_image_conversion(self):
        """测试图片转换"""
        test_html = '<img src="image.jpg" alt="测试图片" title="图片标题">'
        
        result = self.converter.convert(test_html)
        
        self.assertIn('![测试图片]', result)
        self.assertIn('image.jpg', result)


class TestWeb2MD(unittest.TestCase):
    """Web2MD 内容整合功能测试"""
    
    def setUp(self):
        """每个测试方法的初始化"""
        self.extractor = Web2MD(DEFAULT_CONFIG)
    
    def test_initialization(self):
        """测试Web2MD初始化"""
        self.assertIsNotNone(self.extractor)
        self.assertIsNotNone(self.extractor.config)
    
    def test_navigation_integration(self):
        """测试导航信息整合功能"""
        main_content = "# 测试页面\n\n这是主要内容。"
        
        navigation_data = {
            'navigation_count': 1,
            'navigations': [
                {
                    'display_name': '🔗 测试导航',
                    'nav_type': 'main',
                    'items': [
                        {'text': '首页', 'href': '/home', 'is_current': False, 'children': []},
                        {'text': '当前页', 'href': '/current', 'is_current': True, 'children': []}
                    ],
                    'levels': 1,
                    'current_item': {'found': True, 'text': '当前页'}
                }
            ]
        }
        
        result = self.extractor._integrate_navigation_into_content(
            main_content, navigation_data, '测试页面', 'https://example.com'
        )
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(main_content))
        
        # 验证导航信息已整合
        self.assertIn('页面导航概览', result)
        self.assertIn('测试导航', result)
        self.assertIn('当前页面', result)
    
    def test_hierarchical_navigation_display(self):
        """测试层级导航显示"""
        navigation_data = {
            'navigation_count': 1,
            'navigations': [
                {
                    'display_name': '🔗 层级导航',
                    'nav_type': 'main',
                    'items': [
                        {
                            'text': '父项目',
                            'href': '/parent',
                            'is_current': False,
                            'children': [
                                {'text': '子项目1', 'href': '/child1', 'is_current': False, 'level': 2},
                                {'text': '子项目2', 'href': '/child2', 'is_current': True, 'level': 2}
                            ]
                        }
                    ],
                    'levels': 2,
                    'current_item': {'found': True, 'text': '子项目2'}
                }
            ]
        }
        
        result = self.extractor._integrate_navigation_into_content(
            '', navigation_data, '测试页面', 'https://example.com'
        )
        
        # 验证层级结构显示
        self.assertIn('层级导航结构', result)
        self.assertIn('📂', result)  # 文件夹图标（实际使用的是📂）
        self.assertIn('  ', result)  # 缩进
    
    def test_url_truncation_disabled(self):
        """测试URL截断功能已禁用"""
        long_url = "https://example.com/very/long/path/with/many/segments/that/would/normally/be/truncated"
        
        result = self.extractor._truncate_url(long_url)
        
        # 验证URL没有被截断
        self.assertEqual(result, long_url)
        self.assertNotIn('...', result)


class TestNavigationIntegration(unittest.TestCase):
    """导航功能集成测试"""
    
    def setUp(self):
        """每个测试方法的初始化"""
        self.nav_extractor = NavigationExtractor(DEFAULT_CONFIG)
        self.content_extractor = Web2MD(DEFAULT_CONFIG)
        self.converter = HTMLToMarkdownConverter()
    
    def test_end_to_end_navigation_processing(self):
        """测试端到端导航处理流程"""
        test_html = """
        <html>
        <head><title>测试页面</title></head>
        <body>
            <nav class="main-nav">
                <ul>
                    <li><a href="/home">首页</a></li>
                    <li><a href="/docs" class="current">文档</a>
                        <ul>
                            <li><a href="/docs/api">API</a></li>
                            <li><a href="/docs/guide">指南</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
            <main>
                <h1>文档页面</h1>
                <p>这是文档内容。</p>
            </main>
        </body>
        </html>
        """
        
        # 1. 提取导航
        nav_result = self.nav_extractor.extract_navigation(test_html)
        
        # 2. 转换主要内容
        soup = BeautifulSoup(test_html, 'html.parser')
        main_element = soup.find('main')
        main_content = self.converter.convert(str(main_element)) if main_element else ""
        
        # 3. 整合导航和内容
        final_content = self.content_extractor._integrate_navigation_into_content(
            main_content, nav_result, '测试页面', 'https://example.com'
        )
        
        # 验证完整流程
        self.assertIsInstance(final_content, str)
        self.assertGreater(len(final_content), 0)
        
        # 验证包含所有预期元素
        self.assertIn('文档页面', final_content)  # 主要内容
        self.assertIn('页面导航概览', final_content)  # 导航概览
        self.assertIn('当前页面', final_content)  # 当前页面标记
        self.assertIn('层级', final_content)  # 层级结构
    
    def test_navigation_consistency(self):
        """测试导航数据一致性"""
        test_html = """
        <nav>
            <ul>
                <li><a href="/page1">Page 1</a></li>
                <li><a href="/page2" class="active">Page 2</a></li>
            </ul>
        </nav>
        """
        
        result = self.nav_extractor.extract_navigation(test_html)
        
        # 验证数据一致性
        self.assertEqual(len(result['navigations']), result['navigation_count'])
        
        if result['navigations']:
            nav = result['navigations'][0]
            
            # 验证项目统计一致性
            actual_items = len(nav['items'])
            self.assertGreater(actual_items, 0)
            
            # 验证当前页面检测一致性
            current_items = [item for item in nav['items'] if item.get('is_current')]
            if current_items:
                self.assertTrue(nav.get('current_item', {}).get('found', False))


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def setUp(self):
        """每个测试方法的初始化"""
        self.extractor = NavigationExtractor(DEFAULT_CONFIG)
    
    def test_invalid_html_handling(self):
        """测试无效HTML处理"""
        invalid_html = "这不是HTML内容"
        
        try:
            result = self.extractor.extract_navigation(invalid_html)
            self.assertIsInstance(result, dict)
            self.assertEqual(result.get('navigation_count', 0), 0)
        except Exception as e:
            self.fail(f"处理无效HTML时不应该抛出异常: {e}")
    
    def test_empty_input_handling(self):
        """测试空输入处理"""
        empty_inputs = ["", None, "<html></html>"]
        
        for empty_input in empty_inputs:
            with self.subTest(input=empty_input):
                try:
                    result = self.extractor.extract_navigation(empty_input)
                    self.assertIsInstance(result, dict)
                except Exception as e:
                    self.fail(f"处理空输入 '{empty_input}' 时不应该抛出异常: {e}")


def run_navigation_tests():
    """运行所有导航相关测试"""
    # 设置日志
    logging.basicConfig(
        level=logging.WARNING,  # 减少测试时的日志输出
        format='%(levelname)s: %(message)s'
    )
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestNavigationExtractor,
        TestHTMLToMarkdownConverter,
        TestWeb2MD,
        TestNavigationIntegration,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("🧪 PyWeb2MD 导航功能单元测试")
    print("=" * 60)
    print("🎯 测试范围: NavigationExtractor, Web2MD, HTMLToMarkdownConverter")
    print("🎯 测试重点: 层级结构提取, 智能命名, URL处理, 内容整合")
    print("🎯 严格遵循: API2Tool 测试管理规范")
    print("=" * 60)
    
    success = run_navigation_tests()
    
    print("=" * 60)
    if success:
        print("🎉 所有测试通过！")
        exit(0)
    else:
        print("❌ 部分测试失败，请检查输出")
        exit(1) 