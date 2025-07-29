import os
import sys
import logging
import httpx
from typing import Any

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logging.info("Starting Hunyuan Plugin MCP Server")

def fitRecall(arguments: dict[str, Any],api_key,domain) -> str:
    targetUrl = domain+"/openapi/betav1/tools/fit_recall"

    query = arguments.get("query", None)
    if query is None:
        raise ValueError("query不能为空")
    question = arguments.get("question", None)
    if question is None:
        raise ValueError("question不能为空")
    data_type = arguments.get("data_type", None)
    if data_type is None:
        raise ValueError("data_type不能为空")
    se_params = arguments.get("se_params", None)
    extra_params= arguments.get("extra_params", None)
    payload = {
        "query": query,
        "question":question,
        "data_type":data_type,
        "se_params":se_params,
        "extra_params":extra_params
    }

    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    logging.info("start to call hunyuan plugin api:", payload)
    timeout = httpx.Timeout(90.0, connect=10.0)
    response = httpx.post(targetUrl, headers=headers, json=payload, timeout=timeout)
    response_json = response.json()
    if response.status_code == 401:
        raise SystemError("token验证失败")
    if response.status_code != 200:
        error_info = response_json.get("error", None)
        if error_info is None:
            raise SystemError(f"请求服务器失败，错误码{response.status_code}")
        else:
            err_msg = error_info.get("message", "未知错误")
            raise SystemError(f"请求服务器失败，{err_msg}")
        
    logging.info("hunyuan openapi response:", response_json)
    err_code = response_json.get("code", 0)
    if err_code != 0:
        raise SystemError(f"Fit股票接口异常，请稍后重试{err_code}")
    return str(response.content, encoding='utf-8')

def exchange(arguments: dict[str, Any],api_key,domain) -> str:
    targetUrl = domain+"/openapi/betav1/tools/exchange_rate"

    fromC = arguments.get("from", None)
    if fromC is None:
        raise ValueError("from不能为空")
    to = arguments.get("to", None)
    if to is None:
        raise ValueError("to不能为空")
    
    money = arguments.get("money", None)
    if money is None:
        raise ValueError("money不能为空")
    payload = {
        "fromC": fromC,
        "to":to,
        "money":money
    }

    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    logging.info("start to call hunyuan plugin api:", payload)
    timeout = httpx.Timeout(90.0, connect=10.0)
    response = httpx.post(targetUrl, headers=headers, json=payload, timeout=timeout)
    response_json = response.json()
    if response.status_code == 401:
        raise SystemError("token验证失败")
    if response.status_code != 200:
        error_info = response_json.get("error", None)
        if error_info is None:
            raise SystemError(f"请求服务器失败，错误码{response.status_code}")
        else:
            err_msg = error_info.get("message", "未知错误")
            raise SystemError(f"请求服务器失败，{err_msg}")
        
    logging.info("hunyuan openapi response:", response_json)
    err_code = response_json.get("code", 0)
    if err_code != 0:
        raise SystemError(f"汇率查询接口异常，请稍后重试{err_code}")
    return str(response.content, encoding='utf-8')

def stock(arguments: dict[str, Any],api_key,domain) -> str:
    targetUrl = domain+"/openapi/betav1/tools/stock"

    query = arguments.get("query", None)
    if query is None:
        raise ValueError("query不能为空")
    inner = arguments.get("inner", None)
    if inner is None:
        raise ValueError("inner不能为空")
    payload = {
        "query": query,
        "inner":inner
    }

    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    logging.info("start to call hunyuan plugin api:", payload)
    timeout = httpx.Timeout(90.0, connect=10.0)
    response = httpx.post(targetUrl, headers=headers, json=payload, timeout=timeout)
    response_json = response.json()
    if response.status_code == 401:
        raise SystemError("token验证失败")
    if response.status_code != 200:
        error_info = response_json.get("error", None)
        if error_info is None:
            raise SystemError(f"请求服务器失败，错误码{response.status_code}")
        else:
            err_msg = error_info.get("message", "未知错误")
            raise SystemError(f"请求服务器失败，{err_msg}")
        
    logging.info("hunyuan openapi response:", response_json)
    err_code = response_json.get("code", 0)
    if err_code != 0:
        raise SystemError(f"股票接口异常，请稍后重试{err_code}")
    return str(response.content, encoding='utf-8')

async def main():
    logging.info("Starting hunyuan Plugin MCP Server.")
    
    server = Server("hunyuan-mcp-finance", "0.0.11", "mcp server to invoke hunyuan finance")
    
    # Register handlers
    logging.debug("Registering handlers")
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="stock",
                description="股票查询接口",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string", 
                            "description": "用户的搜索查询词列表。查询词不能为空。"
                        },
                        "inner":{
                            "type": "int", 
                            "description": "0：外部用户t1行情，1：内部用户t0行情"
                        }
                    },
                    "required": ["query","inner"],
                },
            ),
            types.Tool(
                name="exchange_rate",
                description="汇率兑换",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "from": {
                            "type": "string", 
                            "description": "待兑换的币种",
                        },
                        "to": {
                            "type": "string", 
                            "description": "目标币种",
                        },
                        "money": {
                            "type": "string", 
                            "description": "兑换金额",
                        }
                    },
                    "required": ["from","to","money"],
                },
            ),
            types.Tool(
                name="fit_recall",
                description="fit股票接口",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string", 
                            "description": "用户问题",
                        },
                        "question": {
                            "type": "string", 
                            "description": "用户问题",
                        },
                        "data_type": {
                            "type": "string", 
                            "description": "all:api+文章；api只召回api数据；doc:只召回文章数据",
                        },
                        "se_params": {
                            "type": "object",
                            "additionalProperties": True,
                        },
                        "extra_params": {
                            "type": "object",
                            "additionalProperties": True,
                        }
                    },
                    "required": ["query","question","data_type"],
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            env = os.getenv("ENV", "prod")
            if env == "test":
                domain="http://120.241.140.192"
            else:
                domain="https://hunyuan-agent.tencent.com"

            if name == "fit_recall":
                 api_key = os.getenv("FIT_RECALL_API_KEY", None)
                 if api_key is None:
                     return ValueError("环境变量FIT_RECALL_API_KEY没有设置")
                 results = fitRecall(arguments,api_key,domain)
                 return [types.TextContent(type="text", text=str(results))]
            elif name == "stock":
                 api_key = os.getenv("STOCK_API_KEY", None)
                 if api_key is None:
                     return ValueError("环境变量STOCK_API_KEY没有设置")
                 results = stock(arguments,api_key,domain)
                 return [types.TextContent(type="text", text=str(results))]
            elif name == "exchange_rate":
                 api_key = os.getenv("EXCHANGE_RATE_API_KEY", None)
                 if api_key is None:
                     return ValueError("环境变量EXCHANGE_RATE_API_KEY没有设置")
                 results = exchange(arguments,api_key,domain)
                 return [types.TextContent(type="text", text=str(results))]
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            raise e # [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with stdio_server() as (read_stream, write_stream):
        logging.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hunyuan-mcp-finance", 
                server_version="0.0.11",
                server_instructions="mcp server to invoke hunyuan finance",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

class ServerWrapper():
    """A wrapper to compat with mcp[cli]"""
    def run(self):
        import asyncio
        asyncio.run(main())


wrapper = ServerWrapper()