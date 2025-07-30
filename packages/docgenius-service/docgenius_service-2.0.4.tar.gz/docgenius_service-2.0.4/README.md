# DocGenius - AI驱动的动态文档生成服务

DocGenius 是一个基于模型上下文协议（MCP）的智能服务，能够接收用户的自然语言指令和文本内容，自主选择合适的文档模板，将文本内容渲染成设计精美的HTML，并输出为图片。

## 🚀 特性

- **动态模板发现**: AI能够自动扫描并发现可用的文档模板
- **智能模板选择**: 根据用户需求自动选择最合适的模板
- **多种模板支持**: 支持简历、知识卡片等多种文档类型
- **高质量渲染**: 使用Playwright进行精确的HTML到图片转换
- **按模板分类存储**: 自动按模板类型组织输出文件
- **基于FastMCP**: 使用现代化的MCP框架构建

## 📁 项目结构

```
card-creator-mcp/
├── templates/              # 模板文件目录
│   ├── resume.md          # 简历模板
│   └── knowledge_card.md  # 知识卡片模板
├── pic/                   # 输出图片目录（自动创建）
├── main_service.py        # 主服务文件
├── requirements.txt       # 项目依赖
└── README.md             # 项目文档
```

## 🛠️ 安装方式

### 方式一：使用 uvx 直接运行（推荐）

无需本地安装，直接运行最新版本：

```bash
# 直接运行服务
uvx docgenius-service

# 或使用简化命令
uvx --from docgenius-service docgenius
```

### 方式二：pip 安装

```bash
# 安装到本地环境
pip install docgenius-service

# 运行服务
docgenius-service
# 或
docgenius
```

### 方式三：开发模式

如果你需要修改源码：

```bash
git clone <repository-url>
cd docgenius-service
pip install -e .
docgenius-service  # 首次运行会自动安装Chromium浏览器
```

## ⚙️ 配置选项

### 环境变量

DocGenius 支持通过环境变量进行配置：

- `DOCGENIUS_TEMPLATES_DIR`: 自定义模板文件夹路径（可选）

**设置方式：**

1. **使用 .env 文件（推荐）**：
   ```bash
   # 在当前目录创建 .env 文件
   echo "DOCGENIUS_TEMPLATES_DIR=/path/to/your/templates" > .env
   docgenius-service
   ```

2. **命令行设置**：
   ```bash
   # Windows PowerShell
   $env:DOCGENIUS_TEMPLATES_DIR="D:\path\to\templates" ; docgenius-service
   
   # Linux/macOS
   DOCGENIUS_TEMPLATES_DIR=/path/to/templates docgenius-service
   ```

### MCP 客户端配置

如果你使用 MCP 客户端（如 Claude Desktop），可以在 `mcp.json` 中配置：

```json
{
  "mcpServers": {
    "docgenius": {
      "command": "uvx",
      "args": ["docgenius-service"],
      "env": {
        "DOCGENIUS_TEMPLATES_DIR": "/path/to/your/custom/templates"
      }
    }
  }
}
```

或者使用本地安装的版本：

```json
{
  "mcpServers": {
    "docgenius": {
      "command": "docgenius-service",
      "env": {
        "DOCGENIUS_TEMPLATES_DIR": "/path/to/your/custom/templates"
      }
    }
  }
}
```

## 🎯 可用工具

### 1. list_available_templates()
列出所有可用的文档模板。

**返回**: 包含模板名称和描述的列表

### 2. get_template_details(template_name: str)
获取指定模板的详细信息，包括元数据和提示词。

**参数**:
- `template_name`: 模板名称

**返回**: 包含模板详细信息的字典

### 3. save_html_file(html_content: str, template_name: str, file_name: str)
将HTML内容保存为本地文件。

**参数**:
- `html_content`: HTML代码字符串
- `template_name`: 使用的模板名称
- `file_name`: 输出文件名（不含扩展名）

**返回**: 保存的HTML文件的绝对路径

### 4. create_image_from_html_file(html_file_path: str, width: int, height: int)
读取本地HTML文件并将其渲染为JPG图片。

**参数**:
- `html_file_path`: HTML文件的路径
- `width`: 图片宽度
- `height`: 图片高度

**返回**: 生成的JPG图片文件的绝对路径

## 📋 模板格式

模板文件采用Markdown格式，包含YAML Frontmatter：

```markdown
---
description: "模板描述"
width: 800
height: 600
---
这里是提示词内容，使用 {user_text} 作为用户输入的占位符。
```

## 🔧 技术栈

- **FastMCP**: MCP服务框架
- **Playwright**: 无头浏览器自动化
- **python-frontmatter**: YAML frontmatter解析
- **aiofiles**: 异步文件操作

## 📝 使用示例

### 完整的工作流程

```python
# 1. 列出可用模板
templates = await client.call_tool("list_available_templates")

# 2. 获取模板详情
details = await client.call_tool("get_template_details", {"template_name": "resume"})

# 3. 保存HTML文件
html_path = await client.call_tool("save_html_file", {
    "html_content": "<html>...</html>",
    "template_name": "resume", 
    "file_name": "my_resume"
})

# 4. 生成图片
image_path = await client.call_tool("create_image_from_html_file", {
    "html_file_path": html_path,
    "width": 827,
    "height": 1169
})
```

### 快速测试

运行服务后，文件将保存在当前工作目录的 `pic/` 文件夹中，按模板类型自动分类：

```
当前目录/
├── pic/
│   ├── resume/
│   │   ├── my_resume.html
│   │   └── my_resume.jpg
│   └── knowledge_card/
│       ├── my_card.html
│       └── my_card.jpg
```

## 🚧 开发状态

该项目目前处于 **2.0.3** 版本，具备以下特性：

- ✅ 支持 `uvx` 一键运行
- ✅ 智能模板路径解析
- ✅ 环境变量配置支持
- ✅ 分离式工具设计（HTML保存 + 图片生成）
- ✅ 完整的 MCP 客户端配置支持
- ✅ 跨平台兼容（Windows/Linux/macOS）
- ✅ **自动安装 Playwright 浏览器**（新功能）

**更新日志：**
- v2.0.3: 🎉 **自动安装 Playwright 浏览器** - 首次运行自动检测并安装 Chromium，显著改善用户体验
- v2.0.2: 修复 uvx 运行问题，包含模板文件
- v2.0.1: 添加 docgenius-service 命令支持  
- v2.0.0: 重构为标准 Python 包，支持 uvx 分发

## 📄 许可证

本项目采用MIT许可证开源。 