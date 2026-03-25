import os
import concurrent.futures
from queue import Queue
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from app.core.config import settings

# 所有 Playwright 操作必须在专用线程里运行，greenlet 不许跨线程切换
_pw_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def run_in_pw_thread(fn, timeout: float = 300):
    """Submit fn() to the dedicated playwright thread and block until done."""
    future = _pw_executor.submit(fn)
    return future.result(timeout=timeout)


class BrowserPool:
    def __init__(self):
        self.playwright = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.pages: Queue[Page] = Queue()
        self.initialized = False

    def start(self):
        if self.initialized:
            return

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=settings.browser_headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        storage_state = (
            settings.storage_state_path
            if os.path.exists(settings.storage_state_path)
            else None
        )
        self.context = self.browser.new_context(
            storage_state=storage_state,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
            viewport={"width": 1280, "height": 800},
        )
        # 消除 navigator.webdriver 特征，避免被 XHS 检测为 headless bot
        self.context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        for _ in range(settings.browser_pool_page_size):
            page = self.context.new_page()
            page.set_default_timeout(settings.browser_timeout_ms)
            self.pages.put(page)

        self.initialized = True

    def acquire_page(self) -> Page:
        if not self.initialized:
            self.start()
        return self.pages.get()

    def release_page(self, page: Page):
        try:
            if page.is_closed():
                new_page = self.context.new_page()
                new_page.set_default_timeout(settings.browser_timeout_ms)
                self.pages.put(new_page)
            else:
                self.pages.put(page)
        except Exception:
            if self.context:
                new_page = self.context.new_page()
                new_page.set_default_timeout(settings.browser_timeout_ms)
                self.pages.put(new_page)

    def reset_context(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.initialized = False
        while not self.pages.empty():
            try:
                self.pages.get_nowait()
            except Exception:
                break
        self.start()

    def stop(self):
        while not self.pages.empty():
            page = self.pages.get_nowait()
            try:
                page.close()
            except Exception:
                pass

        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.initialized = False


browser_pool = BrowserPool()
