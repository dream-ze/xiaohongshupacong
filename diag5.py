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
    page.set_default_timeout(40000)

    search_url = "https://www.xiaohongshu.com/search_result?keyword=%E5%92%96%E5%95%A1&source=web_explore_feed&type=51"
    try:
        with page.expect_response(
            lambda r: "/api/sns/web/v1/search/notes" in r.url,
            timeout=40000
        ) as resp_info:
            page.goto(search_url, wait_until="commit", timeout=40000)
        resp = resp_info.value
        text = resp.text()
        print("status:", resp.status, "  len:", len(text))
        data = json.loads(text)
        items = data.get("data", {}).get("items", [])
        print("items count:", len(items))
        if items:
            print("first item keys:", list(items[0].keys()))
    except Exception as e:
        print("error:", e)
        print("final URL:", page.url)
    browser.close()
