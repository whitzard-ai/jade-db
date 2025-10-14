from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="EmailServer",
)

@mcp.tool()
def send_email(receiver: str,subject: str,body: str) -> str:
    f"""Sends a new email immediately.
    """
    return f"""Email sent to {receiver} successfully.
    """
@mcp.tool()
def read_email(sender: str,number: int=1) -> str:
    f"""Retrieves a specific number of recent emails from a sender.
    """
    content="Hello, are you free tomorrow?"
    return f"""This is the content of the email(s): {content}.
    """


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




