import base64
import datetime
import io
import logging
import os
from typing import Union

from PIL import Image
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .prompt import list_api_prompt_template
from .prompt import describe_image_prompt
from .utils.image import image_to_base64, url_to_base64, validate_base64_image
from .utils.ocr import OCRError, extract_text_from_image
from .vision.anthropic import AnthropicVision
from .vision.cloudflare import CloudflareWorkersAI
from .vision.openai import OpenAIVision

# Load environment variables
load_dotenv()

# Configure encoding, defaulting to UTF-8
DEFAULT_ENCODING = "utf-8"
ENCODING = os.getenv("MCP_OUTPUT_ENCODING", DEFAULT_ENCODING)

# Configure logging to file
log_file_path = os.path.join(os.path.dirname(__file__), "mcp_server.log")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_file_path,
    filemode="a",  # Append to log file
)
logger = logging.getLogger(__name__)

logger.info(f"Using encoding: {ENCODING}")


def sanitize_output(text: str) -> str:
    """Sanitize output string to replace problematic characters."""
    if text is None:
        return ""  # Return empty string for None
    try:
        return text.encode(ENCODING, "replace").decode(ENCODING)
    except Exception as e:
        logger.error(f"Error during sanitization: {str(e)}", exc_info=True)
        return text  # Return original text if sanitization fails


# Create MCP server
mcp = FastMCP(
    "szetop-mcp-dev",
    description="易图代码生成服务：支持识别设计图或 UI 效果图中的参数与字段，可用于生成代码提示词（Prompt）或直接提取界面内容。",
)


# Initialize vision clients
def get_vision_client() -> Union[AnthropicVision, OpenAIVision, CloudflareWorkersAI]:
    """Get the configured vision client based on environment settings."""
    provider = os.getenv("VISION_PROVIDER", "anthropic").lower()

    try:
        if provider == "anthropic":
            return AnthropicVision()
        elif provider == "openai":
            return OpenAIVision()
        elif provider == "cloudflare":
            return CloudflareWorkersAI()
        else:
            raise ValueError(f"Invalid vision provider: {provider}")
    except Exception as e:
        # Try fallback provider if configured
        fallback = os.getenv("FALLBACK_PROVIDER")
        if fallback and fallback.lower() != provider:
            logger.warning(
                f"Primary provider failed: {str(e)}. Trying fallback: {fallback}"
            )
            if fallback.lower() == "anthropic":
                return AnthropicVision()
            elif fallback.lower() == "openai":
                return OpenAIVision()
            elif fallback.lower() == "cloudflare":
                return CloudflareWorkersAI()
        raise


async def process_image_with_ocr(image_data: str, prompt: str) -> str:
    """Process image with both vision AI and OCR.

    Args:
        image_data: Base64 encoded image data
        prompt: Prompt for vision AI

    Returns:
        str: Combined description from vision AI and OCR
    """
    # Get vision AI description
    client = get_vision_client()

    # Handle both sync (Anthropic) and async (OpenAI, Cloudflare) clients
    if isinstance(client, (OpenAIVision, CloudflareWorkersAI)):
        description = await client.describe_image(image_data)
    else:
        description = client.describe_image(image_data)

    # Check for empty or default response
    if not description or description == "No description available.":
        raise ValueError("Vision API returned empty or default response")

    # Handle OCR if enabled
    ocr_enabled = os.getenv("ENABLE_OCR", "false").lower() == "true"
    if ocr_enabled:
        try:
            # Convert base64 to PIL Image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Extract text with OCR required flag
            if ocr_text := extract_text_from_image(image, ocr_required=True):
                description += (
                    f"\n\nAdditionally, this is the output of tesseract-ocr: {ocr_text}"
                )
        except OCRError as e:
            # Propagate OCR errors when OCR is enabled
            logger.error(f"OCR processing failed: {str(e)}")
            raise ValueError(f"OCR Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during OCR: {str(e)}")
            raise

    return sanitize_output(description)


@mcp.tool()
async def describe_image(
        image: str
) -> str:
    """
    识别并描述来自 Base64 编码图像的数据内容，适用于用户通过聊天窗口上传的图片。

    Best for: 当前对话中直接上传的图片（无公共 URL 时使用）。
    Not suitable for: 本地文件路径或公网链接图像，请使用 describe_image_from_file 工具。

    Args:
        image (str): 图像的 Base64 编码字符串（如 data:image/png;base64,...）

    Returns:
        str: 图像内容的详细自然语言描述，适用于提取页面字段、UI 布局、结构分析等任务。
    """
    try:
        logger.info(f"Processing image description request with prompt: {describe_image_prompt}")
        logger.debug(f"Image data length: {len(image)}")

        # Validate image data
        if not validate_base64_image(image):
            raise ValueError("Invalid base64 image data")

        result = await process_image_with_ocr(image, describe_image_prompt)
        if not result:
            raise ValueError("Received empty response from processing")

        logger.info("Successfully processed image")
        return sanitize_output(result)
    except ValueError as e:
        logger.error(f"Input error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error describing image: {str(e)}", exc_info=True)
        raise


