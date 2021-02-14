from playwright.sync_api import sync_playwright
import time

def check(page, text, img):
    page.fill("textarea[placeholder=\"请输入您的问题，Shift+Enter换行\"]", text)
    page.press("textarea[placeholder=\"请输入您的问题，Shift+Enter换行\"]", "Enter")
    time.sleep(2)
    page.screenshot(path=img)


def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://admin.iir.ac.cn/result?id=75
    page.goto("https://admin.iir.ac.cn/result?id=75")

    check(page, "一老一小怎么办理？", "yilaoyixiao.png")
    check(page, "高新技术企业认定和高新技术产品认定是一回事吗？", "gaoxin.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
