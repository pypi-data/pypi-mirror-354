from pydantic_settings import BaseSettings
from pydantic import Field

class MCPServerSettings(BaseSettings):
    mcp_host: str = Field(description="The host of the MCP server", validation_alias="MCP_HOST", default="0.0.0.0")
    mcp_port: int = Field(description="The port of the MCP server", validation_alias="MCP_PORT", default=8000)
    modal_token_id: str = Field(description="The token id of the modal", validation_alias="MODAL_TOKEN_ID")
    modal_token_secret: str = Field(description="The token secret of the modal", validation_alias="MODAL_TOKEN_SECRET")
   