from playwright.sync_api import Page
from app.parsers.detail_parser import parse_note_detail_from_page


class XHSDetailService:
    @staticmethod
    def enrich_note_detail(
        browser_page: Page,
        note: dict,
        need_comments: bool = False,
        comment_limit: int = 5,
    ) -> dict:
        if not note.get("note_url"):
            return note

        detail = parse_note_detail_from_page(browser_page, note["note_url"])

        note["title"] = detail.get("title") or note.get("title", "")
        note["desc"] = detail.get("desc") or note.get("desc", "")
        note["content"] = detail.get("content", "")
        note["tags"] = detail.get("tags", [])
        note["cover_url"] = detail.get("cover_url") or note.get("cover_url", "")
        if detail.get("liked_count"):
            note["liked_count"] = detail["liked_count"]
        if detail.get("comment_count"):
            note["comment_count"] = detail["comment_count"]
        if detail.get("collect_count"):
            note["collect_count"] = detail["collect_count"]

        if need_comments:
            note["comments"] = XHSDetailService._mock_comments(comment_limit)
            note["comment_count"] = len(note["comments"])

        return note

    @staticmethod
    def _mock_comments(limit: int = 5) -> list[dict]:
        return [
            {
                "comment_id": f"mock_{i}",
                "user_name": f"user_{i}",
                "user_id": f"user_id_{i}",
                "content": f"示例评论{i}",
                "like_count": 0,
            }
            for i in range(1, limit + 1)
        ]
