import boto3
from typing import Sequence
from uuid import uuid4
from boto3.dynamodb.conditions import Key
from modules.book_class import Book, print_books


LIST_TABLE = boto3.resource("dynamodb", region_name="us-east-1").Table("List")


class List:
    def __init__(self, user_phone_number, list_id):
        self.list_id = list_id
        self.user_phone_number = user_phone_number
        response = LIST_TABLE.get_item(
            Key={
                "user_phone_number": user_phone_number,
                "list_id": list_id,
            }
        )
        item = response["Item"]
        self.list_name = item["list_name"]
        self.book_ids = item["book_ids"] or []

    def write_to_file(self):
        write_list_to_file(
            self.user_phone_number, self.list_id, self.list_name, self.book_ids
        )

    def add_book(self, book_id):
        if book_id not in self.book_ids:
            self.book_ids.append(book_id)
            self.write_to_file()

    def remove_book_from_list(self, book_id):
        if book_id in self.book_ids:
            self.book_ids.remove(book_id)
            self.write_to_file()

    def edit_title(self, new_title):
        self.list_name = new_title
        self.write_to_file()

    def print_books_in_list(self) -> list:
        if len(self.book_ids) == 0:
            return "No books available in this list"

        books = []
        for book_id in self.book_ids:
            books.append(Book(self.user_phone_number, book_id))

        return print_books(books)

    def get_books_in_list(self) -> list:
        if len(self.book_ids) == 0:
            return []
        else:
            books = []
            for book_id in self.book_ids:
                books.append(Book(self.user_phone_number, book_id))

            return books


def write_list_to_file(user_phone_number, list_id, list_name, book_ids=[]):
    LIST_TABLE.put_item(
        Item={
            "user_phone_number": user_phone_number,
            "list_id": list_id,
            "list_name": list_name,
            "book_ids": book_ids,
        },
    )
    return list_id


def create_list_in_class(user_phone_number, list_name) -> str:
    list_id = str(uuid4())
    write_list_to_file(user_phone_number, list_id, list_name, None)
    return list_id


def get_all_lists(user_phone_number) -> Sequence[List]:
    lists = []

    response = LIST_TABLE.query(
        KeyConditionExpression=Key("user_phone_number").eq(user_phone_number)
    )

    for item in response["Items"]:
        list_id = item["list_id"]
        list_name = item["list_name"]

        if list_name == "all_books":
            continue

        lists.append(List(user_phone_number, list_id))

    return lists


def print_lists(lists: Sequence[List]):
    message = ""
    for index, list in enumerate(lists):
        message += f"{index + 1}) {list.list_name}\n"

    return message.strip()


def print_all_lists(user_phone_number):
    return print_lists(get_all_lists(user_phone_number))
