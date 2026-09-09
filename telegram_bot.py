import json
import os
import time
from datetime import datetime

import requests

from retailer_leclerc import check_leclerc
from retailer_leclerc_controller import check_leclerc_controller


# ============================================================
# CONFIGURATION
# ============================================================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

STATE_FILE = "stock_state.json"
USERS_FILE = "users.json"

# Retailer checks happen every 5 minutes.
STOCK_CHECK_INTERVAL = 5 * 60

# Telegram commands/buttons are checked every 2 seconds.
TELEGRAM_CHECK_INTERVAL = 2


# ============================================================
# TELEGRAM
# ============================================================

def telegram_request(method, data=None):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/{method}"
    )

    try:
        response = requests.post(
            url,
            data=data,
            timeout=20
        )

        return response.json()

    except Exception as e:

        print(
            f"Telegram {method} failed:",
            e
        )

        return None


def send_message(chat_id, message, reply_markup=None):

    data = {
        "chat_id": chat_id,
        "text": message
    }

    if reply_markup is not None:

        data["reply_markup"] = json.dumps(
            reply_markup
        )

    result = telegram_request(
        "sendMessage",
        data
    )

    if result and result.get("ok"):

        print(
            f"Telegram message to "
            f"{chat_id}: 200"
        )

    else:

        print(
            f"Telegram message to "
            f"{chat_id}: FAILED"
        )


def answer_callback(callback_query_id):

    telegram_request(
        "answerCallbackQuery",
        {
            "callback_query_id":
                callback_query_id
        }
    )


# ============================================================
# TELEGRAM KEYBOARD
# ============================================================

def main_keyboard():

    return {
        "inline_keyboard": [

            [
                {
                    "text": "🎮 Console",
                    "callback_data":
                        "subscribe_console"
                },
                {
                    "text": "🕹️ Controller",
                    "callback_data":
                        "subscribe_controller"
                }
            ],

            [
                {
                    "text": "📦 Both",
                    "callback_data":
                        "subscribe_both"
                }
            ],

            [
                {
                    "text": "📊 Status",
                    "callback_data":
                        "status"
                },
                {
                    "text": "❌ Stop alerts",
                    "callback_data":
                        "stop"
                }
            ],

            [
                {
                    "text": "ℹ️ Help",
                    "callback_data":
                        "help"
                }
            ]
        ]
    }


# ============================================================
# USERS
# ============================================================

def load_users():

    if not os.path.exists(USERS_FILE):

        return {}

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            users = json.load(file)

            # ------------------------------------------------
            # Backwards compatibility
            # ------------------------------------------------

            changed = False

            for chat_id, preference in list(
                users.items()
            ):

                if preference is True:

                    users[chat_id] = "both"
                    changed = True

                elif preference not in [
                    "console",
                    "controller",
                    "both"
                ]:

                    users[chat_id] = "both"
                    changed = True

            if changed:

                save_users(users)

            return users

    except Exception as e:

        print(
            "Could not load users:",
            e
        )

        return {}


def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4
        )


# ============================================================
# STOCK STATE
# ============================================================

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

        print(
            "Could not load state:",
            e
        )

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


# ============================================================
# PRODUCT INFORMATION
# ============================================================

CONSOLE = {

    "key":
        "console",

    "name":
        "Nintendo Switch 2 Zelda 40th Anniversary Console",

    "short_name":
        "Zelda 40th Anniversary Console",

    "retailer":
        "E.Leclerc",

    "url":
        (
            "https://www.e.leclerc/fp/"
            "console-nintendo-switch-2-edition-"
            "40e-anniversaire-de-the-legend-of-zelda-"
            "nintendo-switch-2-0045496337292"
        ),

    "price":
        "€469"
}


CONTROLLER = {

    "key":
        "controller",

    "name":
        "Nintendo Switch 2 Zelda 40th Anniversary Pro Controller",

    "short_name":
        "Zelda 40th Anniversary Pro Controller",

    "retailer":
        "E.Leclerc",

    "url":
        (
            "https://www.e.leclerc/fp/"
            "manette-pro-controller-nintendo-switch-2-edition-40e-"
            "anniversaire-de-the-legend-of-zelda-nintendo-switch-2-"
            "0045496322045"
        ),

    "price":
        "€89"
}


# ============================================================
# STATUS
# ============================================================

def status_text(value):

    if value is True:
        return "🟢 AVAILABLE"

    if value is False:
        return "🔴 UNAVAILABLE"

    return "⚪ UNKNOWN"


