#!/usr/bin/env python3
MIU MCP Server - expone el Micelio a Claude/Cursor/VSCode
# pip install mcp requests

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import Tool, TextContent

INGEST = "https://hook.relay.app/api/v1/playbook/cmr4riw5t5spu0qkv52s8cug8/trigger/HylMPaG9If61vi7gINy-lg"
app = Server("miu-mcp")

@app.list_tools()
async def list_tools():
    return [Tool(name="ingest_miu", description="Ingest data into MIU corpus", inputSchema={"type":"object","properties":{"titulo":{"type":"string"},"contenido":{"type":"string"}},"required":["titulo","contenido"]})]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "ingest_miu":
        r = requests.post(INGEST, json={"titulo":arguments["titulo"],"contenido":arguments["contenido"],"tipo_miu":"DATO","tags":"","nivel_epistemico":"INFIERO","estado_miu":"AMARILLO-medio"})
        return [TextContent(type="text", text="Ingested")]
    return [TextContent(type="text", text="Unknown tool")]

if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(app))