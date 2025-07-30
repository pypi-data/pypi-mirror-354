import os
import sys
import asyncio
from pathlib import Path
from fastmcp import FastMCP
from playwright.async_api import async_playwright
import frontmatter
import aiofiles

# 初始化 FastMCP 服务
mcp = FastMCP("DocGeniusService")

# 1. 智能路径解析：支持开发环境和安装环境
def _find_templates_dir():
    """
    智能查找模板目录，支持开发环境和安装环境。
    """
    # 1. 优先使用环境变量
    template_dir_env = os.getenv('DOCGENIUS_TEMPLATES_DIR')
    if template_dir_env:
        path = Path(template_dir_env).absolute()
        if path.is_dir():
            return path
    
    # 2. 开发环境：相对于文件的路径
    dev_path = Path(__file__).parent.parent.parent / "templates"
    if dev_path.is_dir():
        return dev_path
    
    # 3. 安装环境：相对于包文件的路径
    package_path = Path(__file__).parent / "templates"
    if package_path.is_dir():
        return package_path
    
    # 4. 尝试从当前工作目录查找
    cwd_path = Path.cwd() / "templates"
    if cwd_path.is_dir():
        return cwd_path
    
    # 5. 如果都找不到，返回开发环境的默认路径（会在main函数中检查并报错）
    return dev_path

TEMPLATE_DIR = _find_templates_dir()

# 输出目录改为基于当前工作目录
OUTPUT_DIR = Path.cwd() / "pic"

def _list_available_templates() -> list[dict]:
    """
    扫描 'templates' 文件夹，列出所有可用文档模板的名称和描述。
    """
    if not TEMPLATE_DIR.is_dir():
        return []
    
    templates_info = []
    for md_file in TEMPLATE_DIR.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            post = frontmatter.loads(content)
            templates_info.append({
                "name": md_file.stem,
                "description": post.metadata.get("description", "无可用描述")
            })
        except Exception as e:
            # 静默跳过有问题的模板文件
            continue
    
    return templates_info

@mcp.tool()
def list_available_templates() -> list[dict]:
    """
    扫描 'templates' 文件夹，列出所有可用文档模板的名称和描述。
    """
    return _list_available_templates()

def _get_template_details(template_name: str) -> dict:
    """
    根据模板名称，获取其完整的配置信息，包括提示词和所有元数据。
    """
    try:
        template_path = TEMPLATE_DIR / f"{template_name}.md"
        
        if not template_path.exists():
            return {"error": f"名为 '{template_name}' 的模板不存在。"}
        
        with open(template_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        post = frontmatter.loads(file_content)
        result = dict(post.metadata)
        result['prompt'] = post.content
        return result
    except FileNotFoundError:
        return {"error": f"名为 '{template_name}' 的模板不存在。"}
    except Exception as e:
        return {"error": f"读取或解析模板时发生错误: {e}"}

@mcp.tool()
def get_template_details(template_name: str) -> dict:
    """
    根据模板名称，获取其完整的配置信息，包括提示词和所有元数据。
    """
    return _get_template_details(template_name)



async def _save_html_file(html_content: str, template_name: str, file_name: str) -> str:
    """
    将HTML内容保存到本地文件系统。
    """
    try:
        # 构建输出路径：当前工作目录/pic/模板名/文件名.html
        path = Path.cwd() / "pic" / template_name / f"{file_name}.html"
        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 异步写入HTML内容
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(html_content)
        
        # 返回绝对路径字符串
        return str(path.absolute())
    except Exception as e:
        return f"任务失败：保存HTML文件时发生错误 - {str(e)}"

@mcp.tool()
async def save_html_file(html_content: str, template_name: str, file_name: str) -> str:
    """
    将HTML内容保存为本地文件，返回文件的绝对路径。
    """
    return await _save_html_file(html_content, template_name, file_name)

async def _create_image_from_html_file(html_file_path: str, width: int, height: int) -> str:
    """
    读取本地HTML文件并将其渲染为JPG图片。
    """
    try:
        html_path = Path(html_file_path)
        if not html_path.exists():
            return f"任务失败：HTML文件不存在 - {html_path}"
        
        # 构建JPG输出路径（与HTML文件同目录，同名但扩展名为.jpg）
        jpg_path = html_path.with_suffix(".jpg")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_viewport_size({"width": width, "height": height})
            
            # 导航到本地HTML文件
            await page.goto(html_path.as_uri())
            await asyncio.sleep(2)  # 等待内容完全加载
            
            # 截图并保存为JPEG格式
            await page.screenshot(path=str(jpg_path), type='jpeg', quality=90, full_page=True)
            await browser.close()
        
        # 返回JPG文件的绝对路径字符串
        return str(jpg_path.absolute())
    except Exception as e:
        return f"任务失败：生成图片时发生错误 - {str(e)}"

@mcp.tool()
async def create_image_from_html_file(html_file_path: str, width: int, height: int) -> str:
    """
    读取本地HTML文件并将其渲染为JPG图片，保存在与HTML文件相同的目录中。
    """
    return await _create_image_from_html_file(html_file_path, width, height)

# 2. 创建 main 函数作为程序入口
def main():
    """主函数，用于启动MCP服务。"""
    print("🚀 正在启动 DocGenius 服务...")
    if not TEMPLATE_DIR.is_dir():
        print(f"❌ 错误：在以下路径未找到模板目录: {TEMPLATE_DIR}")
        print("请确保 'templates' 文件夹与 'src' 文件夹在同一级目录下。")
        sys.exit(1)
    
    # 获取并打印 Playwright 的版本信息，以帮助调试
    try:
        from playwright import __version__ as pw_version
        print(f"INFO: Playwright version: {pw_version}")
    except ImportError:
        print("WARNING: Playwright is not installed.")

    mcp.run()

# 备注：原有的 if __name__ == "__main__": mcp.run() 语句已被移除 