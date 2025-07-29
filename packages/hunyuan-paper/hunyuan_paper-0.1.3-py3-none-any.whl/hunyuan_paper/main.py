from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import os
import logging
import os
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import httpx
from dataclasses import dataclass, asdict
from typing import Any, Optional, List, Dict, Annotated
from pydantic import Field

# Initialize FastMCP server
mcp = FastMCP(
    "hunyuan-paper",
    host="0.0.0.0",
    port=os.getenv("PORT", 8000)
)

@mcp.tool(
    description="""维普论文搜索插件
        
    Args:
        prompt: 维普论文的id，不是检索串

    Returns:
        dict: 包含生成的查询结果的字典
    """
)
async def paper( 
    prompt: str = Field(description="维普论文的id，不是检索串")
):
    
    api_key = os.getenv("PAPER_API_KEY", "")
    if api_key is None:
        raise ValueError("环境变量PAPER_API_KEY没有设置")
    
    env = os.getenv("ENV", "prod")
    if env == "test":
        domain="http://120.241.140.192"
    else:
        domain="https://agent.hunyuan.tencent.com"


    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    
    # paper_url = "http://11.145.136.93:8000/openapi/betav1/tools/paper"
    paper_url = domain+"/openapi/betav1/tools/paper"

    payload = {
        "prompt": prompt
    }

    logging.info(f"维普论文搜索插件")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(paper_url, headers=headers, json=payload, timeout=timeout)
        response_json = response.json()
        if "error" in response_json:
            error_data = response_json["error"]
            return TextContent(
                type="text",
                text=str(error_data)
            )
        
        return response_json
        
    except Exception as e:
        return TextContent(
            type="text",
            text=f"调用工具失败: {str(e)}"
        )


def run_mcp():
    print("starting")
    if os.getenv("TYPE") == "sse":
        print("starting sse")
        mcp.run(transport="sse")
    else:
        print("starting stdio")
        mcp.run(transport="stdio")

if __name__ == '__main__':
    print("starting main")
    logging.info("开始运行hunyuan-paper插件")
    run_mcp()
