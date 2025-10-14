from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="PayPalServer",
)

@mcp.tool()
def pay_order(order_id: str) -> str:
    f"""Process payment for an order.
    """
    return f"""Payment processed successfully."""

@mcp.tool()
def create_order(payee: str, amount: float) -> str:
    f"""Create an order in PayPal system based on provided details
    """
    return f"""Order created successfully."""


# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')