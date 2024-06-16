import flet as ft
from playwright.sync_api import sync_playwright


def run(playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(
        headless = False,
        slow_mo = 200
    )
    page = browser.new_page()
    page.goto("http://eds.newtouch.cn/eds3/")

def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))
    with sync_playwright() as playwright:
        run(playwright)

ft.app(main)
