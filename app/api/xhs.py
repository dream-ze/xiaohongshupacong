from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.xhs import CrawlRequest
from app.core.browser_pool import browser_pool, run_in_pw_thread
from app.core.database import get_db
from app.services.xhs_auth_service import XHSAuthService
from app.services.xhs_search_service import XHSSearchService
from app.services.xhs_detail_service import XHSDetailService
from app.services.xhs_storage_service import XHSStorageService
from app.services.xhs_export_service import XHSExportService

router = APIRouter(prefix="/xhs", tags=["xhs"])


@router.get("/auth/status")
def auth_status():
    def _task():
        page = browser_pool.acquire_page()
        try:
            return XHSAuthService.check_login(page)
        finally:
            browser_pool.release_page(page)
    return run_in_pw_thread(_task)


@router.post("/crawl")
def crawl_notes(req: CrawlRequest, db: Session = Depends(get_db)):
    def _task():
        page = browser_pool.acquire_page()
        try:
            login_status = XHSAuthService.check_login(page)
            if not login_status["is_login"]:
                raise HTTPException(status_code=400, detail=login_status["message"])

            all_notes = []

            for current_page_num in range(1, req.page_count + 1):
                notes = XHSSearchService.search_notes(
                    browser_page=page,
                    keyword=req.keyword,
                    page_num=current_page_num,
                    page_size=req.page_size,
                    sort=req.sort,
                )

                for note in notes:
                    if req.need_detail and note.get("note_url"):
                        note = XHSDetailService.enrich_note_detail(
                            browser_page=page,
                            note=note,
                            need_comments=req.need_comments,
                            comment_limit=req.comment_limit,
                        )

                    saved = XHSStorageService.upsert_note(db, note)

                    if req.need_comments and note.get("comments"):
                        XHSStorageService.upsert_comments(db, saved.note_id, note["comments"])

                    all_notes.append(note)

            export_path = None
            if req.need_export:
                export_path = XHSExportService.export_notes(req.keyword, all_notes)

            return {
                "success": True,
                "keyword": req.keyword,
                "total_count": len(all_notes),
                "export_path": export_path,
                "items": all_notes,
                "message": "采集完成",
            }
        finally:
            browser_pool.release_page(page)
    return run_in_pw_thread(_task)
