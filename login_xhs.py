import os
from playwright.sync_api import sync_playwright

STORAGE_PATH = "data/storage_state.json"


def main():
    os.makedirs("data", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")
        print("请手动登录小红书")
        input("登录完成后按回车保存登录态...")

        context.storage_state(path=STORAGE_PATH)
        print(f"登录态已保存到: {STORAGE_PATH}")

        browser.close()


if __name__ == "__main__":
    main()
