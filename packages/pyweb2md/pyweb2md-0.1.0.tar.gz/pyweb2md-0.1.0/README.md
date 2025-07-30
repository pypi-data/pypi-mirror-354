# PyWeb2MD

🤖 **专为LLM应用优化的网页内容提取和Markdown转换工具**

[![PyPI version](https://badge.fury.io/py/pyweb2md.svg)](https://badge.fury.io/py/pyweb2md)
[![Python](https://img.shields.io/pypi/pyversions/pyweb2md)](https://pypi.org/project/pyweb2md/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 🎯 为什么选择 PyWeb2MD？

传统爬虫返回原始HTML，LLM难以处理且token消耗巨大；PyWeb2MD转换为结构化Markdown，显著降低token消耗并保持内容结构。

**传统爬虫 vs PyWeb2MD**:
- ❌ 传统爬虫：返回原始HTML，LLM难以处理，token消耗巨大
- ✅ PyWeb2MD：转换为结构化Markdown + 导航信息，为LLM应用优化

## ⚡ 快速开始

### 安装

```bash
pip install pyweb2md
```

### 基础使用

```python
from pyweb2md import Web2MD

# 基础使用
converter = Web2MD()
result = converter.extract("https://docs.python.org/3/")

print(f"提取时间: {result['metadata']['extraction_time']}")
print(result['content'])  # 可直接用于LLM

# 只获取内容
content = converter.get_content("https://example.com")
print(content)
```

### 批量处理

```python
from pyweb2md import Web2MD

# 批量处理文档站点
docs_urls = [
    "https://docs.python.org/3/tutorial/",
    "https://docs.python.org/3/library/", 
    "https://docs.python.org/3/reference/"
]

converter = Web2MD()
results = converter.batch_extract(docs_urls)

# 构建知识库
knowledge_base = []
for result in results:
    if result['content']:
        knowledge_base.append({
            'title': result['title'],
            'content': result['content'], 
            'extraction_time': result['metadata']['extraction_time']
        })

print(f"成功提取了 {len(knowledge_base)} 个文档")
```

## 🚀 主要特性

- 🧹 **HTML→Markdown转换** - 高质量转换，保持内容结构
- 🔧 **轻量高效** - 专注核心功能，保持包体积精简
- 🧭 **导航提取** - 提取页面导航结构（面包屑、上下页等）
- 🖼️ **图片处理** - 提取图片链接，转换为Markdown格式
- ⚡ **纯数据转换** - 专注转换质量，控制逻辑留给用户
- 🔄 **批量处理** - 支持多URL并发处理

## 📊 输出格式

```python
{
    # 核心内容 - 清洗后的Markdown
    "content": "# Python 3.12 Documentation\n\n## Quick Start\n...",
    
    # 导航信息（核心功能）
    "navigation": {
        "breadcrumb": ["首页", "Python教程", "快速开始"],
        "siblings": {
            "previous": {"title": "安装指南", "url": "/install"},
            "next": {"title": "进阶教程", "url": "/advanced"}
        }
    },
    
    # 页面基本信息
    "metadata": {
        "title": "Python 3.12 Documentation",
        "url": "https://docs.python.org/3/",
        "extraction_time": "2024-01-01T10:30:00Z"
    },
    
    # 结构化数据
    "images": [
        {
            "src": "https://docs.python.org/3/_images/tutorial.png",
            "alt": "Python tutorial diagram", 
            "title": "Tutorial workflow"
        }
    ]
}
```

## 🤖 与LLM应用集成

```python
import openai
from pyweb2md import Web2MD

def analyze_webpage_with_llm(url: str, question: str):
    """使用LLM分析网页内容"""
    
    # 1. 提取并优化网页内容
    converter = Web2MD()
    result = converter.extract(url)
    
    # 2. 检查提取结果
    if not result['content']:
        return "网页提取失败：无法获取内容"
    
    # 3. 检查内容长度（用户控制）
    content_length = len(result['content'])
    if content_length > 10000:  # 大约3500 tokens
        print("⚠️ 内容较长，建议分段处理")
        
    # 4. 构建LLM输入
    prompt = f"""
请分析以下网页内容并回答问题：

网页标题: {result['title']}
内容:
{result['content']}

问题: {question}
"""
    
    # 5. 调用LLM
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# 使用示例
answer = analyze_webpage_with_llm(
    "https://docs.python.org/3/tutorial/",
    "Python的主要特性有哪些？"
)
print(answer)
```

## 🔧 配置选项

```python
from pyweb2md import Web2MD

# 自定义配置
converter = Web2MD(config={
    'timeout': 60,                # 加载超时时间
    'retry_count': 5,             # 重试次数
    'headless': True,             # 无头模式浏览器
    'extract_images': True,       # 是否提取图片
    'max_content_length': 1000000 # 最大内容长度
})

result = converter.extract("https://example.com")
```

## 📦 开发版本安装

```bash
# 开发版本安装（包含测试工具）
pip install pyweb2md[dev]

# 标准安装（推荐）
pip install pyweb2md
```

## 📋 系统要求

- **Python版本**: 3.8+
- **操作系统**: Windows, macOS, Linux  
- **浏览器**: Chrome (自动管理ChromeDriver)
- **内存**: 建议4GB+

## 🏗️ 核心依赖

- **selenium>=4.15.0** - 浏览器自动化
- **beautifulsoup4>=4.12.0** - HTML解析
- **lxml>=4.9.0** - XML/HTML处理
- **webdriver-manager>=4.0.0** - 自动WebDriver管理

## 📈 性能特点

- **页面加载成功率**: 80-90%
- **平均处理时间**: 2-5秒/页面
- **内容优化**: 相比原始HTML大幅减少内容冗余
- **并发处理**: 支持多线程批量处理

## 🛠️ API文档

### Web2MD 类

#### 构造函数
```python
Web2MD(config: Optional[Dict] = None)
```

#### 主要方法

- `extract(url)` - 提取完整信息
- `get_content(url)` - 只获取Markdown内容
- `batch_extract(urls)` - 批量处理多个URL

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- 🏠 **项目主页**: https://github.com/username/pyweb2md
- 🐛 **问题反馈**: https://github.com/username/pyweb2md/issues
- 📚 **文档**: https://pyweb2md.readthedocs.io
- 💬 **讨论**: https://github.com/username/pyweb2md/discussions

---

**注意**: 本项目专注于网页内容提取和转换，不包含业务逻辑控制。适合作为其他LLM应用的基础组件使用。 