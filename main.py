from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
app = FastAPI()
mcp = FastMCP(name="my_server")
@mcp.tool()
def get_order_status(order_id: str):
    return {
        "status": "Shipped",
        "delivery": "2␣days"
    }