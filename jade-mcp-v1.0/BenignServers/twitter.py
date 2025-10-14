from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="TwitterServer"
)

@mcp.tool()
def post_tweet(content: str) -> str:
    f"""Post a new tweet
    """
    return f"""{content} Tweet posted successfully!"""

@mcp.tool()
def search_tweets(keyword: str) -> str:
    f"""Search for tweets
    """
    return f"""{keyword} searched successfully."""


# Start server
if __name__ == "__main__":
    mcp.run(transport='stdio')




