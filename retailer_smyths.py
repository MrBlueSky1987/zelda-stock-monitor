import requests


PRODUCT_URL = (
    "https://www.smythstoys.com/ie/en-ie/gaming-and-tech/"
    "nintendo-switch-2/nintendo-switch-2-consoles/"
    "nintendo-switch-2-the-legend-of-zelda-40th-anniversary-edition-console/"
    "p/265573"
)


def check_smyths():

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
        "Accept-Language": "en-IE,en;q=0.9"
    }

    response = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=20
    )

    print("STATUS:", response.status_code)
    print("SERVER:", response.headers.get("server"))

    print()
    print("FIRST 1000 CHARACTERS:")
    print(response.text[:1000])


if __name__ == "__main__":
    check_smyths()