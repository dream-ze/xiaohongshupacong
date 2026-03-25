import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font
from app.core.config import settings


class XHSExportService:
    @staticmethod
    def export_notes(keyword: str, notes: list[dict]) -> str:
        os.makedirs(settings.export_dir, exist_ok=True)

        filename = f"xhs_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(settings.export_dir, filename)

        wb = Workbook()
        ws = wb.active
        ws.title = "小红书采集结果"

        headers = [
            "keyword", "note_id", "title", "desc", "content",
            "author_name", "author_id", "liked_count", "comment_count",
            "note_url", "cover_url", "tags",
        ]

        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for note in notes:
            ws.append([
                note.get("keyword", ""),
                note.get("note_id", ""),
                note.get("title", ""),
                note.get("desc", ""),
                note.get("content", ""),
                note.get("author_name", ""),
                note.get("author_id", ""),
                note.get("liked_count", 0),
                note.get("comment_count", 0),
                note.get("note_url", ""),
                note.get("cover_url", ""),
                ",".join(note.get("tags", [])),
            ])

        ws.freeze_panes = "A2"

        for col in ws.columns:
            max_length = 12
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    max_length = max(max_length, len(str(cell.value)) if cell.value else 0)
                except Exception:
                    pass
            ws.column_dimensions[col_letter].width = min(max_length + 2, 50)

        wb.save(filepath)
        return filepath
