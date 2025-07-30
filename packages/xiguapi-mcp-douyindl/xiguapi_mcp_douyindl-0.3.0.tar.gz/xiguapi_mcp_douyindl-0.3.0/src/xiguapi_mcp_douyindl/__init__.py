# server.py
import json
from mcp.server.fastmcp import FastMCP
from DrissionPage import ChromiumPage, ChromiumOptions
# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def get_video_url(url: str) -> str:
    """Get douyin video download url """
    co = ChromiumOptions().headless()
    browser = ChromiumPage(co)
    browser.listen.start(r'/aweme/v1/web/aweme/detail/')
    browser.get(url)
    resp = browser.listen.wait()
    json_data = resp.response.body
    aweme_detail = json_data.get('aweme_detail') or json_data.get('data', {})
    video_info = aweme_detail.get('video', {})
    play_addr = video_info.get('play_addr', {})
    url_list = play_addr.get('url_list', [])
    video_url = url_list[2].replace('playwm', 'play') if url_list else ''

    browser.quit()
    return json.dumps({'video_url': video_url})


def main() -> None:
     mcp.run(transport="stdio")
