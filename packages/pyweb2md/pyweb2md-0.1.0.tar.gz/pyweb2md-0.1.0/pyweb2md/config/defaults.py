"""
默认配置管理
简化版本的配置，相比原版本大幅减少配置复杂度
"""

DEFAULT_CONFIG = {
    # 浏览器配置
    "browser": "chrome",
    "headless": True,
    "window_size": (1920, 1080),
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    
    # 等待配置
    "wait_timeout": 10,
    "page_load_timeout": 30,
    "implicit_wait": 3,
    
    # 内容提取配置
    "extract_images": True,
    "extract_links": True,
    "max_content_length": 1000000,  # 1MB
    
    # 导航配置
    "max_nav_depth": 3,
    "max_nav_items": 50,
    
    # Markdown转换配置
    "convert_links": True,
    "strip_tags": ["script", "style", "meta", "link"],
    "heading_style": "atx",  # # ## ### 风格
    
    # 日志配置
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}


def merge_config(user_config=None):
    """
    合并用户配置和默认配置
    
    Args:
        user_config (dict): 用户提供的配置
        
    Returns:
        dict: 合并后的配置
    """
    if user_config is None:
        return DEFAULT_CONFIG.copy()
    
    merged = DEFAULT_CONFIG.copy()
    merged.update(user_config)
    return merged


def validate_config(config):
    """
    验证配置的有效性
    
    Args:
        config (dict): 配置字典
        
    Returns:
        bool: 配置是否有效
        
    Raises:
        ValueError: 配置无效时抛出异常
    """
    required_keys = ["browser", "headless", "wait_timeout"]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"缺少必需的配置项: {key}")
    
    if config["browser"] not in ["chrome", "firefox", "safari"]:
        raise ValueError(f"不支持的浏览器: {config['browser']}")
    
    if config["wait_timeout"] <= 0:
        raise ValueError("wait_timeout必须大于0")
    
    return True 