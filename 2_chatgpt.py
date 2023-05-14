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
    page.wait_for_selector("input#username").fill(env_dict["openai_account"])
    page.wait_for_timeout(1000)
    # page.locator(".cf53b6197").click()
    page.locator("._button-login-id").click()
    page.wait_for_selector("input#password").fill(env_dict["openai_passwd"])
    page.locator("._button-login-password").click()
    # page.on("dialog", handle_dialog)
    page.wait_for_load_state("networkidle")
    page.click("'Next'")
    page.wait_for_timeout(1000)
    page.click("'Next'")
    page.wait_for_timeout(1000)
    page.click("'Done'")


    page.fill('textarea[placeholder="Send a message."]', '你好')
    page.keyboard.press('Enter')
    page.wait_for_selector("'Regenerate response'", timeout=1000000)

    print("开始和chatgpt对话吧：")

    while True:

        prompt = input()
        if prompt == 'stop':
            print("bye")
            break
        elif prompt == "new":
            page.click("'New chat'")
            print("开始新的对话")
            continue
        page.fill('textarea[placeholder="Send a message."]', prompt)
        page.keyboard.press('Enter')
        page.wait_for_selector("'Regenerate response'", timeout=1000000)

        page_text = page.query_selector_all(".markdown")[-1]
        text = page_text.evaluate("""
            div => {
                const getText = (node, texts = [], liCounter = { value: 0 }) => {
                    for (const child of node.childNodes) {
                        if (child.nodeType === Node.TEXT_NODE) {
                            const textContent = child.textContent.trim();
                            
                            // 当前节点为 li，则添加序号
                            if (node.tagName === 'LI') {
                                texts.push(`${++liCounter.value}. ${textContent}`);
                            } else {
                                // 节点不是 li，重置序号
                                if (liCounter.value !== 0) {
                                    liCounter.value = 0;
                                }

                                texts.push(textContent);
                            }
                        } else if (child.nodeType === Node.ELEMENT_NODE) {
                            getText(child, texts, liCounter);
                        }
                    }
                    return texts;
                };

                return getText(div).join('%%');
            }
                """)
        print(text.replace("%%", "\n"))

    # page.wait_for_selector(".justify-center").click()
    page.wait_for_timeout(1000)
    page.screenshot(path="example.png")
    browser.close()