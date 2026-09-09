from playwright.sync_api import sync_playwright


FNAC_FR_URL = (
    "https://www.fnac.com/"
    "Console-Nintendo-Switch-2-Edition-Limitee-40eme-anniversaire-"
    "The-Legend-of-Zelda/a21424371"
)

FNAC_BE_URL = (
    "https://www.fr.fnac.be/"
    "Console-Nintendo-Switch-2-Edition-Limitee-40eme-anniversaire-"
    "The-Legend-of-Zelda/a21424371"
)


def check_page(name, url, browser):
    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    page = browser.new_page()

    try:
        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("HTTP STATUS:", response.status if response else "None")
        print("TITLE:", page.title())

        page.wait_for_timeout(5000)

        text = page.locator("body").inner_text().lower()

        print("PAGE TEXT LENGTH:", len(text))

        phrases = [
            "en stock",
            "indisponible",
            "précommander",
            "précommande",
            "ajouter au panier",
            "disponible"
        ]

        print()
        print("PHRASE COUNTS:")

        for phrase in phrases:
            print(
                f"{phrase}: {text.count(phrase)}"
            )

        print()
        print("FIRST 3000 CHARACTERS:")
        print(text[:3000])

    except Exception as error:
        print("ERROR:", error)

    finally:
        page.close()


def main():
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True
        )

        check_page(
            "FNAC FRANCE",
            FNAC_FR_URL,
            browser
        )

        check_page(
            "FNAC BELGIUM",
            FNAC_BE_URL,
            browser
        )

        browser.close()


if __name__ == "__main__":
    main()