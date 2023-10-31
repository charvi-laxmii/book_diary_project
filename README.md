# book_diary_project
**Overview**:
This is a book management applicaiton build by using Python, AWS, Twilio & Beautiful Soup. The application allows the user to create books and lists to organize their reading better. Additonally, the applition gets the synoposis of the book using goodreads. 


**Instructions for the Code:**
1. Prerequisties: Run the command
2. Go into AWS to create List, User, Book
3. Dist zip
4. Create the lambda function
5. upload the zip
6. create an api gateway trigger
7. Put the link in twilio
8. Set up the ssm
9. Can run this locally using ngrok and server.py


**Code:**
- UserStatus - Enum class that tracks the every status of the user
- UserCache - Enum class that tracks the cache values of the user
  
Menu
1) Add book
- Prompts the user for book_name and author_name, then adds it to the book table and all_books list
- After creating the book, the user is given the option to add the book to a custom list.
- If the user chooses not to add it to the list, the status will reset to the menu. Otherwise, the program displays all the lists from the database for the user to choose from, and later, the book will be added to the selected list. After that, the user is sent back to the menu
- If there are no lists in the database, the user is prompted to create a list, and then the book will be added.

2) Create List
- Prompts the user for the list name and add the list name to the database

3) Pick my next read
- This function randomizes a list of books to suggest to the user a potential book to read next.
- The user has the option to either randomize all the books in the database or pick a list and then randomize the books in the list

4) Update Book
- Prompts the user to pick the book they would like to update.
- Then, a menu would be prompted with the options of 1) Edit Book Name and 2)Edit author name.
- After the user chooses the menu option, the application prompts the user to input the new value, and the book will be updated in the database.

5) Update List
- Prompts the user to pick the book they would like to update.
- Then, a menu would be prompted with the options of 1) Edit List Name, 2)Add Book, 3)Remove Book
- a) List name: Prompt the user for the new list name and update the database
- b) Add Book: Prompts the user for book_name and author_name, then adds it to the book table, all_books list & selected list
- c) Remove Book: Displays all the books in the List and prompts the user to pick the book they want to remove. The database is then updated with the new List of books, and the book table and all_books list are also updated.

6) Print Summary
- Prompts the user to pick a book they want to get the synopsis for. Then, the summary is printed. 
