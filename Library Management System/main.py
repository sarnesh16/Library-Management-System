import json

class Book:
    def __init__(self, title, author, is_borrowed=False):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed

class Member:
    def __init__(self, name, borrowed_books=None):
        if borrowed_books is None:
            borrowed_books = []
        self.name = name
        self.borrowed_books = borrowed_books

class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, title, author):
        new_book = Book(title, author)
        self.books.append(new_book)
        print(f"Book '{title}' by {author} added successfully!")

        # Save the updated data to librarydata.json
        self.save_data()

    def register_member(self, name):
        new_member = Member(name)
        self.members.append(new_member)
        print(f"Member '{name}' registered successfully!")

        # Save the updated data to librarydata.json
        self.save_data()

    def borrow_book(self, member_name, book_title):
        member = self.find_member(member_name)
        book = self.find_book(book_title)

        if member and book and not book.is_borrowed:
            book.is_borrowed = True
            member.borrowed_books.append(book_title)
            print(f"Member '{member_name}' borrowed '{book_title}' successfully!")
        else:
            print(f"Book '{book_title}' is already borrowed or member does not exist.")

        # Save the updated data to librarydata.json
        self.save_data()

    def return_book(self, member_name, book_title):
        member = self.find_member(member_name)
        book = self.find_book(book_title)

        if member and book and book.is_borrowed:
            book.is_borrowed = False
            member.borrowed_books.remove(book_title)
            print(f"Member '{member_name}' returned '{book_title}' successfully!")
        else:
            print(f"Book '{book_title}' is not borrowed or member does not exist.")

        # Save the updated data to librarydata.json
        self.save_data()

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def find_member(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    def save_data(self):
        # Convert books and members to a dictionary structure for saving as JSON
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "is_borrowed": book.is_borrowed
                }
                for book in self.books
            ],
            "members": [
                {
                    "name": member.name,
                    "borrowed_books": member.borrowed_books
                }
                for member in self.members
            ]
        }

        # Write the data to librarydata.json
        with open("librarydata.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Data saved to librarydata.json!")

    def load_data(self):
        try:
            # Load data from librarydata.json
            with open("librarydata.json", "r") as file:
                data = json.load(file)

            # Recreate books
            self.books = [
                Book(item["title"], item["author"], item["is_borrowed"])
                for item in data.get("books", [])
            ]

            # Recreate members
            self.members = [
                Member(item["name"], item["borrowed_books"])
                for item in data.get("members", [])
            ]
            print("Data loaded successfully from librarydata.json!")
        except FileNotFoundError:
            print("No previous data found. Starting with an empty library.")
        except Exception as e:
            print(f"Error loading data: {e}")

def main():
    library = Library()
    library.load_data()  # Load existing data when the program starts

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. View Books")
        print("6. View Members")
        print("7. Save and Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)

        elif choice == 2:
            name = input("Enter member name: ")
            library.register_member(name)

        elif choice == 3:
            member_name = input("Enter member name: ")
            book_title = input("Enter book title to borrow: ")
            library.borrow_book(member_name, book_title)

        elif choice == 4:
            member_name = input("Enter member name: ")
            book_title = input("Enter book title to return: ")
            library.return_book(member_name, book_title)

        elif choice == 5:
            print("\nBooks in Library:")
            for book in library.books:
                status = "Borrowed" if book.is_borrowed else "Available"
                print(f"Title: {book.title}, Author: {book.author}, Status: {status}")

        elif choice == 6:
            print("\nRegistered Members:")
            for member in library.members:
                print(f"Name: {member.name}, Borrowed Books: {', '.join(member.borrowed_books)}")

        elif choice == 7:
            library.save_data()  # Save before exiting
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()
