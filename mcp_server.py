import os
from typing import Any

import uuid
import requests
import json
import httpx
from mcp.server.fastmcp import FastMCP
import sensetive_data

mcp = FastMCP("mcp-server")

API_BASE_URL = os.environ["API_BASE_URL"]


async def make_request(
    url: str, method: str = "GET", data: dict[str, Any] = None
) -> dict[str, Any] | None:
    api_key = os.environ.get("API_KEY")
    if api_key:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
    else:
        headers = {}

    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.request(method, url, headers=headers, params=data)
        else:
            response = await client.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def open_locker_ticket() -> str:
    """
    Upon user's request you should open a new locker request
    """
    with open('payload.json', 'r') as f:
        payload = json.load(f)

    payload["variables"]["requested_for"] = uuid.uuid4().hex
    payload["sysparm_item_guid"] = uuid.uuid4().hex
    response = requests.post(
        sensetive_data.url, 
        json=payload, 
        headers=sensetive_data.headers, 
        cookies=sensetive_data.cookies,
        verify=True
    )
    nested_data = response.json()
    number = nested_data["result"]["number"]
    sys_id = nested_data["result"]["sys_id"]
    request_url = f"https://redhat.service-now.com/help?id=rh_ticket&table=x_redha_gws_table&sys_id={sys_id}"
    msg = f"""
    New ticket has been created
    Ticket Number: {number}
    Ticket URL: {request_url}
    """
    return msg

if __name__ == "__main__":
    mcp.run(transport=os.environ.get("MCP_TRANSPORT", "stdio"))
