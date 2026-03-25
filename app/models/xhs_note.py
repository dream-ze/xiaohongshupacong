from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base


class XHSNote(Base):
    __tablename__ = "xhs_notes"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String(64), nullable=False, unique=True, index=True)
    keyword = Column(String(255), nullable=True)
    title = Column(Text, nullable=True)
    desc = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    author_name = Column(String(100), nullable=True)
    author_id = Column(String(64), nullable=True)
    liked_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    collect_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    note_url = Column(Text, nullable=True)
    cover_url = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)      # JSON 字符串
    images = Column(Text, nullable=True)    # JSON 字符串
    raw_json = Column(Text, nullable=True)  # 原始返回
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class XHSComment(Base):
    __tablename__ = "xhs_note_comments"
    __table_args__ = (
        UniqueConstraint("note_id", "comment_id", name="uq_note_comment"),
    )

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String(64), nullable=False, index=True)
    comment_id = Column(String(64), nullable=False)
    user_name = Column(String(100), nullable=True)
    user_id = Column(String(64), nullable=True)
    content = Column(Text, nullable=True)
    like_count = Column(Integer, default=0)
    raw_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
