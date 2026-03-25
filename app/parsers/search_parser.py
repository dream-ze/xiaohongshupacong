import json
from urllib.parse import quote


def safe_int(value, default=0):
    try:
        if value is None:
            return default
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return int(value)
    except Exception:
        return default


def parse_search_result(raw_result: dict, keyword: str) -> list[dict]:
    text = raw_result.get("text", "")
    if not text:
        return []

    try:
        data = json.loads(text)
    except Exception:
        return []

    data_block = data.get("data", {}) or {}
    items = data_block.get("items", []) or data_block.get("notes", []) or []

    result = []
    for item in items:
        note_card = item.get("note_card", {}) if isinstance(item, dict) else {}
        user_info = note_card.get("user", {}) if note_card else {}
        xsec_token = item.get("xsec_token", "")

        note_id = item.get("id") or note_card.get("note_id") or item.get("note_id") or ""
        title = note_card.get("display_title") or note_card.get("title") or item.get("title", "")
        desc = note_card.get("desc", "") or item.get("desc", "")
        author_name = user_info.get("nickname") or user_info.get("nick_name") or item.get("author_name", "")
        author_id = user_info.get("user_id", "") or item.get("author_id", "")

        interact_info = note_card.get("interact_info", {}) if note_card else {}
        liked_count = safe_int(interact_info.get("liked_count", 0))

        cover_url = ""
        cover = note_card.get("cover")
        if isinstance(cover, dict):
            cover_url = cover.get("url_default") or cover.get("url", "")
        if not cover_url:
            image_list = note_card.get("image_list", [])
            if image_list and isinstance(image_list, list):
                first_image = image_list[0]
                if isinstance(first_image, dict):
                    cover_url = first_image.get("url_default", "") or first_image.get("url", "")

        note_url = ""
        if note_id and xsec_token:
            encoded_token = quote(str(xsec_token), safe="")
            note_url = (
                f"https://www.xiaohongshu.com/explore/{note_id}"
                f"?xsec_token={encoded_token}&xsec_source=pc_search"
            )

        result.append({
            "keyword": keyword,
            "note_id": note_id,
            "title": title,
            "desc": desc,
            "content": "",
            "author_name": author_name,
            "author_id": author_id,
            "liked_count": liked_count,
            "comment_count": 0,
            "collect_count": 0,
            "share_count": 0,
            "note_url": note_url,
            "cover_url": cover_url,
            "tags": [],
            "comments": [],
            "raw_json": item,
        })

    return result
