from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="GitHubServer",
)

@mcp.tool()
def create_or_update_file(content: str, path: str) -> str:
    f"""Create or update a single file in a GitHub repository.
    """
    return f"""Create or update file successfully."""


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')