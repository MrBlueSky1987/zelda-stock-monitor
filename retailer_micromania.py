import requests

PRODUCT_URL = (
    "https://www.micromania.fr/"
    "p/console-nintendo-switch-2-edition-limitee-40eme-anniversaire-"
    "the-legend-of-zelda-164787.html"
)


def check_micromania():
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
    print("MICROMANIA")
    print("=" * 60)

    response = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=20
    )

    print("STATUS:", response.status_code)
    print("FINAL URL:", response.url)

    if response.status_code != 200:
        print("Micromania request failed.")
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
        "file d'attente",
        "queue",
        "waiting"
    ]

    print()
    print("PHRASE COUNTS:")

    for phrase in phrases:
        print(f"{phrase}: {text.count(phrase)}")

    print()
    print("FIRST 3000 CHARACTERS:")
    print(text[:3000])


if __name__ == "__main__":
    check_micromania()