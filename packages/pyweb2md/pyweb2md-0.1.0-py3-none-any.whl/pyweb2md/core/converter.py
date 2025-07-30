"""
HTML到Markdown转换器
从原WebScraper的HTML处理功能迁移而来
支持完整的HTML标签到Markdown语法转换
"""

import re
from typing import Optional, Dict, List
from urllib.parse import urljoin, urlparse
from ..utils.logger import get_logger

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class HTMLToMarkdownConverter:
    """HTML到Markdown转换器 - 完整版本"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化转换器
        
        Args:
            config (dict, optional): 转换配置
        """
        self.logger = get_logger("HTMLToMarkdownConverter")
        self.config = self._merge_default_config(config)
        
        # 转换状态
        self._base_url = ""
        self._current_list_level = 0
        self._in_table = False
    
    def _merge_default_config(self, user_config: Optional[Dict] = None) -> Dict:
        """合并默认配置"""
        default = {
            'preserve_links': True,
            'preserve_images': True,
            'preserve_tables': True,
            'preserve_code_blocks': True,
            'preserve_lists': True,
            'convert_headings': True,
            'convert_emphasis': True,
            'strip_scripts': True,
            'strip_styles': True,
            'wrap_width': 0,  # 0表示不自动换行
            'link_style': 'inline',  # inline或reference
            'code_fence_style': '```',  # ```或~~~
            'heading_style': 'atx',  # atx(#)或setext(下划线)
            'emphasis_style': '*',  # *或_
        }
        
        if user_config:
            default.update(user_config)
        
        return default
    
    def convert(self, html_content: str, base_url: str = "") -> str:
        """
        转换HTML到Markdown
        
        Args:
            html_content (str): HTML内容
            base_url (str): 基础URL，用于相对链接转换
            
        Returns:
            str: Markdown内容
        """
        if not html_content:
            return ""
        
        self._base_url = base_url
        
        try:
            if BS4_AVAILABLE:
                return self._convert_with_bs4(html_content)
            else:
                self.logger.warning("BeautifulSoup不可用，使用简单转换")
                return self._convert_simple(html_content)
                
        except Exception as e:
            self.logger.error(f"HTML转换失败: {e}")
            return self._convert_simple(html_content)
    
    def _convert_with_bs4(self, html_content: str) -> str:
        """使用BeautifulSoup进行完整转换"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 清理不需要的标签
            if self.config.get('strip_scripts', True):
                for script in soup.find_all(['script', 'style', 'noscript']):
                    script.decompose()
            
            # 转换为Markdown
            markdown_content = self._process_element(soup)
            
            # 后处理
            markdown_content = self._post_process_markdown(markdown_content)
            
            return markdown_content
            
        except Exception as e:
            self.logger.error(f"BeautifulSoup转换失败: {e}")
            return self._convert_simple(html_content)
    
    def _process_element(self, element) -> str:
        """递归处理HTML元素"""
        if isinstance(element, NavigableString):
            return self._clean_text(str(element))
        
        if not isinstance(element, Tag):
            return ""
        
        tag_name = element.name.lower()
        
        # 标题转换
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.config.get('convert_headings', True):
            return self._convert_heading(element)
        
        # 段落转换
        elif tag_name == 'p':
            return self._convert_paragraph(element)
        
        # 强调转换
        elif tag_name in ['strong', 'b'] and self.config.get('convert_emphasis', True):
            return self._convert_strong(element)
        
        elif tag_name in ['em', 'i'] and self.config.get('convert_emphasis', True):
            return self._convert_emphasis(element)
        
        # 链接转换
        elif tag_name == 'a' and self.config.get('preserve_links', True):
            return self._convert_link(element)
        
        # 图片转换
        elif tag_name == 'img' and self.config.get('preserve_images', True):
            return self._convert_image(element)
        
        # 代码转换
        elif tag_name == 'code' and self.config.get('preserve_code_blocks', True):
            return self._convert_inline_code(element)
        
        elif tag_name == 'pre' and self.config.get('preserve_code_blocks', True):
            return self._convert_code_block(element)
        
        # 列表转换
        elif tag_name in ['ul', 'ol'] and self.config.get('preserve_lists', True):
            return self._convert_list(element)
        
        elif tag_name == 'li':
            return self._convert_list_item(element)
        
        # 表格转换
        elif tag_name == 'table' and self.config.get('preserve_tables', True):
            return self._convert_table(element)
        
        # 换行转换
        elif tag_name == 'br':
            return '\n'
        
        elif tag_name == 'hr':
            return '\n---\n\n'
        
        # 引用转换
        elif tag_name == 'blockquote':
            return self._convert_blockquote(element)
        
        # 行内元素
        elif tag_name in ['span', 'div', 'section', 'article', 'main']:
            return self._process_children(element)
        
        # 忽略的标签
        elif tag_name in ['script', 'style', 'noscript', 'head', 'meta', 'link']:
            return ""
        
        # 默认处理：处理子元素
        else:
            return self._process_children(element)
    
    def _process_children(self, element) -> str:
        """处理元素的子节点"""
        results = []
        for child in element.children:
            result = self._process_element(child)
            if result:
                results.append(result)
        return ''.join(results)
    
    def _convert_heading(self, element) -> str:
        """转换标题"""
        level = int(element.name[1])  # h1 -> 1, h2 -> 2, etc.
        text = self._get_text_content(element)
        
        if self.config.get('heading_style') == 'atx':
            return f"\n{'#' * level} {text}\n\n"
        else:
            # Setext style (只支持h1和h2)
            if level == 1:
                return f"\n{text}\n{'=' * len(text)}\n\n"
            elif level == 2:
                return f"\n{text}\n{'-' * len(text)}\n\n"
            else:
                return f"\n{'#' * level} {text}\n\n"
    
    def _convert_paragraph(self, element) -> str:
        """转换段落"""
        text = self._process_children(element)
        return f"{text}\n\n" if text.strip() else ""
    
    def _convert_strong(self, element) -> str:
        """转换粗体"""
        text = self._get_text_content(element)
        marker = '**'
        return f"{marker}{text}{marker}"
    
    def _convert_emphasis(self, element) -> str:
        """转换斜体"""
        text = self._get_text_content(element)
        marker = self.config.get('emphasis_style', '*')
        return f"{marker}{text}{marker}"
    
    def _convert_link(self, element) -> str:
        """转换链接"""
        text = self._get_text_content(element)
        href = element.get('href', '')
        
        if not href:
            return text
        
        # 处理相对链接
        if self._base_url and not href.startswith(('http://', 'https://', 'mailto:', '#')):
            href = urljoin(self._base_url, href)
        
        # 内联样式
        if self.config.get('link_style') == 'inline':
            title = element.get('title', '')
            if title:
                return f'[{text}]({href} "{title}")'
            else:
                return f'[{text}]({href})'
        else:
            # 引用样式（简化实现）
            return f'[{text}]({href})'
    
    def _convert_image(self, element) -> str:
        """转换图片"""
        alt = element.get('alt', '')
        src = element.get('src', '')
        title = element.get('title', '')
        
        if not src:
            return alt
        
        # 处理相对链接
        if self._base_url and not src.startswith(('http://', 'https://', 'data:')):
            src = urljoin(self._base_url, src)
        
        if title:
            return f'![{alt}]({src} "{title}")'
        else:
            return f'![{alt}]({src})'
    
    def _convert_inline_code(self, element) -> str:
        """转换行内代码"""
        text = self._get_text_content(element)
        return f'`{text}`'
    
    def _convert_code_block(self, element) -> str:
        """转换代码块"""
        # 检查是否包含code标签
        code_element = element.find('code')
        if code_element:
            text = self._get_text_content(code_element)
            # 尝试检测语言
            class_attr = code_element.get('class', [])
            language = self._detect_language_from_class(class_attr)
        else:
            text = self._get_text_content(element)
            language = ""
        
        fence = self.config.get('code_fence_style', '```')
        
        if language:
            return f"\n{fence}{language}\n{text}\n{fence}\n\n"
        else:
            return f"\n{fence}\n{text}\n{fence}\n\n"
    
    def _convert_list(self, element) -> str:
        """转换列表"""
        self._current_list_level += 1
        
        items = []
        is_ordered = element.name == 'ol'
        
        for i, li in enumerate(element.find_all('li', recursive=False)):
            if is_ordered:
                marker = f"{i + 1}."
            else:
                marker = "-"
            
            indent = "  " * (self._current_list_level - 1)
            item_content = self._process_element(li).strip()
            items.append(f"{indent}{marker} {item_content}")
        
        self._current_list_level -= 1
        
        result = "\n".join(items)
        return f"\n{result}\n\n" if self._current_list_level == 0 else f"\n{result}\n"
    
    def _convert_list_item(self, element) -> str:
        """转换列表项"""
        return self._process_children(element)
    
    def _convert_table(self, element) -> str:
        """转换表格"""
        rows = []
        
        # 处理表头
        thead = element.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = [self._get_text_content(th).strip() 
                          for th in header_row.find_all(['th', 'td'])]
                if headers:
                    rows.append('| ' + ' | '.join(headers) + ' |')
                    rows.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
        
        # 处理表体
        tbody = element.find('tbody') or element
        for tr in tbody.find_all('tr'):
            cells = [self._get_text_content(cell).strip().replace('\n', ' ') 
                    for cell in tr.find_all(['td', 'th'])]
            if cells:
                rows.append('| ' + ' | '.join(cells) + ' |')
        
        if rows:
            return f"\n{chr(10).join(rows)}\n\n"
        else:
            return ""
    
    def _convert_blockquote(self, element) -> str:
        """转换引用"""
        content = self._process_children(element).strip()
        lines = content.split('\n')
        quoted_lines = [f"> {line}" if line.strip() else ">" for line in lines]
        return f"\n{chr(10).join(quoted_lines)}\n\n"
    
    def _get_text_content(self, element) -> str:
        """获取元素的文本内容"""
        if isinstance(element, NavigableString):
            return self._clean_text(str(element))
        
        return self._clean_text(element.get_text())
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 规范化空白字符
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _detect_language_from_class(self, class_list) -> str:
        """从class属性检测代码语言"""
        if isinstance(class_list, str):
            class_list = [class_list]
        
        for class_name in class_list:
            class_name = class_name.lower()
            # 常见的语言标识模式
            patterns = [
                r'lang-(\w+)',
                r'language-(\w+)',
                r'highlight-(\w+)',
                r'^(\w+)$'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, class_name)
                if match:
                    lang = match.group(1)
                    # 验证是否是已知语言
                    known_languages = [
                        'python', 'javascript', 'java', 'cpp', 'c', 'html', 'css', 
                        'sql', 'json', 'xml', 'yaml', 'bash', 'shell', 'php', 'ruby'
                    ]
                    if lang in known_languages:
                        return lang
        
        return ""
    
    def _post_process_markdown(self, markdown: str) -> str:
        """后处理Markdown内容"""
        # 清理多余的空行
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # 清理行尾空白
        lines = markdown.split('\n')
        cleaned_lines = [line.rstrip() for line in lines]
        markdown = '\n'.join(cleaned_lines)
        
        # 确保文档以换行结束
        if markdown and not markdown.endswith('\n'):
            markdown += '\n'
        
        return markdown.strip()
    
    def _convert_simple(self, html_content: str) -> str:
        """简单的HTML转换（不依赖BeautifulSoup）"""
        # 基础HTML标签转换
        content = html_content
        
        # 标题转换
        for i in range(1, 7):
            content = re.sub(f'<h{i}[^>]*>(.*?)</h{i}>', f'\n{"#" * i} \\1\n\n', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 段落转换
        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 强调转换
        content = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 链接转换
        content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 代码转换
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'\n```\n\1\n```\n\n', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 换行转换
        content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'<hr\s*/?>', '\n---\n\n', content, flags=re.IGNORECASE)
        
        # 移除所有剩余的HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        
        # 清理空白
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r'[ \t]+', ' ', content)
        
        return content.strip()
    
    # 向后兼容方法
    def convert_html_to_text(self, html_content: str) -> str:
        """向后兼容的简单文本转换"""
        return self._convert_simple(html_content)
    
    def convert_to_text(self, html_content: str) -> str:
        """向后兼容的简单文本转换"""
        return self._convert_simple(html_content)
