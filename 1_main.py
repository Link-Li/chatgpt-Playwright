"""
Name 1_main
Date 2023/5/9 23:09
Version 1.0
TODO:
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev/python/docs/library")
    print(page.title())
    browser.close()

with sync_playwright() as p:
    browser = p.webkit.launch()
    page = browser.new_page()
    page.goto("https://www.bilibili.com/")
    page.screenshot(path="example.png")
    browser.close()