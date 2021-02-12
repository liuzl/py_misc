from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.baidu.com/
    page.goto("https://www.baidu.com/")

    # Click input[name="wd"]
    page.click("input[name=\"wd\"]")

    # Fill input[name="wd"]
    page.fill("input[name=\"wd\"]", "刘占亮")

    # Press Enter
    page.press("input[name=\"wd\"]", "Enter")
    # assert page.url == "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=刘占亮&fenlei=256&rsv_pq=915a9b500025ce4f&rsv_t=db46+BIMzu86ccIBDgG/GXk7Bso1v7zWrDRFKwCKY0qP+AEyJIOmndwlSi4&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=8&rsv_sug1=7&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&prefixsug=%E5%88%98%E5%8D%A0%E4%BA%AE&rsp=5&inputT=7438&rsv_sug4=7745"

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
