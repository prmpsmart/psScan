import os
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    Updater,
)
import requests
import json

TELEGRAM_BOT_TOKEN = "6522595578:AAEoohT3dDPq7JGczjSffttpl3NVR-GoY7Q"
ETHERSCAN_APIKEY = "5VSCYDENMVJQUMZXP4JZP26Z1U8GVV3HN1"
ETHEREUM_API_URL = "https://api.etherscan.io/api"


# Ethereum:
#    0x1d81D79d0D5cc899E16d8cdaD7995B8bEb6f7114 (Uniswap)
#    0x4f0178AB2545c2c3629653B44588647f6f0059E3 (Chainlink)
#    0x509faABc284aa9770437423b9f133863Da9cb728 (Tether)

# Ethereum blockchain API URL


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
    contract_information = json.loads(response.content.decode())

    return contract_information


# Function to scan the token contract on the Ethereum blockchain
def scan_token_contract(token_contract_address):
    """Scans the token contract on the Ethereum blockchain and returns the contract information."""

    params = {
        "module": "contract",
        "action": "getabi",
        "address": token_contract_address,
        "apikey": ETHERSCAN_APIKEY,
    }

    response = requests.get(ETHEREUM_API_URL, params=params)
    contract_information = json.loads(response.content.decode())

    return contract_information


# Function to calculate the amount of tax received in the marketing wallet
def calculate_tax_received_in_marketing_wallet(contract_information):
    """Calculates the amount of tax received in the marketing wallet."""

    # Get the marketing wallet address from the contract information
    marketing_wallet_address = contract_information["result"]["marketingWallet"]

    # Calculate the amount of tax received in the marketing wallet
    tax_received_in_marketing_wallet = 0

    # TODO: Implement the logic to calculate the amount of tax received in the marketing wallet

    return tax_received_in_marketing_wallet


# Function to send a report to the user
def send_report_to_user(bot, user_id, tax_received_in_marketing_wallet):
    """Sends a report to the user with the amount of tax received in the marketing wallet."""

    bot.sendMessage(
        user_id,
        f"The amount of tax received in the marketing wallet is {tax_received_in_marketing_wallet}.",
    )


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"""Hi {user.mention_html()}!
This bot is just a proof-of-work done by:
Miracle Apata a.k.a @prmpsmart

To check the balance of a token address type /bal followed by the address
e.g

/bal 0x1d81D79d0D5cc899E16d8cdaD7995B8bEb6f7114""",
        # reply_markup=ForceReply(selective=True),
    )


async def bal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks the balance of the address given by the user"""
    text = update.message.text.strip()

    if text:
        text = text.split()[0]
        contract_information = address_balance(text)
        # print(contract_information)
        text = "STATUS: {status}\nMESSAGE: {message}\nRESULT: {result}".format(
            **contract_information
        )
        await update.message.reply_text(text)

    else:
        await update.message.reply_text("Enter an address!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    # application = updater.dispatcher

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bal", bal))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # application.run_webhook(listen="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
