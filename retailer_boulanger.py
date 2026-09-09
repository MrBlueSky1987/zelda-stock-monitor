from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.boulanger.com/ref/1247632"


def check_boulanger():
    print("=" * 60)
    print("BOULANGER")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            locale="fr-FR"
        )

        try:
            response = page.goto(
                PRODUCT_URL,
                wait_until="domcontentloaded",
                timeout=30000
            )

            print("STATUS:", response.status if response else "NONE")
            print("FINAL URL:", page.url)

            page.wait_for_timeout(5000)

            text = page.locator("body").inner_text().lower()

            print("PAGE TEXT SIZE:", len(text))

            phrases = [
                "en stock",
                "indisponible",
                "précommande",
                "précommander",
                "ajouter au panier",
                "disponible",
                "rupture",
                "épuisé"
            ]

            print()
            print("PHRASE COUNTS:")

            for phrase in phrases:
                print(f"{phrase}: {text.count(phrase)}")

            print()
            print("PAGE TEXT:")
            print(text[:5000])

        except Exception as e:
            print("ERROR:", type(e).__name__)
            print(e)

        finally:
            browser.close()


if __name__ == "__main__":
    check_boulanger()