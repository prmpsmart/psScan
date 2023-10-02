import threading
import telebot
from telebot import types
from fastapi import FastAPI

from crypto_coins import *

TELEGRAM_BOT_TOKEN = "6522595578:AAEoohT3dDPq7JGczjSffttpl3NVR-GoY7Q"
ETHERSCAN_APIKEY = "5VSCYDENMVJQUMZXP4JZP26Z1U8GVV3HN1"
ETHEREUM_API_URL = "https://api.etherscan.io/api"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def getMention(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    return "[" + user_name + "](tg://user?id=" + str(user_id) + ")"


@bot.message_handler(commands=["start"])
def command_start(message: types.Message):
    print(type(message))

    start_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    start_markup.row("/start", "/help")
    start_markup.row("/crypto", "/bal")
    start_markup.row("/hide")
    bot.send_message(
        message.chat.id, "🤖 The bot has started!\n⚙ Enter /help to see bot's function's"
    )
    bot.send_message(
        message.chat.id,
        f"""Hi {getMention(message)}!\nThis bot is just a proof-of-work done by:\nMiracle Apata a.k.a @prmpsmart\n\nTo check the balance of a token address type /bal followed by the address\ne.g\n/bal 0x1d81D79d0D5cc899E16d8cdaD7995B8bEb6f7114""",
        parse_mode="Markdown",
    )
    bot.send_message(
        message.from_user.id,
        "⌨️ The Keyboard is added!\n⌨️ /hide To remove kb",
        reply_markup=start_markup,
    )


@bot.message_handler(commands=["hide"])
def command_hide(message: types.Message):
    hide_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)


@bot.message_handler(commands=["help"])
def command_help(message: types.Message):
    bot.send_message(
        message.chat.id,
        "🤖 /start - display the keyboard\n"
        "💎 /crypto - current cryptocurrency\n"
        "⌛️ /bal - calculate eth aadress bal\n",
    )


@bot.message_handler(commands=["crypto"])
def command_crypto(message: types.Message):
    coins_markup = types.InlineKeyboardMarkup(row_width=1)
    for key, value in coins.items():
        coins_markup.add(types.InlineKeyboardButton(text=key, callback_data=value))
    bot.send_message(message.chat.id, "📃 Choose the coin:", reply_markup=coins_markup)


# Function to scan the token contract on the Ethereum blockchain
def address_balance(token_contract_address):
    """Scans the token contract on the Ethereum blockchain and returns the contract information."""

    params = {
        "module": "account",
        "action": "balance",
        "address": token_contract_address,
        "apikey": ETHERSCAN_APIKEY,
    }

    response = requests.get(ETHEREUM_API_URL, params=params)
    contract_information = response.json()

    return contract_information


@bot.message_handler(commands=["bal"])
def command_bal(message: types.Message):
    text = message.text.strip()

    if text:
        text_ = text.split()[-1]
        contract_information = address_balance(text_)
        text = """STATUS: {status}\nMESSAGE: {message}\nRESULT: {result}\nUSER_INPUT: {text}""".format(
            text=text, **contract_information
        )
        bot.reply_to(message, text)

    else:
        bot.reply_to(message, "Enter a valid address!")


@bot.callback_query_handler(func=lambda call: True)
def callback_crypto_stocks(call):
    if call.message:
        coins_switcher = {
            "BTC": f"💰Bitcoin:  ${btc_price}",
            "LTC": f"💰Litecoin:  ${ltc_price}",
            "ETH": f"💰Ethereum:  ${eth_price}",
            "ETC": f"💰Ethereum Classic:  ${etc_price}",
            "ZEC": f"💰Zcash:  ${zec_price}",
            "DSH": f"💰Dash:  ${dsh_price}",
            "XRP": f"💰Ripple:  ${xrp_price}",
        }

        coin_response = coins_switcher.get(call.data)
        if coin_response:
            bot.send_message(call.message.chat.id, coin_response)


def start():
    # bot.polling(non_stop=True)

    threading.Thread(target=bot.polling, kwargs=dict(non_stop=True)).start()


app = FastAPI(
    title="psScan Telegram bot",
    version="1.0.0",
    on_startup=[start],
    # on_shutdown=[exit],
)


@app.get("/")
async def home() -> str:
    return "Hello World"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        use_colors=True,
        host="127.0.0.1",
        port=8000,
        reload=0,
    )
