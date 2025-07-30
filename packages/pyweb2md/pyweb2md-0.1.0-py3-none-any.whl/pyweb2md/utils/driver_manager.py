"""
浏览器驱动管理器
从原WebScraper的setup_driver()和相关方法迁移而来
负责浏览器驱动的完整生命周期管理
"""

import time
import os
from pathlib import Path
from typing import Optional, Dict
from contextlib import contextmanager
from .logger import get_logger

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class DriverManager:
    """浏览器驱动管理器"""
    
    def __init__(self, config: Optional[dict] = None):
        """
        初始化驱动管理器
        
        Args:
            config (dict, optional): 驱动配置
        """
        self.logger = get_logger("DriverManager")
        self.config = self._merge_default_config(config)
        self.driver = None
        self._current_base_url = None
    
    def _merge_default_config(self, user_config: Optional[dict] = None) -> Dict:
        """合并默认配置"""
        default = {
            'browser': 'chrome',
            'headless': True,
            'wait_timeout': 10,
            'page_load_timeout': 30,
            'implicit_wait': 5,
            'user_agent': None,
            'window_size': (1920, 1080),
            'mobile_mode': False,
            'disable_images': True,  # 提升加载速度
            'disable_plugins': True,
            'max_retries': 3
        }
        
        if user_config:
            default.update(user_config)
        
        return default
    
    def setup_driver(self):
        """设置浏览器驱动 - 从原WebScraper.setup_driver()迁移"""
        if not SELENIUM_AVAILABLE:
            raise RuntimeError("Selenium不可用，请安装selenium和相关驱动")
        
        try:
            browser = self.config.get('browser', 'chrome').lower()
            
            if browser == 'chrome':
                self.driver = self._setup_chrome_driver()
            elif browser == 'firefox':
                self.driver = self._setup_firefox_driver()
            else:
                raise ValueError(f"不支持的浏览器类型: {browser}")
            
            # 设置超时和等待
            self.driver.implicitly_wait(self.config.get('implicit_wait', 5))
            self.driver.set_page_load_timeout(self.config.get('page_load_timeout', 30))
            
            self.logger.info(f"浏览器驱动设置完成: {browser}")
            
        except Exception as e:
            self.logger.error(f"浏览器驱动设置失败: {e}")
            raise
    
    def _setup_chrome_driver(self):
        """设置Chrome驱动"""
        chrome_options = Options()
        
        # 基础设置
        if self.config.get('headless', True):
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # 窗口大小
        window_size = self.config.get('window_size', [1920, 1080])
        chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        
        # User-Agent
        user_agent = self.config.get('user_agent')
        if user_agent:
            chrome_options.add_argument(f'--user-agent={user_agent}')
        
        # 移动端模拟
        if self.config.get('mobile_mode', False):
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # 性能优化
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-extensions')
        
        if self.config.get('disable_plugins', True):
            chrome_options.add_argument('--disable-plugins')
        
        if self.config.get('disable_images', True):
            chrome_options.add_argument('--disable-images')
        
        # 查找ChromeDriver
        service = self._find_chrome_driver()
        
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def _find_chrome_driver(self):
        """查找ChromeDriver - 优先使用本地版本"""
        # 查找本地ChromeDriver
        project_root = Path(__file__).parent.parent.parent.parent
        local_chromedriver_paths = [
            project_root / "drivers" / "chromedriver-mac-x64" / "chromedriver",
            project_root / "drivers" / "chromedriver-mac-arm64" / "chromedriver", 
            project_root / "drivers" / "chromedriver-linux64" / "chromedriver",
            project_root / "drivers" / "chromedriver-win64" / "chromedriver.exe",
            project_root / "drivers" / "chromedriver-win32" / "chromedriver.exe",
        ]
        
        for driver_path in local_chromedriver_paths:
            if driver_path.exists() and os.access(driver_path, os.X_OK):
                self.logger.info(f"使用本地ChromeDriver: {driver_path}")
                return Service(str(driver_path))
        
        # 回退到WebDriver Manager
        self.logger.warning("本地ChromeDriver不可用，使用WebDriver Manager")
        return Service(ChromeDriverManager().install())
    
    def _setup_firefox_driver(self):
        """设置Firefox驱动"""
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        
        firefox_options = FirefoxOptions()
        
        if self.config.get('headless', True):
            firefox_options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=firefox_options)
    
    def smart_wait(self, wait_time: int = None):
        """智能等待策略 - 从原WebScraper._smart_wait()迁移"""
        if not self.driver:
            return
        
        wait_time = wait_time or self.config.get('wait_timeout', 10)
        
        try:
            # 1. 等待DOM加载完成
            WebDriverWait(self.driver, min(wait_time, 10)).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # 2. 等待主要内容加载
            content_selectors = [
                'main', 'article', '.content', '#content', 
                '.main-content', '.documentation', '.api-docs'
            ]
            
            for selector in content_selectors:
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    self.logger.debug(f"找到主要内容容器: {selector}")
                    break
                except TimeoutException:
                    continue
            
            # 3. 等待Ajax请求完成 (jQuery)
            try:
                WebDriverWait(self.driver, 3).until(
                    lambda d: d.execute_script("return typeof jQuery !== 'undefined' ? jQuery.active == 0 : true")
                )
            except:
                pass  # 页面可能不使用jQuery
            
            # 4. 额外等待时间
            if wait_time > 0:
                time.sleep(min(wait_time, 5))  # 最多等待5秒
                
        except TimeoutException:
            self.logger.warning("智能等待超时，继续处理")
        except Exception as e:
            self.logger.warning(f"智能等待异常: {e}")
    
    def verify_page_load(self) -> bool:
        """验证页面是否成功加载 - 从原WebScraper._verify_page_load()迁移"""
        if not self.driver:
            return False
        
        try:
            # 检查页面是否有基本的HTML结构
            page_source = self.driver.page_source
            
            if not page_source or len(page_source) < 100:
                return False
            
            # 检查是否有错误页面标识
            error_indicators = [
                '404', '403', '500', 'not found', 'access denied', 
                'server error', 'page not found', 'forbidden'
            ]
            
            page_lower = page_source.lower()
            title_lower = self.driver.title.lower() if self.driver.title else ""
            
            for indicator in error_indicators:
                if indicator in page_lower or indicator in title_lower:
                    self.logger.warning(f"检测到错误页面标识: {indicator}")
                    return False
            
            # 检查是否有基本的HTML标签
            basic_tags = ['<html', '<head', '<body']
            if not any(tag in page_source.lower() for tag in basic_tags):
                return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"页面加载验证异常: {e}")
            return False
    
    def load_page_with_retry(self, url: str, options: Optional[Dict] = None) -> Dict:
        """带重试机制的页面加载"""
        if not self.driver:
            self.setup_driver()
        
        options = options or {}
        max_retries = options.get('max_retries', self.config.get('max_retries', 3))
        attempt_count = 0
        start_time = time.time()
        
        self._current_base_url = url
        
        while attempt_count < max_retries:
            try:
                attempt_count += 1
                self.logger.info(f"加载页面 (第{attempt_count}次尝试): {url}")
                
                # 设置页面加载超时
                timeout = options.get('page_load_timeout', self.config.get('page_load_timeout', 30))
                self.driver.set_page_load_timeout(timeout)
                
                # 访问页面
                self.driver.get(url)
                
                # 智能等待
                wait_time = options.get('wait_time', self.config.get('wait_timeout', 3))
                self.smart_wait(wait_time)
                
                # 验证页面加载
                if not self.verify_page_load():
                    if attempt_count < max_retries:
                        self.logger.warning(f"页面加载验证失败，重试 (第{attempt_count}次)")
                        time.sleep(2)
                        continue
                    else:
                        self.logger.warning("页面加载验证失败，继续处理")
                
                # 成功加载
                processing_time = time.time() - start_time
                self._current_base_url = self.driver.current_url
                
                return {
                    'success': True,
                    'url': self.driver.current_url,
                    'original_url': url,
                    'title': self.driver.title,
                    'page_source': self.driver.page_source,
                    'processing_time': processing_time,
                    'attempt_count': attempt_count
                }
                
            except TimeoutException as e:
                if attempt_count < max_retries:
                    self.logger.warning(f"页面加载超时，重试 (第{attempt_count}次): {str(e)}")
                    time.sleep(2)
                    continue
                else:
                    processing_time = time.time() - start_time
                    self.logger.error(f"页面加载超时，已达最大重试次数: {str(e)}")
                    return self._create_error_result(url, f"页面加载超时: {str(e)}", processing_time, attempt_count)
            
            except WebDriverException as e:
                if attempt_count < max_retries:
                    self.logger.warning(f"WebDriver异常，重试 (第{attempt_count}次): {str(e)}")
                    time.sleep(3)
                    continue
                else:
                    processing_time = time.time() - start_time
                    self.logger.error(f"WebDriver异常，已达最大重试次数: {str(e)}")
                    return self._create_error_result(url, f"WebDriver异常: {str(e)}", processing_time, attempt_count)
        
        # 所有重试都失败了
        processing_time = time.time() - start_time
        return self._create_error_result(url, "达到最大重试次数，页面加载失败", processing_time, attempt_count)
    
    def _create_error_result(self, url: str, error_msg: str, processing_time: float, attempt_count: int) -> Dict:
        """创建错误结果"""
        return {
            'success': False,
            'url': url,
            'error': error_msg,
            'page_source': '',
            'title': '',
            'processing_time': processing_time,
            'attempt_count': attempt_count
        }
    
    @contextmanager
    def get_driver(self):
        """上下文管理器 - 获取驱动实例"""
        if not self.driver:
            self.setup_driver()
        
        try:
            yield self.driver
        except Exception as e:
            self.logger.error(f"驱动使用异常: {e}")
            raise
        # 注意：不在这里关闭driver，由close()方法负责
    
    def get_current_url(self) -> Optional[str]:
        """获取当前URL"""
        return self._current_base_url
    
    def close(self):
        """关闭浏览器驱动"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("浏览器驱动已关闭")
            except Exception as e:
                self.logger.warning(f"关闭浏览器驱动失败: {e}")
            finally:
                self.driver = None
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close() 