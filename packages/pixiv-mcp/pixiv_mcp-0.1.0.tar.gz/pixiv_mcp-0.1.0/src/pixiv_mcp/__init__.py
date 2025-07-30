import random
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# 日志配置（保持与MCP服务兼容）
# logging.basicConfig(
#     level=logging.WARNING,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[logging.NullHandler()]
# )

mcp = FastMCP(
    name="pixiv-tool",
    version="1.0.0",
    description="Pixiv热门作品查询服务"
)


class PixivService:
    def __init__(self):
        self.config = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }
        self.session = self._create_session()

    def _create_session(self):
        """创建带自动重试的HTTP会话"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    async def fetch_random_artwork(self, tag: str) -> Dict[str, Any]:
        try:
            url = f"https://pixiv.navirank.com/search/?words={tag}"
            response = self.session.get(url, headers={'user-agent': self.config['user_agent']})
            soup = BeautifulSoup(response.text, 'html.parser')

            rank_all_div = soup.find('div', id='rank_all')

            artworks = [
                href.split('/')[2]
                for href in (a.get('href') for a in rank_all_div.select('li.rank ul.irank li.img a')[:20])
                if href and href.startswith('/id/')
            ]

            if not artworks:
                return {"status": "error", "message": "未找到相关作品"}

            artwork_id = random.choice(artworks)

            return {
                "status": "success",
                "data": {
                    "tag": tag,
                    "artwork_id": artwork_id,
                    "url": f"https://www.pixiv.net/artworks/{artwork_id}"
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


service = PixivService()


@mcp.tool(description="根据标签(tag)获取Pixiv热门图片,如果标签是中文尽量转换成pixiv中对应的日文tag作为该工具的输入", name="fetch_random_artwork")
async def get_hot_artwork(tag: str) -> Dict[str, Any]:
    """
    根据标签（tag）获取Pixiv热门图片
    Args:
        tag: 搜索标签（如"ブルーアーカイブ"）
    Returns:
        {
            "status": "success"|"error",
            "data": {
                "tag": str,
                "artwork_id": str,
                "url": str
            }
        }
    """
    return await service.fetch_random_artwork(tag)


def main() -> None:
    mcp.run(transport="stdio")
