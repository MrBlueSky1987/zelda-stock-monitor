import json
import os
from datetime import datetime

from retailer_leclerc import check_leclerc
from retailer_leclerc_controller import check_leclerc_controller


STATE_FILE = "stock_state.json"


CONSOLE = {
    "key": "console",
    "name": "Nintendo Switch 2 Zelda 40th Anniversary Console",
    "short_name": "Zelda 40th Anniversary Console",
    "retailer": "E.Leclerc",
    "url": (
        "https://www.e.leclerc/fp/"
        "console-nintendo-switch-2-edition-"
        "40e-anniversaire-de-the-legend-of-zelda-"
        "nintendo-switch-2-0045496337292"
    ),
    "price": "€469"
}


CONTROLLER = {
    "key": "controller",
    "name": "Nintendo Switch 2 Zelda 40th Anniversary Pro Controller",
    "short_name": "Zelda 40th Anniversary Pro Controller",
    "retailer": "E.Leclerc",
    "url": (
        "https://www.e.leclerc/fp/"
        "manette-pro-controller-nintendo-switch-2-edition-40e-"
        "anniversaire-de-the-legend-of-zelda-nintendo-switch-2-"
        "0045496322045"
    ),
    "price": "€89"
}


def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        print("Could not load state:", e)

        return {}


def save_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            indent=4
        )


def check_product(product, new_value, state):

    key = product["key"]

    old_value = state.get(key)

    if new_value is None:

        print(
            f"{product['name']}: "
            "could not be checked. "
            "Keeping previous state."
        )

        return False

    if old_value is None:

        state[key] = new_value

        print(
            f"{product['name']}: "
            f"{new_value} (initial state)"
        )

        return False

    if old_value is False and new_value is True:

        print(
            f"🚨 {product['name']} "
            "IS NOW AVAILABLE!"
        )

        state[key] = new_value

        return True

    if old_value is True and new_value is False:

        print(
            f"{product['name']} "
            "is no longer available."
        )

    else:

        print(
            f"{product['name']}: "
            f"{new_value}"
        )

    state[key] = new_value

    return False


def send_telegram_alert(product):

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_ids = os.getenv("TELEGRAM_CHAT_IDS")

    if not token:

        print(
            "TELEGRAM_BOT_TOKEN is missing."
        )

        return

    if not chat_ids:

        print(
            "TELEGRAM_CHAT_IDS is missing."
        )

        return

    message = (
        "🚨 ZELDA STOCK ALERT!\n\n"
        f"🟢 {product['short_name']}\n\n"
        f"🏪 {product['retailer']}\n"
        f"💰 {product['price']}\n\n"
        f"{product['url']}"
    )

    url = (
        f"https://api.telegram.org/bot"
        f"{token}/sendMessage"
    )

    import requests

    for chat_id in chat_ids.split(","):

        chat_id = chat_id.strip()

        if not chat_id:
            continue

        try:

            response = requests.post(
                url,
                data={
                    "chat_id": chat_id,
                    "text": message
                },
                timeout=20
            )

            print(
                f"Telegram alert to {chat_id}: "
                f"{response.status_code}"
            )

        except requests.RequestException as e:

            print(
                "Telegram request failed:",
                e
            )


def main():

    print()
    print("=" * 60)

    print(
        "Scheduled stock check:",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print("=" * 60)

    state = load_state()

    console_result = check_leclerc()

    print(
        f"E.Leclerc - "
        f"{CONSOLE['name']}: "
        f"{console_result}"
    )

    console_available = check_product(
        CONSOLE,
        console_result,
        state
    )

    if console_available:

        send_telegram_alert(CONSOLE)

    controller_result = check_leclerc_controller()

    print(
        f"E.Leclerc - "
        f"{CONTROLLER['name']}: "
        f"{controller_result}"
    )

    controller_available = check_product(
        CONTROLLER,
        controller_result,
        state
    )

    if controller_available:

        send_telegram_alert(CONTROLLER)

    save_state(state)

    print()
    print("State saved.")
    print()


if __name__ == "__main__":
    main()