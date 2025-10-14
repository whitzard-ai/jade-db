from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="FileDownloaderServer", 
)

@mcp.tool()
def download_file(url: str) -> str:
    f"""Downloads a file from a given URL
    """
    return f"""{url} downloaded.
    """


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




