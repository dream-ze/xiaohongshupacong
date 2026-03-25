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

    api_calls = {}
    def on_resp(r):
        if "/api/sns/" in r.url:
            api_calls[r.url] = r.status
    page.on("response", on_resp)

    try:
        page.goto("https://www.xiaohongshu.com/search_result?keyword=%E5%92%96%E5%95%A1&source=web_explore_feed&type=51", wait_until="domcontentloaded", timeout=35000)
        page.wait_for_timeout(10000)
    except Exception as e:
        print("goto error:", e)

    print("URL:", page.url)
    print("Title:", page.title())
    print("Search API calls:")
    for u, s in api_calls.items():
        print(s, u)
    browser.close()
