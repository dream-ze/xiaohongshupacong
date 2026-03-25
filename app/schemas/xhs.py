from pydantic import BaseModel, Field
from typing import List, Optional


class CrawlRequest(BaseModel):
    keyword: str = Field(..., description="搜索关键词")
    page_count: int = Field(1, ge=1, le=10)
    page_size: int = Field(20, ge=1, le=50)
    sort: str = Field("general")
    need_detail: bool = True
    need_comments: bool = False
    comment_limit: int = Field(5, ge=1, le=20)
    need_export: bool = True


class NoteItem(BaseModel):
    note_id: str
    title: str = ""
    desc: str = ""
    content: str = ""
    author_name: str = ""
    author_id: str = ""
    liked_count: int = 0
    comment_count: int = 0
    collect_count: int = 0
    share_count: int = 0
    note_url: str = ""
    cover_url: str = ""
    tags: List[str] = []
    comments: List[dict] = []


class CrawlResponse(BaseModel):
    success: bool
    keyword: str
    total_count: int
    export_path: Optional[str] = None
    items: List[NoteItem] = []
    message: str = ""
