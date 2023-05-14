# -*- coding: utf-8 -*-
"""
@Time        : 2023/5/12 19:06
@Author      : noahzhenli
@Email       : noahzhenli@tencent.com
@Description : 
"""
import json

from playwright.sync_api import sync_playwright

launch_data_dict = {
    "headless": False,
    "proxy": {"server": "http://127.0.0.1:7892"}
}

js = """
Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
"""

env_dict = {}
with open("env", "r", encoding="utf-8") as f_read:
    for data_line in f_read.readlines():
        for key, value in json.loads(data_line.strip("\n")).items():
            env_dict[key] = value

def handle_popup(dialog):
    print("xxxxxx")
    dialog.wait_for_timeout(1000)
    dialog.wait_for_selector(".btn-neutral").click()

with sync_playwright() as p:
    browser = p.chromium.launch(**launch_data_dict)
    page = browser.new_page()
    context = browser.new_context()
    page.add_init_script(js)
    page.goto("https://chat.openai.com/")
    page.wait_for_load_state("networkidle")
    # page.pause()
    page.wait_for_selector("div[class='mb-2 text-center']")
    page.wait_for_timeout(1000)
    page.wait_for_selector("button:has-text('Log in')").click()
    page.wait_for_selector("div:has-text('Email address')")
    page.wait_for_selector("input#username").fill("1259604265@qq.com")
    page.wait_for_timeout(1000)
    # page.locator(".cf53b6197").click()
    page.locator("._button-login-id").click()
    page.wait_for_selector("input#password").fill(env_dict["passwd"])
    page.locator("._button-login-password").click()
    # page.on("dialog", handle_dialog)
    page.wait_for_load_state("networkidle")
    with context.expect_page() as new_page:
        page.click("'Next'")
        print(page.locator(".justify-center"))
        new_page.wait_for_selector(".justify-center").click()
    # next_route_announcer = page.wait_for_selector("next-route-announcer")

    a = 1
    page.wait_for_selector(".justify-center").click()
    page.wait_for_timeout(50000)
    page.screenshot(path="example.png")
    browser.close()