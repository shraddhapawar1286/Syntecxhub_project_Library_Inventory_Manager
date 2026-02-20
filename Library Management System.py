import json
import os

# -------------------- Book Class --------------------
class Book:
    def __init__(self, book_id, title, author, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "status": self.status
        }


# -------------------- Library Class --------------------
class Library:
    def __init__(self, file_name="library.json"):
        self.file_name = file_name
        self.books = []              # Store books in list
        self.book_index = {}         # Fast lookup dictionary {id: Book}
        self.load_data()

    # ---------------- Load Data ----------------
    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as file:
                    data = json.load(file)
                    for item in data:
                        book = Book(**item)
                        self.books.append(book)
                        self.book_index[book.book_id] = book
            except json.JSONDecodeError:
                print("Warning: library.json is empty or corrupted. Starting fresh.")

    # ---------------- Save Data ----------------
    def save_data(self):
        with open(self.file_name, "w") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    # ---------------- Add Book ----------------
    def add_book(self, book_id, title, author):
        if book_id in self.book_index:
            print("Book ID already exists!")
            return

        book = Book(book_id, title, author)
        self.books.append(book)
        self.book_index[book_id] = book
        self.save_data()
        print("Book added successfully!")

    # ---------------- Search ----------------
    def search(self, keyword):
        results = [
            book for book in self.books
            if keyword.lower() in book.title.lower()
            or keyword.lower() in book.author.lower()
        ]

        if results:
            for book in results:
                self.display(book)
        else:
            print("No matching books found.")

    # ---------------- Issue Book ----------------
    def issue_book(self, book_id):
        book = self.book_index.get(book_id)
        if not book:
            print("Book not found!")
            return

        if book.status == "Issued":
            print("Book already issued.")
        else:
            book.status = "Issued"
            self.save_data()
            print("Book issued successfully!")

    # ---------------- Return Book ----------------
    def return_book(self, book_id):
        book = self.book_index.get(book_id)
        if not book:
            print("Book not found!")
            return

        if book.status == "Available":
            print("Book is already available.")
        else:
            book.status = "Available"
            self.save_data()
            print("Book returned successfully!")

    # ---------------- Display ----------------
    def display(self, book):
        print(f"ID: {book.book_id} | Title: {book.title} | Author: {book.author} | Status: {book.status}")

    # ---------------- Report ----------------
    def report(self):
        total = len(self.books)
        issued = sum(1 for book in self.books if book.status == "Issued")

        print("\n----- Library Report -----")
        print("Total Books:", total)
        print("Issued Books:", issued)
        print("Available Books:", total - issued)


# -------------------- Main Program --------------------
def main():
    library = Library()

    while True:
        print("\n===== Library Menu =====")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Report")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            book_id = input("Book ID: ")
            title = input("Title: ")
            author = input("Author: ")
            library.add_book(book_id, title, author)

        elif choice == "2":
            keyword = input("Enter title or author: ")
            library.search(keyword)

        elif choice == "3":
            book_id = input("Enter Book ID to issue: ")
            library.issue_book(book_id)

        elif choice == "4":
            book_id = input("Enter Book ID to return: ")
            library.return_book(book_id)

        elif choice == "5":
            library.report()

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
