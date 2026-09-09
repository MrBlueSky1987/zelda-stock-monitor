import requests

PRODUCT_URL = "https://www.carrefour.fr/p/console-nintendo-switch-2-edition-zelda-40eme-anniversaire-0045496337292"


def check_carrefour():
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

    print("=" * 60)
    print("CARREFOUR")
    print("=" * 60)

    try:
        response = requests.get(
            PRODUCT_URL,
            headers=headers,
            timeout=20
        )

    except requests.RequestException as e:
        print("Carrefour request failed:")
        print(e)
        return None

    print("STATUS:", response.status_code)
    print("FINAL URL:", response.url)

    if response.status_code != 200:
        print("Carrefour request failed.")
        return None

    text = response.content.decode(
        "utf-8",
        errors="ignore"
    ).lower()

    print("PAGE SIZE:", len(text))

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
    print("FIRST 3000 CHARACTERS:")
    print(text[:3000])


if __name__ == "__main__":
    check_carrefour()