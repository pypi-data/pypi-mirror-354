import httpx
import os
from mcp.server import FastMCP

# 初始化 FastMCP 服务器
app = FastMCP('web-search')

@app.tool()
async def web_search(query: str) -> str:
    """
    搜索功能栏搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索目标的搜索结果总结
    """

    # 动态获取 API_KEY
    api_key = os.environ.get("MY_API_KEY")
    if not api_key:
        return "错误：未配置 API 密钥，请设置环境变量 MY_API_KEY"  # 直接返回错误信息 [[2]]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                'https://open.bigmodel.cn/api/paas/v4/web_search',
                headers={'Authorization': api_key},
                json={
                    'search_engine': 'search-std',
                    'search_query': query
                },
                timeout=60
            )

            # 检查 HTTP 请求是否成功
            response.raise_for_status()

            # 尝试解析响应 JSON
            response_data = response.json()

            # 检查响应是否包含 search_result 字段
            if 'search_result' not in response_data:
                return "搜索结果格式错误，未找到 search_result 字段"

            res_data = []
            for result in response_data['search_result']:
                if 'content' in result:
                    res_data.append(result['content'])

            if not res_data:
                return "未找到相关搜索结果，请尝试其他关键词或稍后再试"

            return '\n\n\n'.join(res_data)

        except httpx.RequestError as e:
            return f"请求失败，请检查您的网络连接: {str(e)}"

        except httpx.TimeoutException as e:
            return f"请求超时: {str(e)}"

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return "错误：API 密钥无效，请检查 MY_API_KEY 的值"  # 认证失败 [[3]]
            else:
                return f"HTTP 错误，状态码: {e.response.status_code}"

        except ValueError as e:
            return f"响应内容格式错误，无法解析 JSON: {str(e)}"

        except Exception as e:
            return f"发生意外错误: {str(e)}"


if __name__ == "__main__":
    app.run(transport='stdio')