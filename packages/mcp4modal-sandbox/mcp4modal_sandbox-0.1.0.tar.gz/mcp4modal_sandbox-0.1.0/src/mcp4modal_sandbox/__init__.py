import click 
import asyncio 

from mcp4modal_sandbox.backend.mcp_server import MCPServer
from mcp4modal_sandbox.settings import MCPServerSettings


@click.command()
@click.option("--transport", type=click.Choice(['stdio', 'streamable-http', 'sse']), default='stdio', help="The transport to use for the MCP server")
def main(transport: str = 'stdio'):
    mcp_settings = MCPServerSettings()  
    async def run_loop():
        mcp_server = MCPServer(mcp_settings)
        async with mcp_server as mcp:
            await mcp.run_mcp(transport)
    asyncio.run(run_loop())


if __name__ == "__main__":
    main()
