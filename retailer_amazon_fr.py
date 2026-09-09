import requests


PRODUCT_URL = "https://www.amazon.fr/dp/B0F2TN43GH"


def check_amazon():
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

    response = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=20
    )

    print("STATUS:", response.status_code)
    print("FINAL URL:", response.url)

    if response.status_code != 200:
        print("Amazon request failed.")
        return None

    text = response.content.decode(
        "utf-8",
        errors="ignore"
    ).lower()

    print("PAGE SIZE:", len(text))

    phrases = [
        "ajouter au panier",
        "précommander",
        "en stock",
        "actuellement indisponible",
        "indisponible",
        "date de sortie",
        "amazon.fr"
    ]

    print()
    print("PHRASE COUNTS:")

    for phrase in phrases:
        print(
            f"{phrase}: {text.count(phrase)}"
        )

    print()
    print("PAGE TITLE / FIRST PART:")
    print(text[:3000])


if __name__ == "__main__":
    check_amazon()