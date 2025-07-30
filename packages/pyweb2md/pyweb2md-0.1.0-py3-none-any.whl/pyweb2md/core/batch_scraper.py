"""
批量页面抓取器
从原WebScraper的批量处理功能迁移而来
支持多页面抓取、进度跟踪、错误处理等
"""

import time
import asyncio
from typing import List, Dict, Optional, Callable, Any
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from ..utils.logger import get_logger
from .extractor import Web2MD


class BatchScraper:
    """批量页面抓取器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化批量抓取器
        
        Args:
            config (dict, optional): 配置选项
        """
        self.logger = get_logger("BatchScraper")
        self.config = self._merge_default_config(config)
        
        # 批量处理状态
        self._processing_stats = {
            'total_pages': 0,
            'processed_pages': 0,
            'success_count': 0,
            'error_count': 0,
            'start_time': None,
            'end_time': None,
            'errors': []
        }
        
        # 线程安全
        self._stats_lock = threading.Lock()
        self._progress_callback = None
    
    def _merge_default_config(self, user_config: Optional[Dict] = None) -> Dict:
        """合并默认配置"""
        default = {
            'driver': {
                'browser': 'chrome',
                'headless': True,
                'wait_timeout': 5,
                'max_retries': 2
            },
            'batch': {
                'max_workers': 3,  # 最大并发数
                'delay_between_requests': 1.0,  # 请求间隔
                'respect_robots_txt': True,
                'batch_size': 10,  # 批次大小
                'save_intermediate': True,  # 保存中间结果
                'continue_on_error': True  # 遇到错误继续处理
            },
            'output': {
                'include_navigation': True,
                'include_content': True,
                'include_metadata': True,
                'format': 'markdown'
            }
        }
        
        if user_config:
            # 深度合并配置
            for key, value in user_config.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    default[key].update(value)
                else:
                    default[key] = value
        
        return default
    
    def scrape_urls(self, urls: List[str], progress_callback: Optional[Callable] = None) -> Dict:
        """
        批量抓取URL列表
        
        Args:
            urls (List[str]): URL列表
            progress_callback (Callable, optional): 进度回调函数
            
        Returns:
            Dict: 抓取结果汇总
        """
        if not urls:
            return {'success': False, 'error': 'URL列表为空'}
        
        self.logger.info(f"开始批量抓取 {len(urls)} 个页面")
        
        # 初始化统计
        self._reset_stats()
        self._processing_stats['total_pages'] = len(urls)
        self._processing_stats['start_time'] = time.time()
        self._progress_callback = progress_callback
        
        # 分批处理
        batch_size = self.config['batch']['batch_size']
        max_workers = self.config['batch']['max_workers']
        
        all_results = []
        
        try:
            # 分批处理URL
            for i in range(0, len(urls), batch_size):
                batch_urls = urls[i:i + batch_size]
                self.logger.info(f"处理批次 {i//batch_size + 1}/{(len(urls) + batch_size - 1)//batch_size}")
                
                # 并发处理当前批次
                batch_results = self._process_batch(batch_urls, max_workers)
                all_results.extend(batch_results)
                
                # 批次间延迟
                if i + batch_size < len(urls):
                    delay = self.config['batch']['delay_between_requests']
                    if delay > 0:
                        time.sleep(delay)
            
            # 完成处理
            self._processing_stats['end_time'] = time.time()
            
            # 生成汇总结果
            summary = self._generate_summary(all_results)
            
            self.logger.info(f"批量抓取完成: 成功 {self._processing_stats['success_count']}, "
                           f"失败 {self._processing_stats['error_count']}")
            
            return {
                'success': True,
                'results': all_results,
                'summary': summary,
                'stats': self._processing_stats.copy()
            }
            
        except Exception as e:
            self.logger.error(f"批量抓取失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'partial_results': all_results,
                'stats': self._processing_stats.copy()
            }
    
    def _process_batch(self, urls: List[str], max_workers: int) -> List[Dict]:
        """处理单个批次"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            future_to_url = {
                executor.submit(self._scrape_single_url, url): url 
                for url in urls
            }
            
            # 收集结果
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # 更新统计
                    self._update_stats(result.get('success', False), result.get('error'))
                    
                    # 进度回调
                    if self._progress_callback:
                        self._progress_callback(self._processing_stats.copy())
                        
                except Exception as e:
                    self.logger.error(f"处理URL失败 {url}: {e}")
                    error_result = {
                        'success': False,
                        'url': url,
                        'error': str(e),
                        'data': None
                    }
                    results.append(error_result)
                    self._update_stats(False, str(e))
        
        return results
    
    def _scrape_single_url(self, url: str) -> Dict:
        """抓取单个URL"""
        start_time = time.time()
        
        try:
            self.logger.debug(f"开始抓取: {url}")
            
            # 使用Web2MD提取器
            extractor = Web2MD(self.config.get('driver', {}))
            result = extractor.extract(url)
            
            processing_time = time.time() - start_time
            
            # 格式化返回结果
            return {
                'success': result['metadata']['success'],
                'url': result['url'],
                'original_url': result['original_url'],
                'data': result,
                'processing_time': processing_time,
                'error': result['metadata'].get('error') if not result['metadata']['success'] else None
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"抓取URL失败 {url}: {e}")
            
            return {
                'success': False,
                'url': url,
                'original_url': url,
                'data': None,
                'processing_time': processing_time,
                'error': str(e)
            }
    

    
    def scrape_site_map(self, base_url: str, max_depth: int = 2, 
                       max_pages: int = 50) -> Dict:
        """
        抓取网站地图
        
        Args:
            base_url (str): 基础URL
            max_depth (int): 最大深度
            max_pages (int): 最大页面数
            
        Returns:
            Dict: 抓取结果
        """
        self.logger.info(f"开始抓取网站地图: {base_url}")
        
        try:
            # 发现页面链接
            discovered_urls = self._discover_urls(base_url, max_depth, max_pages)
            
            if not discovered_urls:
                return {'success': False, 'error': '未发现可抓取的URL'}
            
            self.logger.info(f"发现 {len(discovered_urls)} 个页面")
            
            # 批量抓取
            return self.scrape_urls(discovered_urls)
            
        except Exception as e:
            self.logger.error(f"网站地图抓取失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def _discover_urls(self, base_url: str, max_depth: int, max_pages: int) -> List[str]:
        """发现页面URL"""
        discovered = set()
        to_visit = [(base_url, 0)]  # (url, depth)
        visited = set()
        
        driver_manager = DriverManager(self.config['driver'])
        
        try:
            while to_visit and len(discovered) < max_pages:
                current_url, depth = to_visit.pop(0)
                
                if current_url in visited or depth > max_depth:
                    continue
                
                visited.add(current_url)
                discovered.add(current_url)
                
                # 如果还没达到最大深度，提取链接
                if depth < max_depth:
                    try:
                        page_result = driver_manager.load_page_with_retry(current_url)
                        if page_result.get('success'):
                            with driver_manager.get_driver() as driver:
                                links = self._extract_links(driver, base_url)
                                for link in links:
                                    if link not in visited and len(discovered) < max_pages:
                                        to_visit.append((link, depth + 1))
                    except Exception as e:
                        self.logger.warning(f"链接发现失败 {current_url}: {e}")
                        continue
            
            return list(discovered)
            
        finally:
            driver_manager.close()
    
    def _extract_links(self, driver, base_url: str) -> List[str]:
        """提取页面链接"""
        from selenium.webdriver.common.by import By
        
        links = []
        try:
            link_elements = driver.find_elements(By.TAG_NAME, 'a')
            base_domain = urlparse(base_url).netloc
            
            for link in link_elements:
                href = link.get_attribute('href')
                if href:
                    # 处理相对链接
                    if href.startswith('/'):
                        href = urljoin(base_url, href)
                    
                    # 只保留同域名链接
                    if urlparse(href).netloc == base_domain:
                        links.append(href)
                        
        except Exception as e:
            self.logger.warning(f"链接提取失败: {e}")
        
        return list(set(links))  # 去重
    
    def _reset_stats(self):
        """重置统计信息"""
        with self._stats_lock:
            self._processing_stats = {
                'total_pages': 0,
                'processed_pages': 0,
                'success_count': 0,
                'error_count': 0,
                'start_time': None,
                'end_time': None,
                'errors': []
            }
    
    def _update_stats(self, success: bool, error: Optional[str] = None):
        """更新统计信息"""
        with self._stats_lock:
            self._processing_stats['processed_pages'] += 1
            
            if success:
                self._processing_stats['success_count'] += 1
            else:
                self._processing_stats['error_count'] += 1
                if error:
                    self._processing_stats['errors'].append(error)
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """生成结果汇总"""
        summary = {
            'total_pages': len(results),
            'successful_pages': len([r for r in results if r.get('success')]),
            'failed_pages': len([r for r in results if not r.get('success')]),
            'total_processing_time': self._processing_stats.get('end_time', 0) - 
                                   self._processing_stats.get('start_time', 0),
            'average_processing_time': 0,
            'total_content_length': 0,
            'total_word_count': 0
        }
        
        # 计算平均处理时间和内容统计
        processing_times = []
        content_lengths = []
        word_counts = []
        
        for result in results:
            if result.get('success') and result.get('data'):
                # 处理时间
                if 'processing_time' in result:
                    processing_times.append(result['processing_time'])
                
                # 内容长度
                data = result['data']
                if 'content' in data:
                    content = data['content'].get('main_content', '')
                    content_lengths.append(len(content))
                    word_counts.append(len(content.split()))
        
        if processing_times:
            summary['average_processing_time'] = sum(processing_times) / len(processing_times)
        
        if content_lengths:
            summary['total_content_length'] = sum(content_lengths)
            summary['average_content_length'] = sum(content_lengths) / len(content_lengths)
        
        if word_counts:
            summary['total_word_count'] = sum(word_counts)
            summary['average_word_count'] = sum(word_counts) / len(word_counts)
        
        return summary
    
    def get_stats(self) -> Dict:
        """获取当前统计信息"""
        with self._stats_lock:
            return self._processing_stats.copy()
    
    def cancel_processing(self):
        """取消处理（简单实现）"""
        self.logger.warning("批量处理取消请求（当前批次将完成）")
        # 在实际实现中，这里可以设置一个取消标志 