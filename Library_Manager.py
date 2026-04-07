import json
import os

FILE_NAME = "library_data.json"


# Book Class
class Book:
    def __init__(self, book_id, title, author, issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }

    @staticmethod
    def from_dict(data):
        return Book(
            data["book_id"],
            data["title"],
            data["author"],
            data["issued"]
        )


# Library Class
class Library:
    def __init__(self):
        self.books = []  # List
        self.book_map = {}  # Dict (HashMap-like)

    # Add Book
    def add_book(self, book):
        self.books.append(book)
        self.book_map[book.book_id] = book
        print("Book added successfully!")

    # Search Book
    def search(self, keyword):
        results = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        return results

    # Issue Book
    def issue_book(self, book_id):
        if book_id in self.book_map:
            book = self.book_map[book_id]
            if not book.issued:
                book.issued = True
                print("Book issued successfully!")
            else:
                print("Book already issued!")
        else:
            print("Book not found!")

    # Return Book
    def return_book(self, book_id):
        if book_id in self.book_map:
            book = self.book_map[book_id]
            if book.issued:
                book.issued = False
                print("Book returned successfully!")
            else:
                print("Book was not issued!")
        else:
            print("Book not found!")

    # Report
    def report(self):
        total = len(self.books)
        issued = sum(1 for book in self.books if book.issued)
        print(f"Total Books: {total}")
        print(f"Issued Books: {issued}")

    # Save to JSON
    def save(self):
        data = [book.to_dict() for book in self.books]
        with open(FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    # Load from JSON
    def load(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                for item in data:
                    book = Book.from_dict(item)
                    self.books.append(book)
                    self.book_map[book.book_id] = book


# Main Program
def main():
    lib = Library()
    lib.load()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Report")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            lib.add_book(Book(book_id, title, author))

        elif choice == "2":
            keyword = input("Enter title/author: ")
            results = lib.search(keyword)
            for book in results:
                status = "Issued" if book.issued else "Available"
                print(f"{book.book_id} | {book.title} | {book.author} | {status}")

        elif choice == "3":
            book_id = input("Enter Book ID: ")
            lib.issue_book(book_id)

        elif choice == "4":
            book_id = input("Enter Book ID: ")
            lib.return_book(book_id)

        elif choice == "5":
            lib.report()

        elif choice == "6":
            lib.save()
            print("Data saved. Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()