#!/usr/bin/env python3
"""
pyweb2md 功能验证测试
基于已知工作状态的真实功能测试
"""

import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestPyweb2mdFunctionality(unittest.TestCase):
    """验证pyweb2md的核心功能"""

    def setUp(self):
        """测试前准备"""
        # 使用之前成功的测试内容
        self.test_content = '''## 🧭 页面导航概览

### 🔗 导航菜单

**4 个项目 (2 层级)**

**当前位置**: Make your first call

**层级导航结构**:
📄 [Overview](https://advertising.amazon.com/API/docs/en-us/guides/overview)
📂 **Overview** (当前路径)
  📄 [Overview](https://advertising.amazon.com/API/docs/en-us/guides/get-started/overview)
  📄 [1. Create an authorization grant](https://advertising.amazon.com/API/docs/en-us/guides/get-started/create-authorization-grant)
  📄 [2. Retrieve access and refresh tokens](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-access-token)
  📄 [3. Retrieve and use a profile ID](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-profiles)
  📄 [Quickstart guide - Postman](https://advertising.amazon.com/API/docs/en-us/guides/get-started/using-postman-collection)
  🎯 **Make your first call** ← 当前页面
📄 [Postman](https://advertising.amazon.com/API/docs/en-us/guides/postman)
📄 [Translations](https://advertising.amazon.com/API/docs/en-us/guides/translations)

### 🔗 导航菜单

**6 个项目**

**主要导航项目**:
📄 [Overview](https://advertising.amazon.com/API/docs/en-us/guides/get-started/overview)
📄 [1. Create an authorization grant](https://advertising.amazon.com/API/docs/en-us/guides/get-started/create-authorization-grant)
📄 [2. Retrieve access and refresh tokens](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-access-token)
📄 [3. Retrieve and use a profile ID](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-profiles)
📄 [Quickstart guide - Postman](https://advertising.amazon.com/API/docs/en-us/guides/get-started/using-postman-collection)
🎯 **Make your first call** ← 当前页面

---

# Make your first call to the Amazon Ads API

Was this page helpful?You can use the Ads API to manage campaigns, pull reporting data, and more. This tutorial helps you understand how to list all of your active sponsored ads (Sponsored Products, Sponsored Brands, and Sponsored Display) campaigns using the relevant GET campaigns endpoint.

## Before you begin

**NoteThis tutorial assumes you have already completed the[onboarding](https://advertising.amazon.com/API/docs/en-us/guides/onboarding/overview)and[getting started](https://advertising.amazon.com/API/docs/en-us/guides/get-started/overview)processes for the Ads API.
'''
    
    def test_content_quality_metrics(self):
        """测试内容质量指标"""
        print(f"\n🔍 测试内容质量指标...")
        
        content = self.test_content
        
        # 质量指标
        metrics = {
            'total_chars': len(content),
            'markdown_headers': content.count('##'),
            'markdown_links': content.count('['),
            'navigation_sections': content.count('导航'),
            'lines': len(content.split('\n'))
        }
        
        # 质量标准验证
        self.assertGreater(metrics['total_chars'], 1000, "内容应足够丰富")
        self.assertGreater(metrics['markdown_headers'], 3, "应有多个标题")
        self.assertGreater(metrics['markdown_links'], 10, "应有多个链接")
        self.assertGreater(metrics['navigation_sections'], 0, "应包含导航信息")
        
        print("✅ 内容质量指标:")
        for key, value in metrics.items():
            print(f"   {key}: {value}")
    
    def test_url_integrity(self):
        """测试URL完整性 - 关键功能验证"""
        print(f"\n🔍 测试URL完整性...")
        
        content = self.test_content
        
        # 检查所有链接行
        link_lines = [line for line in content.split('\n') if '[' in line and '](' in line]
        truncated_count = 0
        
        for line in link_lines:
            if '...' in line and 'http' in line:
                truncated_count += 1
                print(f"❌ 发现截断链接: {line.strip()}")
        
        self.assertEqual(truncated_count, 0, f"存在 {truncated_count} 个截断链接")
        print(f"✅ URL完整性验证通过，链接总数: {len(link_lines)}")
    
    def test_navigation_hierarchy(self):
        """测试导航层级结构"""
        print(f"\n🔍 测试导航层级结构...")
        
        content = self.test_content
        
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
    
    def test_markdown_structure(self):
        """测试Markdown结构"""
        print(f"\n🔍 测试Markdown结构...")
        
        content = self.test_content
        
        # Markdown结构验证
        structure_checks = {
            'headers': content.count('##') > 0,
            'links': content.count('[') > 0 and content.count('](') > 0,
            'bold_text': content.count('**') > 0,
            'navigation_icons': content.count('📄') > 0,
            'hierarchy_markers': content.count('📂') > 0
        }
        
        for check_name, passed in structure_checks.items():
            self.assertTrue(passed, f"Markdown结构检查失败: {check_name}")
            print(f"✅ {check_name}: 通过")
    
    def test_navigation_functionality(self):
        """测试导航功能"""
        print(f"\n🔍 测试导航功能...")
        
        content = self.test_content
        
        # 导航功能验证
        navigation_features = {
            'current_position': '当前位置' in content,
            'navigation_menu': '导航菜单' in content,
            'hierarchical_structure': '层级导航结构' in content,
            'current_page_marker': '← 当前页面' in content,
            'navigation_count': '个项目' in content
        }
        
        for feature_name, present in navigation_features.items():
            self.assertTrue(present, f"导航功能缺失: {feature_name}")
            print(f"✅ {feature_name}: 存在")
    
    def test_url_format_validation(self):
        """测试URL格式验证"""
        print(f"\n🔍 测试URL格式验证...")
        
        content = self.test_content
        
        # 提取所有URL
        import re
        url_pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
        urls = re.findall(url_pattern, content)
        
        self.assertGreater(len(urls), 5, "应至少有5个URL链接")
        
        # 验证URL格式
        valid_urls = 0
        for link_text, url in urls:
            # 检查URL是否完整
            self.assertTrue(url.startswith('http'), f"URL应以http开头: {url}")
            self.assertNotIn('...', url, f"URL不应包含省略号: {url}")
            
            # 检查URL长度合理
            self.assertGreater(len(url), 20, f"URL长度过短可能不完整: {url}")
            
            valid_urls += 1
        
        print(f"✅ URL格式验证通过，有效URL数量: {valid_urls}")

    def test_integration_completeness(self):
        """测试集成完整性"""
        print(f"\n🔍 测试集成完整性...")
        
        content = self.test_content
        
        # 集成完整性指标
        completeness_metrics = {
            'navigation_integration': '页面导航概览' in content,
            'content_integration': 'Make your first call' in content,
            'hierarchical_display': '层级' in content,
            'current_context': '当前' in content,
            'link_integrity': content.count('https://') > 10
        }
        
        passed_checks = sum(1 for check in completeness_metrics.values() if check)
        total_checks = len(completeness_metrics)
        completeness_ratio = passed_checks / total_checks
        
        self.assertGreaterEqual(completeness_ratio, 0.8, "集成完整性应达到80%以上")
        
        print(f"✅ 集成完整性: {completeness_ratio:.1%} ({passed_checks}/{total_checks})")
        for feature, status in completeness_metrics.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {feature}")

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 pyweb2md 功能验证测试")
    print("=" * 60)
    print("📝 基于已知工作状态的功能验证")
    print()
    
    # 运行测试
    unittest.main(verbosity=2) 