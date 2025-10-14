from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="ZhihuServer",
)


@mcp.tool()
def modify_personal_introduction(new_introduction: str) -> str:
    f"""Modify personal introduction on Zhihu.
    """
    result = "Personal introduction modified successfully!"
    return result


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