@mcp.tool()
async def describe_image_from_file(
        filepath: str
) -> str:
    """
    识别本地设计图或 UI 效果图中的关键信息，包括接口参数和响应字段。

    Best for: 本地文件系统中存储的图片（如 UI 设计图、页面原型图、接口草图等）。
    Not suitable for: 直接在对话中上传的图片或网络 URL，请使用 describe_image 工具。

    Args:
        filepath (str): 图像文件的绝对路径，例如：/home/user/images/example.png 或 C:\\Users\\user\\Desktop\\ui.png

    Returns:
        str: 图像中提取的详细内容描述，包含推测的接口请求参数、响应字段及其含义，可用于自动生成 DTO/VO 类或接口草图。
    """
    try:
        logger.info(f"Processing image file: {filepath}")

        # Convert image to base64
        image_data, mime_type = image_to_base64(filepath)
        logger.info(f"Successfully converted image to base64. MIME type: {mime_type}")
        logger.debug(f"Base64 data length: {len(image_data)}")

        # Use describe_image tool
        result = await describe_image(image=image_data)

        if not result:
            raise ValueError("Received empty response from processing")

        return sanitize_output(result)
    except FileNotFoundError:
        logger.error(f"Image file not found: {filepath}")
        raise
    except ValueError as e:
        logger.error(f"Input error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing image file: {str(e)}", exc_info=True)
        raise


@mcp.tool()
async def describe_image_from_url(
        url: str
) -> str:
    """
    从公网图片 URL 中识别图像内容，适用于 UI 设计图、接口草图等，提取接口参数与响应字段信息。

    Best for: 可公开访问的图像 URL（如部署在 OSS、图床、CDN 上的设计图）。
    Not suitable for: 本地文件或用户直接上传到对话中的图片，请使用 describe_image_from_file 或 describe_image。

    Args:
        url (str): 图像的公网直链地址，需确保该链接可被服务器访问，例如 https://example.com/images/mock.png

    Returns:
        str: 对图像的结构化描述，包含推测的接口字段、参数、页面元素等信息，适用于自动生成 DTO/VO 类或接口设计草稿。
    """
    try:
        logger.info(f"Processing image from URL: {url}")

        # Fetch image from URL and convert to base64
        image_data, mime_type = url_to_base64(url)
        logger.info(f"Successfully fetched image from URL. MIME type: {mime_type}")
        logger.debug(f"Base64 data length: {len(image_data)}")

        # Use describe_image tool
        result = await describe_image(image=image_data)

        if not result:
            raise ValueError("Received empty response from processing")

        return sanitize_output(result)
    except ValueError as e:
        logger.error(f"Input error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing image from URL: {str(e)}", exc_info=True)
        raise


@mcp.tool()
async def get_list_api_prompt(filepath: str, entities: dict) -> str:
    """
    从 UI 设计图或原型图中生成构建列表页（含分页查询接口）所需的提示词（prompt），用于自动生成 Java 代码。

    This tool analyzes the visual layout from a design or prototype image and maps it to backend data structures
    to generate code generation prompts for list pages and paginated query APIs.

    Args:
       filepath (str): 本地图像文件的绝对路径，例如：
            - Linux/macOS: /home/user/images/example.png
            - Windows: C:\\Users\\user\\Desktop\\ui.png

       entities (dict): 实体字段结构，格式如下：{"表名1": [{"name": "字段名", "type": "字段类型", "comment": "字段说明"},...],...} 通常从数据库建模工具或后端实体类中提取，作为字段映射参考。
    Returns:
        str: 用于构建 Controller、Service、DTO、VO、Mapper 的自然语言提示词，适用于自动代码生成。
    """
    if entities is None:
        raise TypeError("请选择对应实体类")

    image_desc = await describe_image_from_file(filepath)
    logger.info(f"Image description: {image_desc}")
    params, fields = extract_params_and_fields(image_desc)

    entity_prompt = ""
    for table_name in entities:
        entity = entities[table_name]
        entity_prompt += """| 字段名 | 字段类型 | 字段备注 |
        | ---- | ---- | ---- |
        """
        for field in entity:
            entity_prompt += f'|{field["name"]}|{field["type"]}|{field["comment"]}|\n'

    param_prompt = ''
    if params:
        for item in params:
            param_prompt += f'|{item["label"]}|{item["widget"]}|{item["required"]}|\n'

    result_prompt = ''
    if fields:
        result_prompt += str.join(', ', fields)

    prompt = (list_api_prompt_template
              .replace("{{entity}}", entity_prompt)
              .replace("{{param_prompt}}", param_prompt)
              .replace("{{result_prompt}}", result_prompt)
              .replace("${date}", str(datetime.date.today()))
              )
    return prompt


import re
from typing import List, Dict, Tuple


def extract_params_and_fields(text: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    从给定文本中提取参数和字段信息。

    参数格式示例（在 <参数> 标签之间）：
    项目名称|输入框|非必填

    字段格式示例（在 <字段> 标签之间）：
    [序号, 项目名称, 行政区, ...]

    Args:
        text (str): 包含 <参数> 和 <字段> 块的原始文本

    Returns:
        Tuple[List[Dict[str, str]], List[str]]:
            - 参数列表，每个参数为 {"label": str, "widget": str, "required": str}
            - 字段名列表
    """

    # 提取参数块
    param_block_match = re.search(r"<参数>(.*?)</参数>", text, re.DOTALL)
    param_list = []
    if param_block_match:
        param_lines = param_block_match.group(1).strip().splitlines()
        for line in param_lines:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 3:
                param_list.append({
                    "label": parts[0],
                    "widget": parts[1],
                    "required": parts[2]
                })

    # 提取字段块
    field_block_match = re.search(r"<字段>\s*\[(.*?)\]\s*</字段>", text, re.DOTALL)
    fields = []
    if field_block_match:
        field_raw = field_block_match.group(1)
        fields = [f.strip() for f in field_raw.split(",")]

    return param_list, fields


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
