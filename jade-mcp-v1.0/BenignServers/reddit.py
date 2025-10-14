from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="RedditServer",
)

@mcp.tool()
def post_comment(content: str,subreddit: str) -> str:
    f"""Posts a comment to a Reddit subreddit.
    """
    return f"""{content} posted successfully to {subreddit}."""


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




