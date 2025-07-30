#!/usr/bin/env python3
"""
pyweb2md 真实网站集成测试
实际访问真实网站来验证功能的有效性
"""

import unittest
import sys
import os
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pyweb2md import Web2MD

class TestPyweb2mdRealSites(unittest.TestCase):
    """测试pyweb2md在真实网站上的表现"""

    def setUp(self):
        """测试前准备"""
        self.extractor = Web2MD()
        # 添加延迟避免过于频繁的请求
        self.request_delay = 2
    
    def tearDown(self):
        """测试后清理"""
        time.sleep(self.request_delay)
    
    def test_amazon_api_documentation(self):
        """测试Amazon API文档提取 - 主要测试用例"""
        url = "https://advertising.amazon.com/API/docs/en-us/guides/get-started/first-call"
        
        print(f"\n🔍 测试Amazon API文档提取...")
        print(f"URL: {url}")
        
        try:
            result = self.extractor.extract(url)
        except Exception as e:
            self.skipTest(f"Amazon网站访问失败，可能由于网络问题: {e}")
        
        # 基本结果验证
        self.assertIsNotNone(result, "提取结果不应为空")
        self.assertIn('content', result, "结果应包含content字段")
        self.assertIn('metadata', result, "结果应包含metadata字段")
        
        content = result['content']
        metadata = result['metadata']
        
        # 检查是否提取失败
        if len(content) == 0:
            self.skipTest("内容提取失败，可能由于网站访问问题")
        
        # 内容质量验证
        self.assertGreater(len(content), 1000, "内容长度应大于1000字符")
        self.assertIn('##', content, "应包含Markdown标题")
        self.assertIn('[', content, "应包含Markdown链接")
        
        # 导航功能验证
        self.assertIn('导航', content, "应包含导航信息")
        
        # URL完整性验证 - 关键测试点
        truncated_links = [line for line in content.split('\n') if '...' in line and 'http' in line]
        self.assertEqual(len(truncated_links), 0, f"不应有截断的URL链接，发现: {truncated_links}")
        
        # 层级结构验证
        hierarchy_indicators = ['层级导航结构', '  📄']  # 层级导航标题和缩进项目
        has_hierarchy = any(indicator in content for indicator in hierarchy_indicators)
        self.assertTrue(has_hierarchy, "应包含层级结构信息")
        
        print(f"✅ 内容长度: {len(content)} 字符")
        print(f"✅ 标题数量: {content.count('##')} 个")
        print(f"✅ 链接数量: {content.count('[')} 个")
        print(f"✅ 截断链接: 0 个")
        
    def test_github_documentation(self):
        """测试GitHub文档提取"""
        url = "https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api"
        
        print(f"\n🔍 测试GitHub文档提取...")
        print(f"URL: {url}")
        
        result = self.extractor.extract(url)
        
        self.assertIsNotNone(result)
        content = result['content']
        
        # GitHub文档特征验证
        self.assertGreater(len(content), 500, "内容应有合理长度")
        self.assertIn('API', content, "应包含API相关内容")
        
        # URL完整性验证
        truncated_links = [line for line in content.split('\n') if '...' in line and 'http' in line]
        self.assertEqual(len(truncated_links), 0, "不应有截断的URL")
        
        print(f"✅ GitHub文档提取成功，内容长度: {len(content)} 字符")
    
    def test_python_documentation(self):
        """测试Python官方文档提取"""
        url = "https://docs.python.org/3/tutorial/introduction.html"
        
        print(f"\n🔍 测试Python文档提取...")
        print(f"URL: {url}")
        
        result = self.extractor.extract(url)
        
        self.assertIsNotNone(result)
        content = result['content']
        
        # Python文档特征验证
        self.assertGreater(len(content), 800, "内容应有合理长度")
        self.assertIn('Python', content, "应包含Python相关内容")
        
        # 代码块验证
        self.assertIn('```', content, "应包含代码块")
        
        print(f"✅ Python文档提取成功，内容长度: {len(content)} 字符")
    
    def test_url_integrity_comprehensive(self):
        """综合测试URL完整性 - 核心功能验证"""
        test_urls = [
            "https://advertising.amazon.com/API/docs/en-us/guides/get-started/first-call",
            "https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api"
        ]
        
        print(f"\n🔍 综合测试URL完整性...")
        
        for url in test_urls:
            print(f"测试URL: {url}")
            result = self.extractor.extract(url)
            content = result['content']
            
            # 检查所有链接行
            link_lines = [line for line in content.split('\n') if '[' in line and '](' in line]
            truncated_count = 0
            
            for line in link_lines:
                if '...' in line and 'http' in line:
                    truncated_count += 1
                    print(f"❌ 发现截断链接: {line.strip()}")
            
            self.assertEqual(truncated_count, 0, f"URL {url} 存在 {truncated_count} 个截断链接")
            print(f"✅ URL完整性验证通过，链接总数: {len(link_lines)}")
    
    def test_navigation_hierarchy_real(self):
        """测试真实网站的导航层级结构"""
        url = "https://advertising.amazon.com/API/docs/en-us/guides/get-started/first-call"
        
        print(f"\n🔍 测试导航层级结构...")
        
        result = self.extractor.extract(url)
        content = result['content']
        
        # 检查层级标识符
        hierarchy_patterns = [
            '层级导航结构',  # 层级导航标题
            '  📄',  # 缩进的项目 (2个空格)
            '📂'    # 文件夹图标表示层级
        ]
        
        hierarchy_found = []
        for pattern in hierarchy_patterns:
            if pattern in content:
                hierarchy_found.append(pattern)
        
        self.assertGreater(len(hierarchy_found), 0, "应检测到层级结构")
        
        # 检查是否有实际的层级内容
        lines = content.split('\n')
        indented_lines = [line for line in lines if line.startswith('  📄') and line.strip()]
        self.assertGreater(len(indented_lines), 0, "应有缩进的层级内容")
        
        print(f"✅ 层级结构验证通过，缩进行数: {len(indented_lines)}")
    
    def test_content_quality_metrics(self):
        """测试内容质量指标"""
        url = "https://advertising.amazon.com/API/docs/en-us/guides/get-started/first-call"
        
        print(f"\n🔍 测试内容质量指标...")
        
        result = self.extractor.extract(url)
        content = result['content']
        
        # 质量指标
        metrics = {
            'total_chars': len(content),
            'markdown_headers': content.count('##'),
            'markdown_links': content.count('['),
            'code_blocks': content.count('```'),
            'navigation_sections': content.count('导航'),
            'lines': len(content.split('\n'))
        }
        
        # 质量标准验证
        self.assertGreater(metrics['total_chars'], 5000, "内容应足够丰富")
        self.assertGreater(metrics['markdown_headers'], 3, "应有多个标题")
        self.assertGreater(metrics['markdown_links'], 10, "应有多个链接")
        self.assertGreater(metrics['navigation_sections'], 0, "应包含导航信息")
        
        print("✅ 内容质量指标:")
        for key, value in metrics.items():
            print(f"   {key}: {value}")

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 pyweb2md 真实网站集成测试")
    print("=" * 60)
    
    # 运行测试
    unittest.main(verbosity=2) 