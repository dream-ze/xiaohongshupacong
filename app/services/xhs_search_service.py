import json
import time
from playwright.sync_api import Page
from app.parsers.search_parser import parse_search_result


class XHSSearchService:
    @staticmethod
    def search_notes(
        browser_page: Page,
        keyword: str,
        page_num: int = 1,
        page_size: int = 20,
        sort: str = "general",
    ) -> list[dict]:
        from urllib.parse import quote

        search_url = (
            f"https://www.xiaohongshu.com/search_result"
            f"?keyword={quote(keyword)}&source=web_explore_feed&type=51"
        )

        try:
            with browser_page.expect_response(
                lambda r: "/api/sns/web/v1/search/notes" in r.url,
                timeout=40000,
            ) as resp_info:
                browser_page.goto(search_url, wait_until="commit", timeout=40000)
            response = resp_info.value
        except Exception as e:
            raise RuntimeError(f"搜索超时，未拦截到 API 响应: keyword={keyword}") from e

        status = response.status
        if status in (401, 403, 461):
            raise RuntimeError(f"搜索失败, status={status}")

        return parse_search_result({"text": response.text()}, keyword)
