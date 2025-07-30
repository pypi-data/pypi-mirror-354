"""
导航提取器 - PyWeb2MD的核心算法
负责智能提取和分析网页导航结构
"""

from typing import Dict, List, Optional
from ..utils.logger import get_logger
from ..utils.text_cleaner import TextCleaner

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class NavigationExtractor:
    """导航提取器 - 智能分析网页导航结构"""
    
    def __init__(self, config: Optional[dict] = None):
        """初始化导航提取器"""
        self.logger = get_logger("NavigationExtractor")
        self.config = config or {}
        self.text_cleaner = TextCleaner()
    
    def extract_navigation(self, page_source: str, base_url: str = "") -> Dict:
        """
        提取页面导航结构
        
        Args:
            page_source (str): 页面源码
            base_url (str): 基础URL
            
        Returns:
            dict: 导航结构数据
        """
        if not page_source or not BS4_AVAILABLE:
            return self._empty_result()
        
        try:
            self.logger.info("开始分析页面导航结构")
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 查找所有导航元素
            navigations = self._find_all_navigations(soup)
            
            # 分析每个导航
            navigation_data = []
            for nav in navigations:
                nav_info = self._analyze_navigation(nav)
                if nav_info:
                    navigation_data.append(nav_info)
            
            result = {
                "navigation_count": len(navigation_data),
                "navigations": navigation_data,
                "current_location": self._find_current_location(navigation_data),
                "breadcrumb": self._extract_breadcrumb(soup),
                "toc": self._extract_toc(soup)
            }
            
            self.logger.info(f"导航分析完成，找到 {len(navigation_data)} 个导航")
            return result
            
        except Exception as e:
            self.logger.error(f"导航提取失败: {e}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict:
        """返回空结果"""
        return {
            "navigation_count": 0,
            "navigations": [],
            "current_location": {"found": False},
            "breadcrumb": {"found": False, "items": []},
            "toc": {"found": False, "items": []}
        }
    
    def _find_all_navigations(self, soup) -> List:
        """查找所有导航元素"""
        nav_selectors = [
            'nav',
            '.navigation',
            '.nav', 
            '.navbar',
            '.menu',
            '.main-menu',
            '.docs-nav',
            '.api-nav',
            '.sidebar',
            '[role="navigation"]'
        ]
        
        found_navs = []
        
        # 首先查找传统的导航元素
        for selector in nav_selectors:
            try:
                navs = soup.select(selector)
                for nav in navs:
                    if nav not in found_navs and self._is_valid_navigation(nav):
                        found_navs.append(nav)
            except Exception:
                continue
        
        # 如果没有找到传统导航，查找可能的导航结构
        if not found_navs:
            # 查找嵌套的ul结构，这通常是导航
            all_uls = soup.find_all('ul')
            for ul in all_uls:
                # 检查是否有嵌套结构或大量链接
                nested_ul = ul.find('ul')
                links = ul.find_all('a')
                
                if nested_ul or len(links) >= 5:  # 有嵌套或有足够多的链接
                    if self._is_valid_navigation(ul):
                        found_navs.append(ul)
                        self.logger.debug(f"发现候选导航ul: {len(links)} 个链接, 嵌套: {bool(nested_ul)}")
            
            # 查找包含大量链接的div容器
            if not found_navs:
                potential_nav_divs = soup.find_all('div')
                for div in potential_nav_divs:
                    links = div.find_all('a')
                    if len(links) >= 8:  # 包含足够多链接的div
                        # 检查是否看起来像导航
                        class_names = ' '.join(div.get('class', [])).lower()
                        if any(keyword in class_names for keyword in ['nav', 'menu', 'sidebar', 'tree']):
                            if self._is_valid_navigation(div):
                                found_navs.append(div)
                                self.logger.debug(f"发现候选导航div: {len(links)} 个链接, 类名: {class_names}")
        
        return found_navs
    
    def _is_valid_navigation(self, nav_element) -> bool:
        """判断是否为有效导航"""
        if not nav_element:
            return False
        
        links = nav_element.find_all('a')
        valid_links = [link for link in links if self._is_valid_link(link)]
        
        # 降低要求：对于ul元素或有嵌套结构的元素，1个有效链接就足够
        min_links = 1 if nav_element.name == 'ul' or nav_element.find('ul') else 2
        
        return len(valid_links) >= min_links
    
    def _is_valid_link(self, link) -> bool:
        """判断是否为有效链接"""
        if not link:
            return False
        
        href = link.get('href', '')
        text = link.get_text().strip()
        
        # 过滤无效链接
        if href in ['#', 'javascript:void(0)', 'javascript:', '']:
            return False
        
        # 过滤空文本
        if not text or len(text) < 1:
            return False
        
        return True
    
    def _analyze_navigation(self, nav_element) -> Optional[Dict]:
        """分析单个导航元素，提取层级结构"""
        # 尝试提取层级结构
        hierarchical_items = self._extract_hierarchical_structure(nav_element)
        
        # 如果没有层级结构，使用平面结构
        if not hierarchical_items:
            items = []
            links = nav_element.find_all('a')
            
            for link in links:
                if self._is_valid_link(link):
                    text = self.text_cleaner.clean_nav_text(link.get_text())
                    href = link.get('href', '')
                    
                    items.append({
                        'text': text,
                        'href': href,
                        'is_current': self._is_current_page_link(link),
                        'level': 1,
                        'children': []
                    })
            
            if not items:
                return None
                
            hierarchical_items = items
        
        # 计算最大层级
        max_level = self._calculate_max_level(hierarchical_items)
        
        # 基本导航信息
        nav_info = {
            'display_name': self._get_nav_name(nav_element),
            'nav_type': self._identify_nav_type(nav_element),
            'items': hierarchical_items,
            'levels': max_level,
            'current_item': self._find_current_item_recursive(hierarchical_items)
        }
        
        return nav_info
    
    def _extract_hierarchical_structure(self, nav_element) -> List[Dict]:
        """提取导航的层级结构"""
        try:
            # 首先检查nav_element本身是否就是嵌套的ul
            if nav_element.name == 'ul' and nav_element.find('ul'):
                self.logger.debug("nav_element本身就是嵌套ul，直接解析")
                items = self._parse_nested_list(nav_element, level=1)
                if items:
                    return items
            
            # 寻找可能的层级结构容器
            hierarchical_containers = []
            
            # 查找嵌套的列表结构 (ul > li > ul)
            ul_elements = nav_element.find_all('ul')
            for ul in ul_elements:
                if ul.find('ul'):  # 包含嵌套列表
                    hierarchical_containers.append(ul)
            
            # 查找带有层级类名的元素
            hierarchy_selectors = [
                '.nav-tree', '.tree-nav', '.menu-tree',
                '.nav-hierarchy', '.hierarchical-nav',
                '.nav-level-1', '.level-1'
            ]
            
            for selector in hierarchy_selectors:
                elements = nav_element.select(selector)
                hierarchical_containers.extend(elements)
            
            # 如果找到层级容器，解析其结构
            if hierarchical_containers:
                # 使用第一个有效的层级容器
                for container in hierarchical_containers:
                    items = self._parse_nested_list(container, level=1)
                    if items:
                        self.logger.debug(f"从层级容器解析到 {len(items)} 个项目")
                        return items
            
            return []
            
        except Exception as e:
            self.logger.debug(f"层级结构提取失败: {e}")
            return []
    
    def _parse_nested_list(self, element, level: int = 1) -> List[Dict]:
        """递归解析嵌套列表结构"""
        items = []
        
        # 查找直接子级的列表项
        direct_lis = []
        for child in element.children:
            if hasattr(child, 'name') and child.name == 'li':
                direct_lis.append(child)
        
        self.logger.debug(f"解析层级 {level}，找到 {len(direct_lis)} 个li元素")
        
        for li in direct_lis:
            # 查找该li中的链接
            link = li.find('a')
            if link and self._is_valid_link(link):
                text = self.text_cleaner.clean_nav_text(link.get_text())
                href = link.get('href', '')
                is_current = self._is_current_page_link(link)
                
                # 查找嵌套的子列表
                children = []
                nested_ul = li.find('ul')
                if nested_ul:
                    self.logger.debug(f"在项目 '{text}' 中找到嵌套ul")
                    children = self._parse_nested_list(nested_ul, level + 1)
                
                items.append({
                    'text': text,
                    'href': href,
                    'is_current': is_current,
                    'level': level,
                    'children': children
                })
                
                self.logger.debug(f"添加项目: '{text}' (level={level}, children={len(children)})")
            
            # 如果li没有直接链接但有嵌套结构，处理嵌套部分
            elif li.find('ul'):
                nested_ul = li.find('ul')
                self.logger.debug(f"处理无直接链接的嵌套ul")
                nested_items = self._parse_nested_list(nested_ul, level)
                items.extend(nested_items)
        
        return items
    
    def _calculate_max_level(self, items: List[Dict]) -> int:
        """计算最大层级深度"""
        if not items:
            return 1
        
        max_level = 1
        for item in items:
            current_level = item.get('level', 1)
            max_level = max(max_level, current_level)
            
            # 递归检查子项目
            children = item.get('children', [])
            if children:
                child_max = self._calculate_max_level(children)
                max_level = max(max_level, child_max)
        
        return max_level
    
    def _find_current_item_recursive(self, items: List[Dict]) -> Dict:
        """递归查找当前项目"""
        for item in items:
            if item.get('is_current'):
                return {
                    'found': True,
                    'text': item['text'],
                    'href': item['href'],
                    'level': item.get('level', 1)
                }
            
            # 递归检查子项目
            children = item.get('children', [])
            if children:
                child_result = self._find_current_item_recursive(children)
                if child_result.get('found'):
                    return child_result
        
        return {'found': False}
    
    def _get_nav_name(self, nav_element) -> str:
        """获取导航名称"""
        # 尝试从标题元素获取
        for selector in ['h1', 'h2', 'h3', 'h4', '.nav-title']:
            title = nav_element.find(selector)
            if title:
                title_text = title.get_text().strip()
                if title_text and len(title_text) < 50:
                    return title_text
        
        # 基于类名推断
        classes = ' '.join(nav_element.get('class', [])).lower()
        if 'sidebar' in classes:
            return '📑 侧边栏导航'
        elif 'main' in classes or 'primary' in classes:
            return '🧭 主导航'
        elif 'api' in classes:
            return '🔧 API导航'
        else:
            return '🔗 导航菜单'
    
    def _identify_nav_type(self, nav_element) -> str:
        """识别导航类型"""
        classes = ' '.join(nav_element.get('class', [])).lower()
        element_id = nav_element.get('id', '').lower()
        
        if 'sidebar' in classes or 'side' in classes:
            return 'sidebar_navigation'
        elif 'main' in classes or 'primary' in classes:
            return 'main_navigation'
        elif 'api' in classes or 'docs' in classes:
            return 'api_navigation'
        else:
            return 'general_navigation'
    
    def _is_current_page_link(self, link) -> bool:
        """检查链接是否为当前页面"""
        if not link:
            return False
        
        # 检查CSS类中的当前状态指示器
        classes = link.get('class', [])
        current_indicators = ['active', 'current', 'selected', 'here', 'now', 'is-current', 'current-page']
        
        for indicator in current_indicators:
            if any(indicator in cls.lower() for cls in classes):
                return True
        
        # 检查aria-current属性
        aria_current = link.get('aria-current', '')
        if aria_current in ['page', 'true']:
            return True
        
        # 检查父元素的类
        parent = link.parent
        if parent:
            parent_classes = parent.get('class', [])
            for indicator in current_indicators:
                if any(indicator in cls.lower() for cls in parent_classes):
                    return True
        
        return False
    
    def _find_current_item(self, items) -> Dict:
        """查找当前项目"""
        for item in items:
            if item.get('is_current'):
                return {
                    'found': True,
                    'text': item['text'],
                    'href': item['href']
                }
        
        return {'found': False}
    
    def _find_current_location(self, navigation_data) -> Dict:
        """查找当前位置"""
        for nav in navigation_data:
            current_item = nav.get('current_item', {})
            if current_item.get('found'):
                return {
                    'found': True,
                    'navigation_name': nav.get('display_name'),
                    'navigation_type': nav.get('nav_type'),
                    'current_text': current_item.get('text')
                }
        
        return {'found': False}
    
    def _extract_breadcrumb(self, soup) -> Dict:
        """提取面包屑信息"""
        breadcrumb_selectors = ['.breadcrumb', '.breadcrumbs', '[role="breadcrumb"]']
        
        for selector in breadcrumb_selectors:
            breadcrumb = soup.select_one(selector)
            if breadcrumb:
                items = []
                links = breadcrumb.find_all('a')
                
                for link in links:
                    text = self.text_cleaner.clean_nav_text(link.get_text())
                    href = link.get('href', '')
                    
                    if text:
                        items.append({
                            'text': text,
                            'href': href,
                            'is_current': self._is_current_page_link(link)
                        })
                
                if items:
                    return {'found': True, 'items': items}
        
        return {'found': False, 'items': []}
    
    def _extract_toc(self, soup) -> Dict:
        """提取目录信息"""
        toc_selectors = ['.toc', '.table-of-contents', '#toc']
        
        for selector in toc_selectors:
            toc = soup.select_one(selector)
            if toc:
                items = []
                links = toc.find_all('a')
                
                for link in links:
                    text = self.text_cleaner.clean_nav_text(link.get_text())
                    href = link.get('href', '')
                    
                    if text:
                        items.append({'text': text, 'href': href})
                
                if items:
                    return {'found': True, 'items': items}
        
        return {'found': False, 'items': []} 