from playwright.sync_api import Page


class XHSAuthService:
    @staticmethod
    def check_login(page: Page) -> dict:
        cookies = page.context.cookies()
        has_token = any(
            c.get("name", "") in ("web_session", "customer-sso-sid", "auth")
            for c in cookies
        )
        if has_token:
            return {"is_login": True, "need_relogin": False, "message": "ok"}
        return {
            "is_login": False,
            "need_relogin": True,
            "message": "未检测到登录凭证，请先登录",
        }

