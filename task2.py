from playwright.sync_api import sync_playwright


def capture_cricbuzz_scores():
    match_pages = [
        (
            "current",
            "https://www.cricbuzz.com/cricket-match/live-scores",
        ),
        (
            "last completed",
            "https://www.cricbuzz.com/cricket-match/live-scores/recent-matches",
        ),
    ]
    output_image = "cricbuzz_recent_scorecard.png"

    print("Launching Chromium browser...")
    with sync_playwright() as p:
        # headless=False opens a visible Chromium window.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        scorecard_link = None
        selected_match_type = None

        for match_type, match_url in match_pages:
            print(f"Loading {match_type} matches: {match_url}")
            response = page.goto(
                match_url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            if response is not None and response.status >= 400:
                continue

            # Prefer a current match; use the last completed match only if
            # there is no current scorecard available.
            candidate = page.locator(
                "a[href*='/live-cricket-scorecard/']"
            ).first
            if candidate.count() > 0:
                scorecard_link = candidate
                selected_match_type = match_type
                break

        if scorecard_link is None:
            page.screenshot(path="cricbuzz_access_denied.png", full_page=True)
            raise RuntimeError(
                "No current or last completed scorecard was found. "
                "Cricbuzz may be blocking automated access."
            )

        print(f"Opening the {selected_match_type} scorecard...")
        scorecard_link.click()
        page.wait_for_load_state("domcontentloaded")

        print(f"Saving screenshot to {output_image}...")
        page.screenshot(path=output_image, full_page=True)

        browser.close()
        print("Successfully captured the recent Cricbuzz scorecard!")

if __name__ == "__main__":
    capture_cricbuzz_scores()
