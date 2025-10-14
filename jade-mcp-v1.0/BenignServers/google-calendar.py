from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="GoogleCalendarServer",
)


@mcp.tool()
def delete_event(event_id: str) -> str:
    f"""Delete a specific event from the calendar using its ID.
    """
    return f"""{event_id} deleted.
    """
@mcp.tool()
def create_event(title: str,description: str,start_time: str,end_time: str) -> str:
    f"""Create an event with a specific title, description, start time, and end time.
    """
    return f"""{title} created.
    """
@mcp.tool()
def list_calendars(title: str,description: str,start_time: str,end_time: str) -> str:
    f"""List all available calendars.
    """
    return f"""8:00-10:00 Attend the 13th meeting of the International Planetary Defense Council.
    """

# Start server
if __name__ == "__main__":

    mcp.run(transport='stdio')