def send_help(chat_id):

    message = (
        "🟢 Zelda Stock Monitor\n\n"

        "I monitor the Nintendo Switch 2 "
        "Zelda 40th Anniversary products "
        "at E.Leclerc.\n\n"

        "Currently monitored:\n"
        "🎮 Console — €469\n"
        "🕹️ Pro Controller — €89\n\n"

        "Choose what you want to monitor "
        "using the buttons below.\n\n"

        "Commands:\n"
        "/start — Subscribe / change products\n"
        "/console — Console alerts\n"
        "/controller — Controller alerts\n"
        "/both — Console + controller alerts\n"
        "/status — Check current availability\n"
        "/stop — Unsubscribe\n"
        "/help — Show this help message"
    )

    send_message(
        chat_id,
        message,
        main_keyboard()
    )


# ============================================================
# LIVE STATUS
# ============================================================

def send_status(chat_id):

    print(
        f"Telegram status request from "
        f"{chat_id}"
    )

    console_result = check_leclerc()

    controller_result = (
        check_leclerc_controller()
    )

    message = (
        "📊 Zelda Stock Status\n\n"

        "E.Leclerc\n\n"

        "🎮 Zelda 40th Anniversary Console\n"
        f"{status_text(console_result)}\n"
        "€469\n\n"

        "🕹️ Zelda 40th Anniversary Pro Controller\n"
        f"{status_text(controller_result)}\n"
        "€89"
    )

    send_message(
        chat_id,
        message,
        main_keyboard()
    )


# ============================================================
# SUBSCRIPTIONS
# ============================================================

def subscribe_user(chat_id, preference):

    users = load_users()

    users[str(chat_id)] = preference

    save_users(users)

    if preference == "console":

        message = (
            "🎮 Console alerts enabled!\n\n"

            "I'll notify you when the "
            "Zelda 40th Anniversary Console "
            "becomes available at E.Leclerc.\n\n"

            "Price: €469"
        )

    elif preference == "controller":

        message = (
            "🕹️ Controller alerts enabled!\n\n"

            "I'll notify you when the "
            "Zelda 40th Anniversary Pro Controller "
            "becomes available at E.Leclerc.\n\n"

            "Price: €89"
        )

    else:

        message = (
            "📦 Both alerts enabled!\n\n"

            "I'll notify you when either the "
            "Zelda 40th Anniversary Console or "
            "Pro Controller becomes available "
            "at E.Leclerc.\n\n"

            "🎮 Console: €469\n"
            "🕹️ Controller: €89"
        )

    send_message(
        chat_id,
        message,
        main_keyboard()
    )

    print(
        f"Subscriber {chat_id}: "
        f"{preference}"
    )


def stop_user(chat_id):

    users = load_users()

    chat_id = str(chat_id)

    if chat_id in users:

        del users[chat_id]

        save_users(users)

        send_message(
            chat_id,
            "🔴 You have been unsubscribed.\n\n"
            "You will no longer receive stock alerts.",
            main_keyboard()
        )

        print(
            f"Unsubscribed: {chat_id}"
        )

    else:

        send_message(
            chat_id,
            "You are not currently subscribed.",
            main_keyboard()
        )


# ============================================================
# STOCK ALERTS
# ============================================================

def send_stock_alert(product):

    message = (
        "🚨 ZELDA STOCK ALERT!\n\n"

        f"🟢 {product['short_name']}\n\n"

        f"🏪 {product['retailer']}\n"
        f"💰 {product['price']}\n\n"

        f"{product['url']}"
    )

    users = load_users()

    for chat_id, preference in users.items():

        # Console subscribers.
        if (
            product["key"] == "console"
            and preference not in [
                "console",
                "both"
            ]
        ):

            continue

        # Controller subscribers.
        if (
            product["key"] == "controller"
            and preference not in [
                "controller",
                "both"
            ]
        ):

            continue

        send_message(
            chat_id,
            message,
            main_keyboard()
        )

        print(
            f"Stock alert sent to {chat_id}"
        )


def check_product(
    product,
    new_value,
    state
):

    key = product["key"]

    old_value = state.get(key)

    # --------------------------------------------------------
    # Unknown result
    # --------------------------------------------------------

    if new_value is None:

        print(
            f"{product['retailer']} "
            f"{product['key']} could not be checked. "
            f"Keeping previous state unchanged."
        )

        return

    # --------------------------------------------------------
    # First check
    # --------------------------------------------------------

    if old_value is None:

        state[key] = new_value

        print(
            f"{product['name']}: "
            f"{new_value} (initial state)"
        )

        return

    # --------------------------------------------------------
    # Stock became available
    # --------------------------------------------------------

    if (
        old_value is False
        and new_value is True
    ):

        print(
            f"🚨 {product['name']} "
            f"IS NOW AVAILABLE!"
        )

        send_stock_alert(product)

    # --------------------------------------------------------
    # Stock disappeared
    # --------------------------------------------------------

    elif (
        old_value is True
        and new_value is False
    ):

        print(
            f"{product['name']} "
            f"is no longer available."
        )

    # --------------------------------------------------------
    # No change
    # --------------------------------------------------------

    else:

        print(
            f"{product['name']}: "
            f"{new_value}"
        )

    state[key] = new_value


