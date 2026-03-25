import json
from sqlalchemy.orm import Session
from app.models.xhs_note import XHSNote, XHSComment


class XHSStorageService:
    @staticmethod
    def upsert_note(db: Session, note: dict) -> XHSNote:
        existing = db.query(XHSNote).filter(XHSNote.note_id == note["note_id"]).first()

        if existing:
            existing.keyword = note.get("keyword")
            existing.title = note.get("title")
            existing.desc = note.get("desc")
            existing.content = note.get("content")
            existing.author_name = note.get("author_name")
            existing.author_id = note.get("author_id")
            existing.liked_count = note.get("liked_count", 0)
            existing.comment_count = note.get("comment_count", 0)
            existing.collect_count = note.get("collect_count", 0)
            existing.share_count = note.get("share_count", 0)
            existing.note_url = note.get("note_url")
            existing.cover_url = note.get("cover_url")
            existing.tags = json.dumps(note.get("tags", []), ensure_ascii=False)
            existing.raw_json = json.dumps(note.get("raw_json", {}), ensure_ascii=False)
            db.commit()
            db.refresh(existing)
            return existing

        new_note = XHSNote(
            note_id=note["note_id"],
            keyword=note.get("keyword"),
            title=note.get("title"),
            desc=note.get("desc"),
            content=note.get("content"),
            author_name=note.get("author_name"),
            author_id=note.get("author_id"),
            liked_count=note.get("liked_count", 0),
            comment_count=note.get("comment_count", 0),
            collect_count=note.get("collect_count", 0),
            share_count=note.get("share_count", 0),
            note_url=note.get("note_url"),
            cover_url=note.get("cover_url"),
            tags=json.dumps(note.get("tags", []), ensure_ascii=False),
            raw_json=json.dumps(note.get("raw_json", {}), ensure_ascii=False),
        )
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return new_note

    @staticmethod
    def upsert_comments(db: Session, note_id: str, comments: list[dict]):
        for c in comments:
            exists = db.query(XHSComment).filter(
                XHSComment.note_id == note_id,
                XHSComment.comment_id == c["comment_id"]
            ).first()

            if exists:
                exists.user_name = c.get("user_name")
                exists.user_id = c.get("user_id")
                exists.content = c.get("content")
                exists.like_count = c.get("like_count", 0)
                exists.raw_json = json.dumps(c, ensure_ascii=False)
            else:
                row = XHSComment(
                    note_id=note_id,
                    comment_id=c["comment_id"],
                    user_name=c.get("user_name"),
                    user_id=c.get("user_id"),
                    content=c.get("content"),
                    like_count=c.get("like_count", 0),
                    raw_json=json.dumps(c, ensure_ascii=False),
                )
                db.add(row)

        db.commit()
