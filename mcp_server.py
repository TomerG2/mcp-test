import os
from typing import Any

import uuid
import requests
import json
import httpx
from mcp.server.fastmcp import FastMCP

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

url = "https://redhat.service-now.com/api/sn_sc/v1/servicecatalog/items/a4d32a92978299907d14f0f3a253af04/submit_producer"

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://redhat.service-now.com',
    'Referer': 'https://redhat.service-now.com/help?id=sc_cat_item&sys_id=a4d32a92978299907d14f0f3a253af04&help_type=team_storage&locker_request_type=request_dedicated_locker',
    'X-Transaction-Source': 'Interface=Web,Interface-Name=HELP,Interface-Type=Service Portal,Interface-SysID=518cc8391381db00dce03ff18144b009',
    'X-Use-Polaris': 'false',
    'X-UserToken': '8e27e359933122587df0bfbd1dba10f101a6992de9ae3f8a011e977ae91fe27ce0271a63',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

cookies = {
    'BIGipServerpool_redhat': 'c6046cc0c0b394e313ba1f7301da472c',
    'glide_node_id_for_js': '49d60ca9f5c58bfe6f7b414038e444bb347deed96d0841cb9e834df0baaa3f01', 
    'glide_session_store': '4E27E359933122587DF0BFBD1DBA10F1',
    'glide_sso_id': '80188381db95eb80a16700b5ca961985',
    'glide_user_activity': 'U0N2M18xOlo4ZXlIUVpuRnozdVYwaGlET3dTUGxoK3dmd3J0a2tJWkNzOEMvT3VheVU9OjRDWTcxdmllOTNCMGd6QjlCNzVXWTB4ZVJ6eG1vcXhvcjNOOENQaXNQd3M9',
    'glide_user_route': 'glide.578b231312d45d082563807c0af6537f',
    'JSESSIONID': 'E12EB2A4EEA71C8DB3B1763BE829F52E',
    'vaChat': 'va-visited'
}

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
        url, 
        json=payload, 
        headers=headers, 
        cookies=cookies,
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