# ============================================================
# RETAILER STOCK CHECK
# ============================================================

def run_stock_check():

    print()
    print("=" * 60)

    print(
        "Stock check:",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print("=" * 60)

    state = load_state()

    # --------------------------------------------------------
    # Console
    # --------------------------------------------------------

    console_result = check_leclerc()

    print(
        f"E.Leclerc - "
        f"{CONSOLE['name']}: "
        f"{console_result}"
    )

    check_product(
        CONSOLE,
        console_result,
        state
    )

    # --------------------------------------------------------
    # Controller
    # --------------------------------------------------------

    controller_result = (
        check_leclerc_controller()
    )

    print(
        f"E.Leclerc - "
        f"{CONTROLLER['name']}: "
        f"{controller_result}"
    )

    check_product(
        CONTROLLER,
        controller_result,
        state
    )

    save_state(state)

    print()
    print("State saved.")
    print()
    print(
        "Next stock check in 5 minutes..."
    )


# ============================================================
# TELEGRAM UPDATES
# ============================================================

def process_callback(callback_query):

    callback_id = callback_query.get(
        "id"
    )

    message = callback_query.get(
        "message"
    )

    if not message:
        return

    chat = message.get(
        "chat"
    )

    if not chat:
        return

    chat_id = str(
        chat["id"]
    )

    data = callback_query.get(
        "data",
        ""
    )

    answer_callback(
        callback_id
    )

    if data == "subscribe_console":

        subscribe_user(
            chat_id,
            "console"
        )

    elif data == "subscribe_controller":

        subscribe_user(
            chat_id,
            "controller"
        )

    elif data == "subscribe_both":

        subscribe_user(
            chat_id,
            "both"
        )

    elif data == "status":

        send_status(chat_id)

    elif data == "help":

        send_help(chat_id)

    elif data == "stop":

        stop_user(chat_id)


def process_message(message):

    chat = message.get(
        "chat"
    )

    if not chat:
        return

    chat_id = str(
        chat["id"]
    )

    text = message.get(
        "text",
        ""
    ).strip().lower()

    if text == "/start":

        send_message(
            chat_id,
            "🟢 Welcome to Zelda Stock Monitor!\n\n"
            "Choose what you want to monitor:",
            main_keyboard()
        )

    elif text == "/console":

        subscribe_user(
            chat_id,
            "console"
        )

    elif text == "/controller":

        subscribe_user(
            chat_id,
            "controller"
        )

    elif text == "/both":

        subscribe_user(
            chat_id,
            "both"
        )

    elif text == "/stop":

        stop_user(chat_id)

    elif text == "/status":

        send_status(chat_id)

    elif text == "/help":

        send_help(chat_id)


def check_telegram_commands():

    result = telegram_request(
        "getUpdates"
    )

    if not result or not result.get("ok"):

        return

    updates = result.get(
        "result",
        []
    )

    if not updates:

        return

    last_update_id = None

    for update in updates:

        last_update_id = update.get(
            "update_id"
        )

        # ----------------------------------------------------
        # Inline button
        # ----------------------------------------------------

        callback_query = update.get(
            "callback_query"
        )

        if callback_query:

            process_callback(
                callback_query
            )

            continue

        # ----------------------------------------------------
        # Normal message
        # ----------------------------------------------------

        message = update.get(
            "message"
        )

        if message:

            process_message(
                message
            )

    # --------------------------------------------------------
    # Clear processed updates
    # --------------------------------------------------------

    if last_update_id is not None:

        telegram_request(
            "getUpdates",
            {
                "offset":
                    last_update_id + 1
            }
        )


# ============================================================
# MAIN LOOP
# ============================================================

def main():

    if not BOT_TOKEN:

        print(
            "ERROR: TELEGRAM_BOT_TOKEN "
            "environment variable is missing."
        )

        return

    print(
        "Zelda Stock Monitor started."
    )

    print(
        "Monitoring: E.Leclerc"
    )

    print(
        "Products: Console + Pro Controller"
    )

    print(
        "Telegram subscriptions: ENABLED"
    )

    print(
        "Telegram response time: ~2 seconds"
    )

    print(
        "Stock check interval: 5 minutes"
    )

    print()

    last_stock_check = 0

    while True:

        # ----------------------------------------------------
        # Telegram is checked continuously.
        # ----------------------------------------------------

        check_telegram_commands()

        # ----------------------------------------------------
        # Retailers are checked only every 5 minutes.
        # ----------------------------------------------------

        now = time.time()

        if (
            now - last_stock_check
            >= STOCK_CHECK_INTERVAL
        ):

            run_stock_check()

            last_stock_check = time.time()

        time.sleep(
            TELEGRAM_CHECK_INTERVAL
        )


if __name__ == "__main__":

    main()