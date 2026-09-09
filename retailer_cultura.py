from playwright.sync_api import sync_playwright


PRODUCT_URL = (
    "https://www.cultura.com/"
    "p-console-nintendo-switch-2-edition-limitee-the-legend-of-zelda-"
    "ocarina-of-time-13424072.html"
)


def check_cultura():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        try:

            page.goto(
                PRODUCT_URL,
                wait_until="domcontentloaded",
                timeout=30000
            )

            title = page.title()

            if title == "Just a moment...":

                print("Cultura: Cloudflare protection detected.")
                return None

            text = page.locator("body").inner_text().lower()

            if "en stock en ligne" in text:
                return True

            if "indisponible en ligne" in text:
                return False

            print("Cultura: status unknown.")
            return None

        finally:

            browser.close()


if __name__ == "__main__":

    result = check_cultura()

    if result is True:
        print("🟢 Cultura: AVAILABLE")

    elif result is False:
        print("🔴 Cultura: UNAVAILABLE")

    else:
        print("⚪ Cultura: UNKNOWN / BLOCKED")