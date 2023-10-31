from twilio.rest import Client
from modules.s3 import writeToMessageLog
from modules.ssm import get_encrypted_parameter

TWILIO_NUMBER = "+18663937112"
ACCOUNT_SID = get_encrypted_parameter("book_diary_sid")
AUTH_TOKEN = get_encrypted_parameter("book_diary_auth")


client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_message(user_phone_number, message):
    client.messages.create(to=user_phone_number, from_=TWILIO_NUMBER, body=message)
    writeToMessageLog(user_phone_number, message, "To")
