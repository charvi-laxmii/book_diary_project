import random
from modules.s3 import writeToMessageLog
from modules.message_handler import send_message
from modules.user_class import User, get_or_create_user
from modules.list_class import (
    List,
    get_all_lists,
    create_list_in_class,
    print_all_lists,
)
from modules.book_class import Book, create_book, get_all_books, print_all_books
from modules.enums import UserStatus, UserCache
from modules.scraper import get_book_summary
from modules.validators import is_int_input_valid, is_not_empty_string, format_message


def menu(user: User, number):
    send_message(
        number,
        "1)Add Book\n2)Create List\n3)Pick my next read\n4)Update Book Info\n5)Update List\n6) Get book summary\n7)Exit menu\n",
    )
    user.set_status(UserStatus.picking_menu_option.value)


def exit_menu(user: User):
    send_message(
        user.user_phone_number,
        "It was pleasure assiting you. Text me back if you need anything!",
    )
    user.set_status(UserStatus.menu.value)


def picking_menu_option(user: User, message):
    if not is_int_input_valid(user, message, 6):
        return
    else:
        if message == "1":
            add_book_menu(user, message)
        elif message == "2":
            create_list_menu(user, message)
        elif message == "3":
            pick_my_next_read_menu(user, message)
        elif message == "4":
            update_book_menu(user, message)
        elif message == "5":
            update_list_menu(user, message)
        elif message == "6":
            print_summary_menu(user, message)
        elif message == "7":
            exit_menu(user)


def add_book_menu(user: User, message):
    send_message(user.user_phone_number, "Please enter the book name")
    user.set_status(UserStatus.add_book_enter_name.value)


def create_list_menu(user: User, message):
    send_message(user.user_phone_number, "Please enter the list name:")
    user.set_status(UserStatus.create_list.value)


def pick_my_next_read_menu(user: User, message):
    send_message(
        user.user_phone_number,
        "How would you like to pick your next read\n1) Pick from the list \n2) Random Choice\n",
    )
    user.set_status(UserStatus.pick_my_next_read_choice.value)


def update_book_menu(user: User, message):
    book_for_update_book = get_all_books(user.user_phone_number)
    user.set_cache(
        UserCache.book_count_for_max_value_of_update_book_cache.value,
        len(book_for_update_book),
    )

    if len(book_for_update_book) == 0:
        send_message(
            user.user_phone_number,
            "There are no books available for you to update",
        )
        exit_menu(user)
    else:
        message_content = (
            f"{print_all_books(user.user_phone_number)}\n\nPlease select a book.",
        )

        send_message(user.user_phone_number, message_content)
        user.set_status(UserStatus.pick_book_for_update_book.value)


def update_list_menu(user: User, message):
    lists = get_all_lists(user.user_phone_number)
    if len(lists) == 0:
        send_message(
            user.user_phone_number,
            "There are no lists available for you to edit",
        )
        exit_menu(user)
    else:
        user.set_cache(UserCache.list_count_for_update_list_cache.value, len(lists))

        message_content = (
            f"{print_all_lists(user.user_phone_number)}\n\nPlease select a list."
        )
        send_message(user.user_phone_number, message_content)
        user.set_status(UserStatus.pick_list_to_update_list.value)


def print_summary_menu(user: User, message):
    book_for_summary = get_all_books(user.user_phone_number)
    if len(book_for_summary) == 0:
        send_message(
            user.user_phone_number,
            "There are no books available for you to get the summary from.",
        )
        exit_menu(user)
    else:
        message_content = (
            f"Please select a book\n\n{print_all_books(user.user_phone_number)}\n"
        )

        send_message(user.user_phone_number, message_content)
        user.set_status(UserStatus.print_summary.value)


def add_book_enter_name(user: User, message):
    if not is_not_empty_string(user, message):
        return
    else:
        user.set_cache(UserCache.book_name_cache.value, message)
        send_message(user.user_phone_number, "Please enter the author name")
        user.set_status(UserStatus.add_book_enter_author.value)


