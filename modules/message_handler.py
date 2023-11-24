from twilio.rest import Client
from modules.s3 import writeToMessageLog
from modules.ssm import get_encrypted_parameter

TWILIO_NUMBER = "+18663937112"
ACCOUNT_SID = get_encrypted_parameter("book_diary_sid")
AUTH_TOKEN = get_encrypted_parameter("book_diary_auth")


client = Client(ACCOUNT_SID, AUTH_TOKEN)


def sanitize_message(message: str) -> str:
    punctuation = [".", ",", ":", ";", "?", "!"]

    message = message.replace("\\", "")

    for symbol in punctuation:
        message = message.replace(f"{symbol} ", f"{symbol}").replace(
            f"{symbol}", f"{symbol} "
        )

    message = message.replace(". . .", "...")

    return message


def send_message(user_phone_number, message):
    message = sanitize_message(message)
    client.messages.create(to=user_phone_number, from_=TWILIO_NUMBER, body=message)
    writeToMessageLog(user_phone_number, message, "To")
