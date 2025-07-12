import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError
from keep_alive import keep_alive

load_dotenv()

USERNAME = os.getenv("IG_USER")
PASSWORD = os.getenv("IG_PASS")
THREAD_ID = os.getenv("THREAD_ID")
MESSAGE = os.getenv("SPAM_MESSAGE")

async def login(page):
    await page.goto("https://www.instagram.com/accounts/login/")
    await page.fill("input[name='username']", USERNAME)
    await page.fill("input[name='password']", PASSWORD)
    await page.click("button[type='submit']")

    try:
        await page.wait_for_url("https://www.instagram.com/", timeout=10000)
        print("[+] Login successful!")
    except TimeoutError:
        print("[-] Login failed or took too long.")
        return False
    return True

async def spam():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        success = await login(page)
        if not success:
            return

        await page.goto(f"https://www.instagram.com/direct/t/{THREAD_ID}/")

        print("[+] Spamming Started...")
        while True:
            for char in MESSAGE:
                await page.keyboard.type(char)
                await asyncio.sleep(0.05)  # 50ms per character
            await page.keyboard.press("Enter")
            await asyncio.sleep(10)  # Delay between each message

if __name__ == "__main__":
    keep_alive()
    asyncio.run(spam())
