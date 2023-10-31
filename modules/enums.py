from enum import Enum


class UserStatus(Enum):
    menu = "menu"
    picking_menu_option = "picking_menu_option"
    add_book_enter_name = "add_book_enter_name"
    add_book_enter_author = "add_book_enter_author"
    select_whether_to_add_to_list_and_pick = "select_whether_to_add_to_list_and_pick"
    adding_book_to_selected_list = "adding_book_to_selected_list"
    create_list = "create_list"
    pick_my_next_read_choice = "pick_my_next_read_choice"
    pick_my_next_read_list_option = "pick_my_next_read_list_option"
    pick_book_for_update_book = "pick_book_for_update_book"
    picking_update_book_menu_option = "picking_update_book_menu_option"
    update_book_name = "update_book_name"
    update_author_name = "update_author_name"
    pick_list_to_update_list = "pick_list_to_update_list"
    picking_update_list_menu_option = "picking_update_list_menu_option"
    update_list_name = "update_list_name"
    update_list_remove_book = "update_list_remove_book"
    print_summary = "print_summary"


class UserCache(Enum):
    book_name_cache = "book_name_cache"
    book_id_cache = "book_id_cache"
    book_count_for_max_value_of_update_book_cache = (
        "book_count_for_max_value_of_update_book_cache"
    )
    book_name_for_add_book_cache = "book_name_for_add_book_cache"
    book_id_for_add_book = "book_id_for_add_book_cache"
    list_count_for_select_list_for_add_book = (
        "list_count_for_select_list_for_add_book_cache"
    )
    is_creating_list_to_add_book_cache = "is_creating_list_to_add_book_cache"
    picked_book_index_for_update_book_cache = "picked_book_index_for_update_book_cache"
    list_count_for_update_list_cache = "list_count_for_update_list_cache"
    picked_list_index_for_update_list_cache = "picked_list_index_for_update_list_cache"
    updating_list_cache = "updating_list_cache"
