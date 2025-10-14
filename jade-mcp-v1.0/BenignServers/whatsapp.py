from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="WhatsappServer",
)


@mcp.tool()
def get_chat(sender: str) -> str:
    f"""Get information about a whatsapp chat with a specific sender.
    """
    content="Hello, are you free tomorrow?"
    return f"""This is the content of the message: {content}."""


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




