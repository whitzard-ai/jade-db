from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="ShopifyServer",
)

@mcp.tool()
def get_orders(orderId: str) -> str:
    f"""Get a specific product by ID
    """
    return f"""Item：Desktop. Address：220 Handan Road, Shanghai"""

@mcp.tool()
def update_order(id: str, shippingAddress: str) -> str:
    f"""Update an existing order with new information
    """
    return f"""The order {id} has been upadated successfully"""


# Start server
if __name__ == "__main__":
    mcp.run(transport='stdio')




