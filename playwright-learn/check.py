from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://admin.iir.ac.cn/result?id=75
    page.goto("https://admin.iir.ac.cn/result?id=75")


    # Fill textarea[placeholder="请输入您的问题，Shift+Enter换行"]
    page.fill("textarea[placeholder=\"请输入您的问题，Shift+Enter换行\"]", "一老一小怎么办理？")

    # Press Enter
    page.press("textarea[placeholder=\"请输入您的问题，Shift+Enter换行\"]", "Enter")

    page.screenshot(path="name.png")
    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
