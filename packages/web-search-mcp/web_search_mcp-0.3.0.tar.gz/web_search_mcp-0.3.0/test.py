# 使用stdio连接的最简单客户端实现
import asyncio  
from mcp import ClientSession, StdioServerParameters  
from mcp.client.stdio import stdio_client  
  
async def run_client():  
    # 创建服务器参数（指定要连接的服务器）  
    server_params = StdioServerParameters(  
        command="uv",  # 可执行文件  
        args=['run', 'src/web_search_mcp/server.py'],  # 服务器脚本路径  
        env={"MY_API_KEY": "872bd5f2dfbc41ab8f98a144b55dff17.LxIjFg5oSMrhY22B"}  # 环境变量（可选）  
    )  
      
    # 连接到服务器  
    async with stdio_client(server_params) as (read, write):  
        # 创建客户端会话  
        async with ClientSession(read, write) as session:  
            # 初始化连接  
            await session.initialize()  
            print("连接初始化成功")  
              
            # 列出可用工具  
            tools = await session.list_tools()  
            print(f"可用工具: {tools}")  
              
            # 调用工具示例  
            result = await session.call_tool("web_search", {"query": "今天杭州天气怎么样"})  
            print(f"工具调用结果: {result}")  
              
            # # 列出可用资源  
            # resources = await session.list_resources()  
            # print(f"可用资源: {resources}")  
              
            # # 读取资源示例  
            # resource = await session.read_resource("resource://example")  
            # print(f"资源内容: {resource}")  
  
if __name__ == "__main__":  
    asyncio.run(run_client())