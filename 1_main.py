"""
Name 1_main
Date 2023/5/9 23:09
Version 1.0
TODO:
"""

from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("https://playwright.dev/python/docs/library")
#     print(page.title())
#     browser.close()

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("http://www.baidu.com")
    page.click('id=s-top-loginbtn')
    print(page.content())
    for cookie in page.context.cookies():
        print(cookie)
    page.click('"立即注册"')
    page.wait_for_timeout(100000)
    page.screenshot(path="example.png")
    browser.close()