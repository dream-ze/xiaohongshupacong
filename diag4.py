import json, time
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

    api_calls = []
    def on_resp(r):
        if "xiaohongshu" in r.url and ("/api/" in r.url or "/fe_api/" in r.url):
            api_calls.append((r.status, r.url))
    page.on("response", on_resp)

    page.goto("https://www.xiaohongshu.com/search_result?keyword=%E5%92%96%E5%95%A1&source=web_explore_feed&type=51", wait_until="domcontentloaded", timeout=35000)
    # wait up to 20s for feeds to populate
    deadline = time.time() + 20
    while time.time() < deadline:
        page.wait_for_timeout(1000)
        state = page.evaluate("() => window.__INITIAL_STATE__")
        feeds = (state or {}).get("search", {}).get("feeds", [])
        sv = (state or {}).get("search", {}).get("searchValue", "")
        print(f"t={int(time.time()-deadline+20):2d}s  searchValue={sv!r}  feeds={len(feeds)}")
        if len(feeds) > 0:
            break
    print("== API calls ==")
    for s, u in api_calls:
        print(s, u)
    if feeds:
        print("== First feed keys ==")
        print(list(feeds[0].keys()) if isinstance(feeds[0], dict) else feeds[0])
    browser.close()
