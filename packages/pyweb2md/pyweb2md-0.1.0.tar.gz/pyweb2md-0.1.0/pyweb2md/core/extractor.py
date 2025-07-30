"""
Web2MD 主要提取器类
这是PyWeb2MD的核心接口类
"""

import time
from datetime import datetime
from typing import Dict, Optional
from ..utils.logger import get_logger
from ..utils.driver_manager import DriverManager
from ..config.defaults import DEFAULT_CONFIG, merge_config
from .navigator import NavigationExtractor
from .converter import HTMLToMarkdownConverter


class Web2MD:
    """
    Web2MD 主要提取器类
    
    这是PyWeb2MD包的主要接口，提供网页到Markdown的转换功能
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化Web2MD提取器
        
        Args:
            config (dict, optional): 配置参数
        """
        self.logger = get_logger("Web2MD")
        self.config = merge_config(config)
        
        # 初始化核心组件
        self.driver_manager = None
        self.navigation_extractor = NavigationExtractor(self.config)
        self.html_converter = HTMLToMarkdownConverter(self.config)
        
        # 导航显示配置
        self.nav_display_config = self.config.get('navigation_display', {
            'mode': 'smart',  # 'full', 'smart', 'current_context', 'minimal', 'toc_only', 'none'
            'max_items_per_nav': 15,
            'max_depth': 3,
            'show_links': True,
            'show_hierarchy': True,
            'include_current_context': True,
            'expand_current_branch': True
        })
        
        self.logger.info("Web2MD提取器初始化完成")
    
    def extract(self, url: str) -> Dict:
        """
        从URL提取Markdown内容
        
        Args:
            url (str): 要抓取的网页URL
            
        Returns:
            dict: 包含content、navigation、metadata等的结果字典
        """
        start_time = time.time()
        self.logger.info(f"开始提取URL: {url}")
        
        try:
            # 初始化驱动管理器
            if not self.driver_manager:
                self.driver_manager = DriverManager(self.config)
            
            # 获取页面内容
            with self.driver_manager.get_driver() as driver:
                # 访问页面
                driver.get(url)
                
                # 智能等待页面加载
                self._smart_wait(driver)
                
                # 获取页面源码和基本信息
                page_source = driver.page_source
                title = driver.title
                current_url = driver.current_url
            
            # 提取导航信息
            navigation_data = self.navigation_extractor.extract_navigation(page_source, current_url)
            
            # 提取并转换内容
            content = self._extract_content(page_source)
            main_markdown = self.html_converter.convert(content, current_url)
            
            # 集成导航信息到最终内容
            markdown_content = self._integrate_navigation_into_content(
                main_markdown, navigation_data, title, current_url
            )
            
            # 构建结果
            processing_time = time.time() - start_time
            
            result = {
                "url": current_url,
                "original_url": url,
                "title": title,
                "content": markdown_content,
                "navigation": navigation_data,
                "metadata": {
                    "extraction_time": datetime.now().isoformat(),
                    "processing_time": round(processing_time, 2),
                    "content_length": len(markdown_content),
                    "success": True
                },
                "images": self._extract_images(page_source, current_url)
            }
            
            self.logger.info(f"URL提取完成: {current_url}, 耗时: {processing_time:.2f}秒")
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"URL提取失败: {url}, 错误: {e}")
        
        return {
            "url": url,
                "original_url": url,
                "title": "",
                "content": "",
                "navigation": {},
            "metadata": {
                    "extraction_time": datetime.now().isoformat(),
                    "processing_time": round(processing_time, 2),
                    "content_length": 0,
                    "success": False,
                    "error": str(e)
            },
            "images": []
        }
    
    def _smart_wait(self, driver, wait_time: int = None):
        """智能等待策略"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException
        
        if wait_time is None:
            wait_time = self.config.get('wait_timeout', 10)
        
        try:
            # 1. 等待DOM加载完成
            WebDriverWait(driver, min(wait_time, 10)).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # 2. 等待主要内容加载
            content_selectors = [
                'main', 'article', '.content', '#content', 
                '.main-content', '.documentation', '.api-docs'
            ]
            
            for selector in content_selectors:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    self.logger.debug(f"找到主要内容容器: {selector}")
                    break
                except TimeoutException:
                    continue
            
            # 3. 额外等待时间
            additional_wait = min(wait_time, 3)
            if additional_wait > 0:
                time.sleep(additional_wait)
                
        except TimeoutException:
            self.logger.warning("智能等待超时，继续处理")
        except Exception as e:
            self.logger.warning(f"智能等待异常: {e}")
    
    def _extract_content(self, page_source: str) -> str:
        """提取页面HTML内容（保留结构用于Markdown转换）"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 移除脚本和样式，但保留HTML结构
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            
            # 查找主要内容区域
            main_content = self._find_main_content_area(soup)
            if main_content:
                # 返回HTML字符串而不是纯文本
                return str(main_content)
            
            # 回退到body内容
            body = soup.find('body')
            if body:
                return str(body)
            
            # 最后回退到整个HTML
            return str(soup)
            
        except ImportError:
            # BeautifulSoup不可用时的回退方案 - 只清理脚本和样式
            import re
            html = re.sub(r'<script[^>]*>.*?</script>', '', page_source, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL | re.IGNORECASE)
            return html.strip()
        except Exception as e:
            self.logger.warning(f"内容提取失败: {e}")
            return ""
    
    def _find_main_content_area(self, soup):
        """查找主要内容区域"""
        main_selectors = [
            'main',
            '[role="main"]',
            '#main',
            '#content',
            '.main-content',
            '.content',
            '.page-content',
            'article',
            '.article'
        ]
        
        for selector in main_selectors:
            main_area = soup.select_one(selector)
            if main_area:
                self.logger.debug(f"找到主内容区域: {selector}")
                return main_area
        
        return None
    
    def _extract_images(self, page_source: str, base_url: str) -> list:
        """提取页面图片信息"""
        images = []
        try:
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin
            
            soup = BeautifulSoup(page_source, 'html.parser')
            
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    # 转换为绝对URL
                    absolute_url = urljoin(base_url, src)
                    images.append({
                        'src': absolute_url,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', '')
                    })
        except Exception as e:
            self.logger.warning(f"图片提取失败: {e}")
        
        return images
    
    def _integrate_navigation_into_content(self, main_content: str, navigation_data: Dict, page_title: str, base_url: str) -> str:
        """
        将导航信息集成到主要内容中，支持多种显示模式
        
        Args:
            main_content (str): 主要的Markdown内容
            navigation_data (Dict): 导航结构数据
            page_title (str): 页面标题
            base_url (str): 基础URL，用于补全相对链接
            
        Returns:
            str: 集成了导航信息的完整Markdown内容
        """
        # 检查是否禁用导航显示
        if self.nav_display_config.get('mode') == 'none':
            return main_content
        
        content_parts = []
        
        # 1. 页面标题（如果主要内容没有以标题开始）
        if main_content and not main_content.strip().startswith('#'):
            if page_title and page_title.strip():
                content_parts.append(f"# {page_title}\n\n")
        
        # 2. 导航概览（如果有导航信息）
        nav_content = self._format_navigation_for_display(navigation_data, base_url)
        if nav_content:
            content_parts.append(nav_content)
            content_parts.append("---\n\n")  # 分隔线
        
        # 3. 面包屑导航（如果有）
        breadcrumb_content = self._format_breadcrumb_for_display(navigation_data.get('breadcrumb', {}), base_url)
        if breadcrumb_content:
            content_parts.append(breadcrumb_content)
            content_parts.append("\n")
        
        # 4. 主要内容
        if main_content:
            content_parts.append(main_content)
        
        return ''.join(content_parts)
    
    def _format_navigation_for_display(self, navigation_data: Dict, base_url: str) -> str:
        """
        格式化导航信息为显示内容（迁移自原始web_scraper的优秀设计）
        支持多种显示模式和完整的链接处理
        """
        if not navigation_data:
            return ""
        
        # 检查是否有任何导航信息（包括TOC）
        has_navigation = navigation_data.get('navigations') or navigation_data.get('toc', {}).get('found')
        if not has_navigation:
            return ""
        
        nav_parts = []
        nav_parts.append("## 🧭 页面导航概览\n\n")
        
        # 处理每个导航（使用原始web_scraper的策略）
        for nav_info in navigation_data.get('navigations', []):
            display_name = nav_info.get('display_name', '未知导航')
            nav_type = nav_info.get('nav_type', 'general')
            items = nav_info.get('items', [])
            current_item = nav_info.get('current_item', {})
            levels = nav_info.get('levels', 1)
            
            # 🔧 修复：使用items本身作为层级结构，因为NavigationExtractor已经提供了正确的层级数据
            # items中每个元素都包含children字段，这就是层级结构
            hierarchical_structure = items
            
            if not items:
                continue
            
            # 导航标题和基本信息（沿用原始设计）
            nav_parts.append(f"### {display_name}\n\n")
            
            # 显示基本统计信息
            items_count = len(items)
            info_parts = []
            if nav_type != 'general_navigation':
                info_parts.append(f"类型: {nav_type}")
            if items_count > 0:
                info_str = f"{items_count} 个项目"
                if levels > 1:
                    info_str += f" ({levels} 层级)"
                info_parts.append(info_str)
            
            if info_parts:
                nav_parts.append(f"**{' | '.join(info_parts)}**\n\n")
            
            # 根据显示模式选择渲染策略
            mode = self.nav_display_config.get('mode', 'smart')
            
            # 🔧 修复：检查是否真的有层级结构
            has_hierarchy = any(item.get('children') for item in items) or levels > 1
            
            if current_item.get('found') and has_hierarchy:
                current_text = current_item.get('text', '')
                nav_parts.append(f"**当前位置**: {current_text}\n\n")
                
                if mode == 'full':
                    # 完整导航：显示所有层级和链接
                    content = self._render_full_navigation(hierarchical_structure, current_item, base_url)
                elif mode == 'current_context':
                    # 当前上下文：只显示当前位置相关的导航路径
                    content = self._render_current_path_context(hierarchical_structure, current_item, base_url)
                else:  # smart (default)
                    # 智能显示：平衡完整性和简洁性
                    content = self._render_navigation_intelligently(hierarchical_structure, current_item, base_url)
                
                if content:
                    nav_parts.append("**层级导航结构**:\n")
                    nav_parts.append(content)
                    nav_parts.append("\n")
            else:
                # 没有当前位置或层级结构，显示概览
                if has_hierarchy:
                    overview_content = self._render_navigation_overview(hierarchical_structure, base_url)
                    nav_parts.append("**主要导航项目** (层级结构):\n")
                else:
                    overview_content = self._render_flat_navigation(items, current_item, base_url)
                    nav_parts.append("**主要导航项目**:\n")
                
                if overview_content:
                    nav_parts.append(overview_content)
                    nav_parts.append("\n")
        
        # 🔧 修复：处理目录信息时，优先使用导航的层级结构而不是独立的TOC
        # 如果已经有了层级导航，就不再单独显示TOC
        has_hierarchical_nav = any(
            any(item.get('children') for item in nav_info.get('items', [])) or nav_info.get('levels', 1) > 1
            for nav_info in navigation_data.get('navigations', [])
        )
        
        if not has_hierarchical_nav:
            # 只有在没有层级导航时才显示独立的TOC
            toc = navigation_data.get('toc', {})
            if toc.get('found') and toc.get('items'):
                nav_parts.append("### 📚 页面目录\n\n")
                
                toc_items = toc.get('items', [])
                max_toc_items = self.nav_display_config.get('max_items_per_nav', 15)
                items_to_show = toc_items[:max_toc_items]
                
                for item in items_to_show:
                    text = self._clean_nav_text(item.get('text', ''))
                    href = item.get('href', '')
                    
                    if text:
                        if href:
                            # 修复：正确处理所有类型的链接，不只是#开头的
                            full_url = self._get_full_url(href, base_url)
                            display_url = self._truncate_url(full_url)
                            nav_parts.append(f"- [{text}]({display_url})\n")
                        else:
                            nav_parts.append(f"- {text}\n")
                
                if len(toc_items) > max_toc_items:
                    remaining = len(toc_items) - max_toc_items
                    nav_parts.append(f"- *... 还有 {remaining} 个目录项*\n")
                
                nav_parts.append("\n")
        
        return ''.join(nav_parts)
    
    # ==================== 导航渲染方法（迁移自原始web_scraper） ====================
    
    def _render_full_navigation(self, hierarchical_structure: list, current_item: Dict, base_url: str) -> str:
        """完整导航：显示所有层级和链接"""
        nav_lines = []
        
        def render_all_items(items, current_depth=0):
            max_depth = self.nav_display_config.get('max_depth', 3)
            if current_depth >= max_depth:
                return
            
            for item in items:
                text = self._clean_nav_text(item.get('text', ''))
                href = item.get('href', '')
                is_current = item.get('is_current', False)
                children = item.get('children', [])
                
                indent = "  " * current_depth
                
                if is_current:
                    nav_lines.append(f"{indent}🎯 **{text}** ← 当前页面\n")
                elif children:
                    children_count = len(children)
                    if href and href not in ['#', 'javascript:void(0)', '']:
                        full_url = self._get_full_url(href, base_url)
                        display_url = self._truncate_url(full_url)
                        nav_lines.append(f"{indent}📁 [{text}]({display_url}) ({children_count} 个子项目)\n")
                    else:
                        nav_lines.append(f"{indent}📁 **{text}** ({children_count} 个子项目)\n")
                else:
                    if href and href not in ['#', 'javascript:void(0)', '']:
                        full_url = self._get_full_url(href, base_url)
                        display_url = self._truncate_url(full_url)
                        nav_lines.append(f"{indent}📄 [{text}]({display_url})\n")
                    else:
                        nav_lines.append(f"{indent}📄 {text}\n")
                
                # 递归处理子项目
                if children and self.nav_display_config.get('show_hierarchy', True):
                    render_all_items(children, current_depth + 1)
        
        render_all_items(hierarchical_structure)
        return ''.join(nav_lines)
    
    def _render_current_path_context(self, hierarchical_structure: list, current_item: Dict, base_url: str) -> str:
        """渲染当前路径的上下文导航（迁移自原始web_scraper）"""
        if not current_item.get('found'):
            return ""
        
        current_text = current_item.get('text', '')
        current_location = self._find_current_location_in_hierarchy(hierarchical_structure, current_text)
        
        if not current_location:
            return ""
        
        return self._render_contextual_navigation(current_location, base_url)
    
    def _render_navigation_intelligently(self, hierarchical_structure: list, current_item: Dict, base_url: str) -> str:
        """智能渲染导航结构（迁移自原始web_scraper）"""
        nav_lines = []
        current_path = self._find_current_path_in_hierarchy(hierarchical_structure, current_item)
        
        def render_items_smart(items, current_depth=0, is_current_branch=False, max_items=None):
            if current_depth >= self.nav_display_config.get('max_depth', 3):
                return
            
            # 动态调整显示数量
            if max_items is None:
                base_max = self.nav_display_config.get('max_items_per_nav', 15)
                if current_depth == 0:
                    max_items = min(8, base_max)  # 顶级最多8个
                elif is_current_branch:
                    max_items = min(10, base_max)  # 当前分支多显示一些
                else:
                    max_items = min(3, base_max)   # 非当前分支少显示
            
            items_to_show = min(len(items), max_items)
            
            for i, item in enumerate(items[:items_to_show]):
                text = item.get('text', '')
                href = item.get('href', '')
                is_current = item.get('is_current', False)
                children = item.get('children', [])
                
                # 检查是否在当前路径上
                item_in_current_path = text in current_path if current_path else False
                
                text = self._clean_nav_text(text)
                indent = "  " * current_depth
                
                # 渲染项目
                if is_current:
                    nav_lines.append(f"{indent}🎯 **{text}** ← 当前页面\n")
                elif item_in_current_path and children:
                    nav_lines.append(f"{indent}📂 **{text}** (当前路径)\n")
                elif children:
                    children_count = len(children)
                    if href and href not in ['#', 'javascript:void(0)', '']:
                        full_url = self._get_full_url(href, base_url)
                        display_url = self._truncate_url(full_url)
                        nav_lines.append(f"{indent}📁 [{text}]({display_url}) ({children_count} 个子项目)\n")
                    else:
                        nav_lines.append(f"{indent}📁 **{text}** ({children_count} 个子项目)\n")
                else:
                    if href and href not in ['#', 'javascript:void(0)', '']:
                        full_url = self._get_full_url(href, base_url)
                        display_url = self._truncate_url(full_url)
                        nav_lines.append(f"{indent}📄 [{text}]({display_url})\n")
                    else:
                        nav_lines.append(f"{indent}📄 {text}\n")
                
                # 决定是否渲染子项目
                should_render_children = False
                if children and current_depth < self.nav_display_config.get('max_depth', 3) - 1:
                    if is_current or item_in_current_path:
                        should_render_children = True
                    elif current_depth == 0 and not current_path:
                        should_render_children = len(children) <= 5
                    elif is_current_branch and current_depth <= 1:
                        should_render_children = True
                
                if should_render_children:
                    render_items_smart(
                        children, 
                        current_depth + 1, 
                        is_current_branch or item_in_current_path,
                        None
                    )
            
            # 显示省略信息
            if len(items) > items_to_show:
                indent = "  " * current_depth
                remaining = len(items) - items_to_show
                nav_lines.append(f"{indent}💭 ... 还有 {remaining} 个项目\n")
        
        render_items_smart(hierarchical_structure, 0, True)
        return ''.join(nav_lines)
    
    def _render_navigation_overview(self, hierarchical_structure: list, base_url: str, max_items: int = 5) -> str:
        """渲染导航概览"""
        nav_lines = []
        items_shown = 0
        
        for item in hierarchical_structure:
            if items_shown >= max_items:
                break
            
            text = self._clean_nav_text(item.get('text', ''))
            href = item.get('href', '')
            children = item.get('children', [])
            
            if children:
                children_count = len(children)
                if href and href not in ['#', 'javascript:void(0)', '']:
                    full_url = self._get_full_url(href, base_url)
                    display_url = self._truncate_url(full_url)
                    nav_lines.append(f"📁 [{text}]({display_url}) ({children_count} 个子项目)\n")
                else:
                    nav_lines.append(f"📁 **{text}** ({children_count} 个子项目)\n")
            else:
                if href and href not in ['#', 'javascript:void(0)', '']:
                    full_url = self._get_full_url(href, base_url)
                    display_url = self._truncate_url(full_url)
                    nav_lines.append(f"📄 [{text}]({display_url})\n")
                else:
                    nav_lines.append(f"📄 {text}\n")
            
            items_shown += 1
        
        if len(hierarchical_structure) > max_items:
            remaining = len(hierarchical_structure) - max_items
            nav_lines.append(f"💭 ... 还有 {remaining} 个项目\n")
        
        return ''.join(nav_lines)
    
    def _render_flat_navigation(self, items: list, current_item: Dict, base_url: str) -> str:
        """渲染扁平导航"""
        nav_lines = []
        current_text = current_item.get('text', '') if current_item.get('found') else ''
        max_items = self.nav_display_config.get('max_items_per_nav', 15)
        
        items_to_show = items[:max_items]
        
        for item in items_to_show:
            text = self._clean_nav_text(item.get('text', ''))
            href = item.get('href', '')
            is_current = item.get('is_current', False)
            
            if is_current:
                nav_lines.append(f"🎯 **{text}** ← 当前页面\n")
            else:
                if href and href not in ['#', 'javascript:void(0)', '']:
                    full_url = self._get_full_url(href, base_url)
                    display_url = self._truncate_url(full_url)
                    nav_lines.append(f"📄 [{text}]({display_url})\n")
                else:
                    nav_lines.append(f"📄 {text}\n")
        
        if len(items) > max_items:
            remaining = len(items) - max_items
            nav_lines.append(f"💭 ... 还有 {remaining} 个项目\n")
        
        return ''.join(nav_lines)
    
    # ==================== 辅助方法（迁移自原始web_scraper） ====================
    
    def _find_current_location_in_hierarchy(self, hierarchical_structure: list, current_text: str) -> Dict:
        """找到当前项目在层次结构中的详细位置信息"""
        def search_recursive(items, target_text, parent_items=None, parent_index=-1, depth=0):
            for i, item in enumerate(items):
                if item.get('text', '') == target_text or item.get('is_current', False):
                    return {
                        'current_item': item,
                        'current_index': i,
                        'siblings': items,
                        'parent_items': parent_items,
                        'parent_index': parent_index,
                        'depth': depth
                    }
                
                if item.get('children'):
                    result = search_recursive(item['children'], target_text, items, i, depth + 1)
                    if result:
                        return result
            return None
        
        return search_recursive(hierarchical_structure, current_text)
    
    def _render_contextual_navigation(self, location_info: Dict, base_url: str) -> str:
        """渲染包含上下文的导航结构"""
        nav_lines = []
        current_item = location_info['current_item']
        current_index = location_info['current_index']
        siblings = location_info['siblings']
        depth = location_info['depth']
        
        if depth > 0:
            nav_lines.append("**导航上下文**:\n")
        else:
            nav_lines.append("**当前层级**:\n")
        
        # 显示当前层级的所有兄弟项目
        for i, sibling in enumerate(siblings):
            sibling_text = self._clean_nav_text(sibling.get('text', ''))
            href = sibling.get('href', '')
            
            if i == current_index:
                nav_lines.append(f"- **【当前】{sibling_text}**\n")
            else:
                if href and href not in ['#', 'javascript:void(0)', '']:
                    full_url = self._get_full_url(href, base_url)
                    display_url = self._truncate_url(full_url)
                    nav_lines.append(f"- [{sibling_text}]({display_url})\n")
                else:
                    nav_lines.append(f"- {sibling_text}\n")
        
        return ''.join(nav_lines)
    
    def _find_current_path_in_hierarchy(self, hierarchical_structure: list, current_item: Dict) -> list:
        """在层次结构中找到当前页面的路径"""
        if not current_item.get('found'):
            return []
        
        current_text = current_item.get('text', '')
        
        def find_path_recursive(items, target_text, current_path):
            for item in items:
                item_path = current_path + [item.get('text', '')]
                
                if item.get('text', '') == target_text or item.get('is_current', False):
                    return item_path
                
                if item.get('children'):
                    result = find_path_recursive(item['children'], target_text, item_path)
                    if result:
                        return result
            return None
        
        result = find_path_recursive(hierarchical_structure, current_text, [])
        return result if result else []
    
    def _get_full_url(self, href: str, base_url: str) -> str:
        """获取完整URL，处理相对链接（迁移自原始web_scraper）"""
        if not href:
            return href
        
        # 如果已经是完整URL，直接返回
        if href.startswith(('http://', 'https://')):
            return href
        
        # 处理相对链接
        try:
            from urllib.parse import urljoin
            return urljoin(base_url, href)
        except Exception:
            # 如果urljoin失败，尝试简单拼接
            if href.startswith('/'):
                from urllib.parse import urlparse
                parsed = urlparse(base_url)
                return f"{parsed.scheme}://{parsed.netloc}{href}"
            else:
                return f"{base_url.rstrip('/')}/{href.lstrip('/')}"
    
    def _truncate_url(self, url: str) -> str:
        """返回完整URL，不进行截断"""
        return url if url else ""
    
    def _clean_nav_text(self, text: str) -> str:
        """清理导航文本，移除多余空白和换行"""
        if not text:
            return ""
        
        # 移除多余的空白和换行符
        text = ' '.join(text.split())
        
        # 截断过长的文本
        if len(text) > 60:
            text = text[:57] + "..."
        
        return text
    
    def _format_breadcrumb_for_display(self, breadcrumb_data: Dict, base_url: str) -> str:
        """格式化面包屑导航为显示内容"""
        if not breadcrumb_data.get('found') or not breadcrumb_data.get('items'):
            return ""
        
        breadcrumb_parts = ["## 🍞 导航路径\n\n"]
        
        items = breadcrumb_data.get('items', [])
        breadcrumb_items = []
        
        for item in items:
            text = self._clean_nav_text(item.get('text', ''))
            href = item.get('href', '')
            
            if text:
                if href and href not in ['#', 'javascript:void(0)', '']:
                    full_url = self._get_full_url(href, base_url)
                    display_url = self._truncate_url(full_url)
                    breadcrumb_items.append(f"[{text}]({display_url})")
                else:
                    breadcrumb_items.append(text)
        
        if breadcrumb_items:
            breadcrumb_parts.append(' > '.join(breadcrumb_items))
            breadcrumb_parts.append("\n\n")
        
        return ''.join(breadcrumb_parts)
    
    def get_content(self, url: str) -> str:
        """
        便捷方法：只获取Markdown内容
        
        Args:
            url (str): 要抓取的网页URL
            
        Returns:
            str: Markdown内容
        """
        result = self.extract(url)
        return result.get("content", "") 
    
    def close(self):
        """关闭资源"""
        if self.driver_manager:
            self.driver_manager.close()
            self.logger.info("Web2MD资源已关闭")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close() 