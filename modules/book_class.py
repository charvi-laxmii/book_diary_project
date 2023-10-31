import boto3
from typing import Sequence
from uuid import uuid4
from boto3.dynamodb.conditions import Key

BOOK_TABLE = boto3.resource("dynamodb", region_name="us-east-1").Table("Books")


class Book(object):
    def __init__(self, user_phone_number, book_id):
        self.book_id = book_id
        self.user_phone_number = user_phone_number
        response = BOOK_TABLE.get_item(
            Key={
                "user_phone_number": user_phone_number,
                "book_id": book_id,
            }
        )
        item = response["Item"]
        self.book_name = item["book_name"]
        self.author_name = item["author_name"]
        self.summary = item["summary"]

    def __str__(self):
        return f"Book Name: {self.book_name}\nAuthor Name: {self.author_name}\n"

    def write_to_file(self):
        write_book_to_file(
            self.user_phone_number,
            self.book_id,
            self.book_name,
            self.author_name,
            self.summary,
        )

    def edit_title(self, new_title):
        self.book_name = new_title
        self.write_to_file()

    def edit_author_name(self, new_author_name):
        self.author_name = new_author_name
        self.write_to_file()

    def delete_book(self):
        resp = BOOK_TABLE.delete_item(
            Key={"user_phone_number": self.user_phone_number, "book_id": self.book_id}
        )

    def print_summary(self):
        return self.summary


def write_book_to_file(user_phone_number, book_id, book_name, author_name, summary):
    BOOK_TABLE.put_item(
        Item={
            "user_phone_number": user_phone_number,
            "book_id": book_id,
            "book_name": book_name,
            "author_name": author_name,
            "summary": summary,
        },
    )


def create_book(user_phone_number, book_name, author, summary):
    book_id = str(uuid4())
    write_book_to_file(user_phone_number, book_id, book_name, author, summary)
    return book_id


def get_all_books(user_phone_number) -> Sequence[Book]:
    books = []

    response = BOOK_TABLE.query(
        KeyConditionExpression=Key("user_phone_number").eq(user_phone_number)
    )

    for item in response["Items"]:
        book_id = item["book_id"]

        books.append(Book(user_phone_number, book_id))

    return books


def print_books(books: Sequence[Book]):
    message = ""
    for index, book in enumerate(books):
        message += f"{index + 1}) {book}\n"

    return message.strip()


def print_all_books(user_phone_number: str):
    return print_books(get_all_books(user_phone_number))
