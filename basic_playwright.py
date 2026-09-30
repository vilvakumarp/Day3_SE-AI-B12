#this is a basic program to test playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://google.com")
    #make a screenshot of the page
    page.screenshot(path="playwright_screenshot.png")
    browser.close()