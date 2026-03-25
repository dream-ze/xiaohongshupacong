from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "XHS Playwright Service"
    xhs_base_url: str = "https://www.xiaohongshu.com"
    storage_state_path: str = "data/storage_state.json"
    browser_headless: bool = True
    browser_timeout_ms: int = 30000
    browser_pool_page_size: int = 2
    sqlite_url: str = "sqlite:///./xhs_service.db"
    export_dir: str = "data/exports"


settings = Settings()