def add_book_enter_author(user: User, message):
    if not is_not_empty_string(user, message):
        return
    else:
        summary = get_book_summary(user.cache[UserCache.book_name_cache.value], message)
        book_id = create_book(
            user.user_phone_number,
            user.cache[UserCache.book_name_cache.value],
            message,
            summary,
        )
        List(user.user_phone_number, user.default_list_id).add_book(book_id)

        if (
            UserCache.updating_list_cache.value in user.cache
            and user.cache[UserCache.updating_list_cache.value] == "Yes"
        ):
            updating_list = get_all_lists(user.user_phone_number)
            updating_list[
                int(user.cache[UserCache.picked_list_index_for_update_list_cache.value])
                - 1
            ].add_book(book_id)
            send_message(user.user_phone_number, "Book is added to your list!")
            user.set_cache(UserCache.updating_list_cache.value, None)
            exit_menu(user)

        else:
            user.set_cache(UserCache.book_id_cache.value, book_id)
            send_message(
                user.user_phone_number,
                "Would you like to add this book to a list.\n1) Yes \n2)No",
            )
            user.set_status(UserStatus.select_whether_to_add_to_list_and_pick.value)


def select_whether_to_add_to_list_and_pick(user: User, message):
    if not is_int_input_valid(user, message, 2):
        return

    else:
        if message == "1":
            list_for_adding_book = get_all_lists(user.user_phone_number)

            user.set_cache(
                UserCache.list_count_for_select_list_for_add_book.value,
                len(list_for_adding_book),
            )

            if len(list_for_adding_book) == 0:
                send_message(
                    user.user_phone_number,
                    "You have no lists avialble to display. Press enter the list name to create one.",
                )
                user.set_cache(
                    UserCache.is_creating_list_to_add_book_cache.value, "Yes"
                )
                user.set_status(UserStatus.create_list.value)
            else:
                message_content = (
                    f"Please select a list\n\n{print_all_lists(user.user_phone_number)}"
                )
                send_message(
                    user.user_phone_number,
                    message_content,
                )
                user.set_status(UserStatus.adding_book_to_selected_list.value)

        else:
            send_message(
                user.user_phone_number,
                "Got it!!",
            )
            exit_menu(user)


def adding_book_to_selected_list(user: User, message):
    if not is_int_input_valid(
        user,
        message,
        int(user.cache[UserCache.list_count_for_select_list_for_add_book.value]) - 1,
    ):
        return
    else:
        lists = get_all_lists(user.user_phone_number)
        send_message(
            user.user_phone_number, "The book has been added to the selected list."
        )

        lists[int(message) - 1].add_book(user.cache[UserCache.book_id_cache.value])
        exit_menu(user)


def create_list(user: User, message):
    if not is_not_empty_string(user, message):
        return
    else:
        list_id = create_list_in_class(user.user_phone_number, message)

        if (
            UserCache.is_creating_list_to_add_book_cache.value in user.cache
            and user.cache[UserCache.is_creating_list_to_add_book_cache.value] == "Yes"
        ):
            List(user.user_phone_number, list_id).add_book(
                user.cache[UserCache.book_id_cache.value]
            )
            user.set_cache(UserCache.book_id_cache.value, None)
            user.set_cache(UserCache.is_creating_list_to_add_book_cache.value, None)
            send_message(
                user.user_phone_number,
                "Book has been added to given list!",
            )
            exit_menu(user)
        else:
            send_message(
                user.user_phone_number,
                "New list has been created.",
            )
            exit_menu(user)


def pick_my_next_read_choice(user: User, message):
    if not is_int_input_valid(user, message, 2):
        return
    else:
        if message == "1":
            lists = get_all_lists(user.user_phone_number)
            if len(lists) == 0:
                send_message(
                    user.user_phone_number, "You have no lists to select from!"
                )
                exit_menu(user)
            else:
                message_content = f"{print_all_lists(user.user_phone_number)}\n\nPlease select a list."
                send_message(user.user_phone_number, message_content)
                user.set_status(UserStatus.pick_my_next_read_list_option.value)
        else:
            lists = get_all_books(user.user_phone_number)
            if len(lists) == 0:
                send_message(
                    user.user_phone_number,
                    "There are no books available to pick from!!",
                )
                exit_menu(user)
            else:
                picked_book = random.choice(lists)
                send_message(
                    user.user_phone_number,
                    f"Here is a suggestion for your next read\n{picked_book}",
                )
                exit_menu(user)


