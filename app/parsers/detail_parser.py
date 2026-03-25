import re

from playwright.sync_api import Page


def parse_note_detail_from_page(page: Page, note_url: str) -> dict:
    """
    访问笔记详情页，从页面 SSR 嵌入的 window.__INITIAL_STATE__ 提取数据。
    """
    page.goto(note_url, wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(1000)

    try:
        initial_state = page.evaluate("() => window.__INITIAL_STATE__")
    except Exception:
        return {"note_url": note_url}

    if not initial_state:
        return {"note_url": note_url}

    return _parse_initial_state(initial_state, note_url)


# ---------------------------------------------------------------------------
# 内部工具函数
# ---------------------------------------------------------------------------

def _safe_int(value, default: int = 0) -> int:
    try:
        return int(str(value).replace(",", "").strip())
    except Exception:
        return default


def _parse_initial_state(state: dict, note_url: str) -> dict:
    note_detail_map = (state.get("note") or {}).get("noteDetailMap") or {}

    note_data: dict = {}
    for entry in note_detail_map.values():
        note_data = (entry or {}).get("note") or {}
        break

    if not note_data:
        return {"note_url": note_url}

    title: str = note_data.get("title", "") or ""
    desc: str = note_data.get("desc", "") or ""

    tag_list = note_data.get("tagList") or []
    tags = [
        f"#{t['name']}"
        for t in tag_list
        if isinstance(t, dict) and t.get("name")
    ][:10]
    if not tags:
        tags = [f"#{t}" for t in re.findall(r"#([^\s#\u3000]+)", desc)][:10]

    image_list = note_data.get("imageList") or []
    cover_url = ""
    if image_list and isinstance(image_list[0], dict):
        cover_url = image_list[0].get("urlDefault") or image_list[0].get("url", "")

    interact_info = note_data.get("interactInfo") or {}
    return {
        "title": title,
        "desc": desc,
        "content": desc,
        "tags": tags,
        "cover_url": cover_url,
        "note_url": note_url,
        "liked_count": _safe_int(interact_info.get("likedCount", 0)),
        "comment_count": _safe_int(interact_info.get("commentCount", 0)),
        "collect_count": _safe_int(interact_info.get("collectCount", 0)),
    }


