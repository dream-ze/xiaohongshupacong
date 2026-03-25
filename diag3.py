import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled","--no-sandbox","--disable-dev-shm-usage"],
    )
    context = browser.new_context(
        storage_state="data/storage_state.json",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        locale="zh-CN",
        viewport={"width": 1280, "height": 800},
    )
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = context.new_page()
    page.set_default_timeout(35000)
    page.goto("https://www.xiaohongshu.com/search_result?keyword=%E5%92%96%E5%95%A1&source=web_explore_feed&type=51", wait_until="domcontentloaded", timeout=35000)
    page.wait_for_timeout(3000)
    state = page.evaluate("() => window.__INITIAL_STATE__")
    search = state.get("search", {})
    print("search keys:", list(search.keys()))
    feeds = search.get("feeds", {})
    print("feeds type:", type(feeds).__name__)
    if isinstance(feeds, dict):
        print("feeds keys:", list(feeds.keys())[:10])
    elif isinstance(feeds, list):
        print("feeds length:", len(feeds))
        if feeds:
            print("first feed keys:", list(feeds[0].keys()) if isinstance(feeds[0], dict) else feeds[0])
    # Also print raw search section truncated
    print("search.state:", search.get("state"))
    print("search.searchValue:", search.get("searchValue"))
    browser.close()