def pick_my_next_read_list_option(user: User, message):
    if not is_int_input_valid(user, message, 4):
        return
    else:
        list_for_pick_my_next_read = get_all_lists(user.user_phone_number)
        if len(list_for_pick_my_next_read[int(message) - 1].book_ids) == 0:
            send_message(
                user.user_phone_number, "There are no books available in the list."
            )
            exit_menu(user)
        else:
            all_books_in_list = list_for_pick_my_next_read[
                int(message) - 1
            ].get_books_in_list()
            picked_book = random.choice(all_books_in_list)

            send_message(
                user.user_phone_number,
                f"Here is a suggestion for your next read\n{picked_book}",
            )

            exit_menu(user)


def pick_book_for_update_book(user: User, message):
    if not is_int_input_valid(
        user,
        message,
        int(user.cache[UserCache.book_count_for_max_value_of_update_book_cache.value]),
    ):
        return
    else:
        user.set_cache(
            UserCache.picked_book_index_for_update_book_cache.value, int(message)
        )
        send_message(
            user.user_phone_number,
            "What would you like to edit\n1) Book Name \n2) Author Name\n",
        )
        user.set_status(UserStatus.picking_update_book_menu_option.value)


def picking_update_book_menu_option(user: User, message):
    if not is_int_input_valid(user, message, 2):
        return
    else:
        if message == "1":
            send_message(user.user_phone_number, "Enter the new book name:")
            user.set_status(UserStatus.update_book_name.value)
        else:
            send_message(user.user_phone_number, "Enter the new author name:")
            user.set_status(UserStatus.update_author_name.value)


def update_book_name(user: User, message):
    if not is_not_empty_string(user, message):
        return
    else:
        all_books = get_all_books(user.user_phone_number)
        book_index = (
            int(user.cache[UserCache.picked_book_index_for_update_book_cache.value]) - 1
        )
        all_books[book_index].edit_title(message)

        user.set_cache(UserCache.picked_book_index_for_update_book_cache.value, None)
        send_message(user.user_phone_number, "Book name has been updated.")
        exit_menu(user)


def update_author_name(user: User, message):
    if not is_not_empty_string(user, message):
        return
    else:
        all_books = get_all_books(user.user_phone_number)
        book_index = (
            int(user.cache[UserCache.picked_book_index_for_update_book_cache.value]) - 1
        )
        all_books[book_index].edit_author_name(message)

        user.set_cache(UserCache.picked_book_index_for_update_book_cache.value, None)
        send_message(user.user_phone_number, "Author name is updated.")
        exit_menu(user)


def pick_list_for_update_list(user: User, message):
    if not is_int_input_valid(
        user,
        message,
        int(user.cache[UserCache.list_count_for_update_list_cache.value]),
    ):
        return
    else:
        user.set_cache(
            UserCache.picked_list_index_for_update_list_cache.value, int(message)
        )
        send_message(
            user.user_phone_number,
            "How would you like to edit the list\n1) Edit list name\n2) Add book\n3) Remove book",
        )
        user.set_status(UserStatus.picking_update_list_menu_option.value)


