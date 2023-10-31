from modules.message_handler import send_message
from modules.user_class import User


def is_int_input_valid(user: User, prompt: str, maxValue: int) -> bool:
    values = []
    for i in range(maxValue):
        values.append(str(i + 1))

    if prompt not in values:
        send_message(
            user.user_phone_number, f"Please enter one of the following: {values}"
        )
        return False
    else:
        return True


def is_not_empty_string(user: User, prompt: str) -> bool:
    if prompt.strip() == " ":
        send_message(user.user_phone_number, "Please enter any value!")
        return False
    else:
        return True


def format_message(message) -> str:
    message = message.strip().lower()
    punctuation = [",", ".", "!"]

    for punct in punctuation:
        message = message.replace(punct, "")

    return message
