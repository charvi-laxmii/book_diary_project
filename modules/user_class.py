import boto3
from modules.list_class import create_list_in_class
from modules.message_handler import send_message
from modules.enums import UserStatus

USERS_TABLE = boto3.resource("dynamodb", region_name="us-east-1").Table("Users")


def get_or_create_user(number):
    existing = loadUser(number)

    if existing:
        return existing
    else:
        default_list_id = create_list_in_class(number, "all_books")
        userKey = {
            "user_phone_number": number,
            "status": UserStatus.menu.value,
            "cache": {},
            "default_list_id": default_list_id,
        }
        USERS_TABLE.put_item(Item=userKey)

        send_message(
            number,
            "Welcome!! I am a book management bot built by Charvi Pattila. You can see my source code at https://github.com/charvi-laxmii/book_diary_project.",
        )

        return User(number)


class User:
    def __init__(self, user_phone_number):
        data = USERS_TABLE.get_item(
            Key={
                "user_phone_number": user_phone_number,
            }
        )["Item"]

        self.user_phone_number = user_phone_number
        self.status = data["status"]
        self.cache = {} if "cache" not in data else data["cache"]
        self.default_list_id = data["default_list_id"]

    def set_status(self, new_status):
        self.status = new_status
        self.write_to_file()

    def set_cache(self, key, value):
        self.cache[key] = value
        self.write_to_file()

    def write_to_file(self):
        write_user_to_file(
            self.user_phone_number, self.status, self.cache, self.default_list_id
        )


def loadUser(number):
    try:
        return User(number)
    except Exception as e:
        print(e)
        return None


def write_user_to_file(user_phone_number, status, cache, default_list_id):
    USERS_TABLE.put_item(
        Item={
            "user_phone_number": user_phone_number,
            "status": status,
            "cache": cache,
            "default_list_id": default_list_id,
        }
    )
