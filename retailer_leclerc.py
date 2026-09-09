import requests


PRODUCT_URL = (
    "https://www.e.leclerc/fp/"
    "console-nintendo-switch-2-edition-"
    "40e-anniversaire-de-the-legend-of-zelda-"
    "nintendo-switch-2-0045496337292"
)


def check_leclerc():

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
        print("E.Leclerc request failed:", e)
        return None

    if response.status_code != 200:
        print(
            "E.Leclerc request failed "
            f"(HTTP {response.status_code})."
        )
        return None

    text = response.content.decode(
        "utf-8",
        errors="ignore"
    ).lower()

    marker = "disabled-text-light"

    position = text.rfind(marker)

    if position == -1:
        print(
            "E.Leclerc: Availability section not found."
        )
        return None

    section = text[position - 500:position + 1500]

    if "précommande épuisée" in section:
        print("E.Leclerc: UNAVAILABLE")
        return False

    if "en précommande" in section:
        print("E.Leclerc: AVAILABLE")
        return True

    print(
        "E.Leclerc: Could not determine availability."
    )

    return None


if __name__ == "__main__":

    result = check_leclerc()

    print()
    print("RESULT:", result)
