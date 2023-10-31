import requests
from bs4 import BeautifulSoup


def get_book_summary(book_name, author_name):
    formatted_book_name = "+".join(book_name.split())
    formatted_author_name = "+".join(author_name.split())

    search_url = f"https://www.goodreads.com/search?q={formatted_book_name}+{formatted_author_name}"

    html = requests.get(search_url)
    soup = BeautifulSoup(html.content, "html.parser")

    table = soup.find("table", class_="tableList")
    if not table == None:
        rows = table.find_all("tr")

        book_link = ""

        for row in rows:
            book_title_element = row.find("a", class_="bookTitle")
            book_author = row.find("a", class_="authorName")

            if book_title_element and book_author:
                row_title = book_title_element.text
                row_author = book_author.text

                if (
                    book_name.lower() in row_title.lower()
                    and author_name.lower() in row_author.lower()
                ):
                    book_link = book_title_element["href"]
                    break

        if book_link == "":
            return "This book isn't on book reads"
        else:
            book_html = requests.get(f"https://www.goodreads.com{book_link}")
            book_soup = BeautifulSoup(book_html.content, "html.parser")
            content = book_soup.find(id="__next")
            # Find and print the book summary
            summary = book_soup.find("span", class_="Formatted")
            if summary:
                return summary.get_text()
            else:
                return "None found"
    else:
        return "Book doesn't exist"
