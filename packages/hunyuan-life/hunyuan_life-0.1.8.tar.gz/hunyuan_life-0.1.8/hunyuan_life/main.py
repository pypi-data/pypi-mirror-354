from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import os
import logging
import httpx
from dataclasses import dataclass, asdict
from typing import Any, Optional, List, Dict, Annotated
from pydantic import Field

# from .exceptions import *

# Initialize FastMCP server
mcp = FastMCP(
    "hunyuan-life",
    host="0.0.0.0",
    port=os.getenv("PORT", 8000)
)

@mcp.tool(
    description="""日历查询插件
        
    Args:
        time: 用户的搜索内容，不能为空。

    Returns:
        dict: 包含生成的查询结果的字典
    """
)
async def calendar( 
    time: str = Field(description="用户的搜索内容，不能为空。"),
):
    
    api_key = os.getenv("CALENDAR_API_KEY", "")
    if api_key is None:
        raise ValueError("环境变量CALENDAR_API_KEY没有设置")
    
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
    
    # calendar_url = "http://11.145.140.98:8000/openapi/betav1/tools/calendar"
    calendar_url = domain+"/openapi/betav1/tools/calendar"

    payload = {
        "time": time
    }

    logging.info(f"日历查询插件")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(calendar_url, headers=headers, json=payload, timeout=timeout)
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
    

@mcp.tool(
    description="""天气查询插件
        
    Args:
        city_name: 查询城市名，不能为空
        api_type: forecast15days: 天气预报15天 condition: 天气实况

    Returns:
        dict: 包含生成的查询结果的字典
    """
)
async def weather( 
    city_name: str = Field(description="查询城市名，不能为空"),
    api_type: str = Field(description="forecast15days: 天气预报15天 condition: 天气实况")
):
    
    api_key = os.getenv("WEATHER_API_KEY", "")
    if api_key is None:
        raise ValueError("环境变量WEATHER_API_KEY没有设置")
    
    env = os.getenv("ENV", "prod")
    if env == "test":
        domain = "http://120.241.140.192"
        # domain = "http://11.145.157.98:8000"
    else:
        domain = "https://agent.hunyuan.tencent.com"

    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    
    # weather_url = "http://11.145.140.98:8000/openapi/betav1/tools/weather"
    weather_url = domain+"/openapi/betav1/tools/weather"

    payload = {
        "city_name": city_name,
        "api_type": api_type
    }

    logging.info(f"天气查询插件")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(weather_url, headers=headers, json=payload, timeout=timeout)
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
    logging.info("开始运行hunyuan-life插件")
    run_mcp()
