from playwright.sync_api import sync_playwright


GOOGLE_URL = "https://www.google.com"
ACCUWEATHER_URL = (
    "https://www.accuweather.com/en/in/chennai/206671/"
    "weather-forecast/206671"
)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigation and screenshot
    page.goto(GOOGLE_URL, wait_until="domcontentloaded")
    page.screenshot(path="playwright_screenshot.png", full_page=True)

    # Navigate to AccuWeather and take a screenshot
    page.goto(ACCUWEATHER_URL, wait_until="domcontentloaded")
    page.screenshot(path="playwright_screenshot_accuweather.png", full_page=True)

    # Locate and click the first current-weather link, if available
    current_weather_link = page.locator('a[href*="/current-weather/"]').first
    if current_weather_link.count() > 0:
        current_weather_link.click()
        print("Navigated to:", page.url)

    """# Return to Google for the typing and search example
    page.goto(GOOGLE_URL, wait_until="domcontentloaded")
    search_box = page.locator("input[name='q']")
    search_box.fill("Playwright")
    search_box.press("Enter")
    page.wait_for_load_state("domcontentloaded")
    page.screenshot(path="playwright_screenshot_search.png", full_page=True)

    # Wait for a Playwright result and capture it
    page.wait_for_selector("text=Playwright", timeout=10000)
    page.screenshot(path="playwright_screenshot_result.png", full_page=True)

    # Extract the page title
    print(f"Page title: {page.title()}")"""
    browser.close()
