import requests

PRODUCT_URL = (
    "https://www.auchan.fr/"
    "nintendo-console-de-jeu-nintendo-switch-2-edition-zelda/"
    "pr-C1893413"
)


def check_auchan():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"
    }

    try:
        response = requests.get(
            PRODUCT_URL,
            headers=headers,
            timeout=20
        )

    except requests.RequestException as e:
        print("Auchan request failed:")
        print(e)
        return None

    print("Auchan STATUS:", response.status_code)

    if response.status_code != 200:
        print("Auchan: Could not access product page.")
        return None

    text = response.content.decode(
        "utf-8",
        errors="ignore"
    ).lower()

    # Look specifically for the purchase button.
    marker = 'class="quantity-selector--label"'

    positions = []
    position = 0

    while True:
        position = text.find(marker, position)

        if position == -1:
            break

        positions.append(position)
        position += len(marker)

    print("Auchan purchase buttons found:", len(positions))

    if not positions:
        print("Auchan: Purchase button not found.")
        return None

    # Check the text immediately following each purchase button.
    for position in positions:
        section = text[position:position + 300]

        print()
        print("Auchan purchase section:")
        print(section)

        if "précommander" in section:
            print("Auchan: AVAILABLE (PREORDER)")
            return True

        if "ajouter au panier" in section:
            print("Auchan: AVAILABLE")
            return True

        if "indisponible" in section:
            print("Auchan: UNAVAILABLE")
            return False

    print("Auchan: Could not determine availability.")
    return None


if __name__ == "__main__":
    result = check_auchan()

    print()
    print("RESULT:", result)