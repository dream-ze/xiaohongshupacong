import json
from playwright.sync_api import sync_playwright
from urllib.parse import quote

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
    with page.expect_response(lambda r: "/api/sns/web/v1/search/notes" in r.url, timeout=40000) as ri:
        page.goto("https://www.xiaohongshu.com/search_result?keyword=%E5%92%96%E5%95%A1&source=web_explore_feed&type=51", wait_until="commit", timeout=40000)
    data = json.loads(ri.value.text())
    item = data["data"]["items"][0]
    nc = item.get("note_card", {})
    print("item top keys:", list(item.keys()))
    print("note_card keys:", list(nc.keys())[:15])
    print("note_card.note_id:", nc.get("note_id"))
    print("note_card.title:", nc.get("title"))
    print("note_card.desc:", nc.get("desc"))
    user = nc.get("user", {})
    print("user keys:", list(user.keys()))
    print("user.nickname:", user.get("nickname"))
    ii = nc.get("interact_info", {})
    print("interact_info.liked_count:", ii.get("liked_count"))
    browser.close()