def picking_update_list_menu_option(user: User, message):
    if not is_int_input_valid(user, message, 3):
        return
    else:
        if message == "1":
            send_message(user.user_phone_number, "Enter the new list name:")
            user.set_status(UserStatus.update_list_name.value)
        elif message == "2":
            send_message(user.user_phone_number, "Enter the book name:")
            user.set_cache(UserCache.updating_list_cache.value, "Yes")
            user.set_status(UserStatus.add_book_enter_name.value)
        else:
            all_lists = get_all_lists(user.user_phone_number)
            list_index = (
                int(user.cache[UserCache.picked_list_index_for_update_list_cache.value])
                - 1
            )
            book_ids = all_lists[list_index].book_ids
            if len(book_ids) == 0:
                send_message(
                    user.user_phone_number, "There are no books in this list to remove."
                )
                exit_menu(user)
            else:
                message_content = f"{all_lists[list_index].print_books_in_list()}\nPlease select the book you want to remove"
                send_message(user.user_phone_number, message_content)
                user.set_status(UserStatus.update_list_remove_book.value)


def update_list_name(user: User, message):
    if not is_not_empty_string(user, message):
        return
    else:
        all_lists = get_all_lists(user.user_phone_number)
        list_index = (
            int(user.cache[UserCache.picked_list_index_for_update_list_cache.value]) - 1
        )
        all_lists[list_index].edit_title(message)

        send_message(user.user_phone_number, "List name updated!!")
        exit_menu(user)


def update_list_remove_book(user: User, message):
    if not is_int_input_valid(
        user,
        message,
        int(user.cache[UserCache.list_count_for_update_list_cache.value]),
    ):
        return
    else:
        all_lists = get_all_lists(user.user_phone_number)
        list_index = (
            int(user.cache[UserCache.picked_list_index_for_update_list_cache.value]) - 1
        )

        book_id_to_remove = all_lists[list_index].book_ids[int(message) - 1]

        all_lists[list_index].remove_book_from_list(book_id_to_remove)

        Book.delete_book(user.user_phone_number, book_id_to_remove)

        send_message(user.user_phone_number, "Book id has been removed")
        exit_menu(user)


def print_summary(user: User, message):
    books_for_summary = get_all_books(user.user_phone_number)
    if not is_int_input_valid(user, message, len(books_for_summary)):
        return
    else:
        message_content = books_for_summary[int(message) - 1].print_summary()
        send_message(user.user_phone_number, message_content)
        exit_menu(user)


def handle_text(number, message):
    writeToMessageLog(number, message, "From")

    message = format_message(message)
    user = get_or_create_user(number)

    if user.status == UserStatus.menu.value:
        menu(user, number)
    elif user.status == UserStatus.picking_menu_option.value:
        picking_menu_option(user, message)
    elif user.status == UserStatus.add_book_enter_name.value:
        add_book_enter_name(user, message)
    elif user.status == UserStatus.add_book_enter_author.value:
        add_book_enter_author(user, message)
    elif user.status == UserStatus.select_whether_to_add_to_list_and_pick.value:
        select_whether_to_add_to_list_and_pick(user, message)
    elif user.status == UserStatus.adding_book_to_selected_list.value:
        adding_book_to_selected_list(user, message)
    elif user.status == UserStatus.create_list.value:
        create_list(user, message)
    elif user.status == UserStatus.pick_my_next_read_choice.value:
        pick_my_next_read_choice(user, message)
    elif user.status == UserStatus.pick_my_next_read_list_option.value:
        pick_my_next_read_list_option(user, message)
    elif user.status == UserStatus.pick_book_for_update_book.value:
        pick_book_for_update_book(user, message)
    elif user.status == UserStatus.picking_update_book_menu_option.value:
        picking_update_book_menu_option(user, message)
    elif user.status == UserStatus.update_book_name.value:
        update_book_name(user, message)
    elif user.status == UserStatus.update_author_name.value:
        update_author_name(user, message)
    elif user.status == UserStatus.pick_list_to_update_list.value:
        pick_list_for_update_list(user, message)
    elif user.status == UserStatus.picking_update_list_menu_option.value:
        picking_update_list_menu_option(user, message)
    elif user.status == UserStatus.update_list_name.value:
        update_list_name(user, message)
    elif user.status == UserStatus.update_list_remove_book.value:
        update_list_remove_book(user, message)
    elif user.status == UserStatus.print_summary.value:
        print_summary(user, message)
