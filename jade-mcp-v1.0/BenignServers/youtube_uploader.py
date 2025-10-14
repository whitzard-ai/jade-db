from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="YoutubeUploaderServer",
)


@mcp.tool()
def upload_video(sender: str) -> str:
    f"""Upload a video to YouTube.
    """
    result = "上传成功！"
    return result


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




