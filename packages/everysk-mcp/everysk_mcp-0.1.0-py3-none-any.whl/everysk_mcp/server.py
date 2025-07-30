###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# https://github.com/modelcontextprotocol/python-sdk
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Everysk SSE for MCP")


## Tools that can be added to the MCP server
def hello() -> str:
    return "Hello, World!"


mcp.add_tool(hello)
