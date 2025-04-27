import os

# Define the file path
FILE_PATH = 'books.txt'

# Check if the books.txt exists, if not create it
if not os.path.exists(FILE_PATH):
    open(FILE_PATH, 'w').close()

# Main program loop
while True:
    print("\n1. Add Book\n2. Search Book\n3. Update Book\n4. Delete Book\n5. Display Books\n6. Exit")
    choice = input("Choose an option: ")

    if choice == '1':  # Add Book
        title = input("Enter book title: ")
        author = input("Enter author: ")
        year = input("Enter year: ")
        with open(FILE_PATH, 'a') as file:
            file.write(f"{title},{author},{year}\n")
            print("Book added.")

    elif choice == '2':  # Search Book
        title = input("Enter book title to search: ")
        found = False
        try:
            with open(FILE_PATH, 'r') as file:
                for line in file:
                    if title.lower() in line.lower():
                        print(line.strip())  # Display the matching book
                        found = True
            if not found:
                print("Book not found!")
        except FileNotFoundError:
            print("No books found!")

    elif choice == '3':  # Update Book
        old_title = input("Enter the title of the book you want to update: ")
        new_title = input("Enter new title: ")
        new_author = input("Enter new author: ")
        new_year = input("Enter new year: ")

        updated = False
        try:
            with open(FILE_PATH, 'r') as file:
                lines = file.readlines()
            
            with open(FILE_PATH, 'w') as file:
                for line in lines:
                    if line.startswith(old_title):
                        file.write(f"{new_title},{new_author},{new_year}\n")
                        updated = True
                        print("Book updated.")
                    else:
                        file.write(line)

            if not updated:
                print("Book not found for update!")
        
        except Exception as e:
            print(f"An error occurred while updating the book: {e}")

    elif choice == '4':  # Delete Book
        title = input("Enter book title to delete: ")
        found = False
        try:
            with open(FILE_PATH, 'r') as file:
                lines = file.readlines()

            with open(FILE_PATH, 'w') as file:
                for line in lines:
                    if not line.startswith(title):
                        file.write(line)
                    else:
                        found = True
                if found:
                    print("Book deleted.")
                else:
                    print("Book not found.")
        
        except Exception as e:
            print(f"An error occurred while deleting the book: {e}")

    elif choice == '5':  # Display Books
        if not os.path.exists(FILE_PATH):
            print("No books found!")
        else:
            try:
                with open(FILE_PATH, 'r') as file:
                    books = file.readlines()
                    books = [book.strip() for book in books]  # Remove newline
                    books.sort()  # Sort books alphabetically by title
                    for book in books:
                        print(book)
            except Exception as e:
                print(f"An error occurred while displaying the books: {e}")

    elif choice == '6':  # Exit
        try:
            # Backup the current books.txt before exiting
            os.rename(FILE_PATH, 'books_backup.txt')
            print("Backup created as 'books_backup.txt'. Exiting the program.")
        except Exception as e:
            print(f"An error occurred while backing up: {e}")
        break

    else:
        print("Invalid option! Please try again.")