"""Questions 5 and 6. Manage a university library from the terminal."""

import argparse
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile


@dataclass
class Book:
    book_id: str
    title: str
    borrowed_by: str | None = None


@dataclass
class Student:
    student_id: str
    name: str


@dataclass
class Library:
    books: dict[str, Book] = field(default_factory=dict)
    students: dict[str, Student] = field(default_factory=dict)

    def add_book(self, book_id, title):
        if book_id in self.books:
            raise ValueError("That book ID already exists.")
        self.books[book_id] = Book(book_id, title)

    def add_student(self, student_id, name):
        if student_id in self.students:
            raise ValueError("That student ID already exists.")
        self.students[student_id] = Student(student_id, name)

    def get_book(self, book_id):
        book = self.books.get(book_id)
        if book is None:
            raise ValueError("Unknown book ID.")
        return book

    def available_books(self):
        return [book for book in self.books.values() if book.borrowed_by is None]

    def lend(self, book_id, student_id):
        if student_id not in self.students:
            raise ValueError("Unknown student ID.")
        book = self.get_book(book_id)
        if book.borrowed_by is not None:
            raise ValueError("This book is already on loan.")
        book.borrowed_by = student_id

    def receive(self, book_id, student_id):
        book = self.get_book(book_id)
        if book.borrowed_by is None:
            raise ValueError("This book is already in the library.")
        if book.borrowed_by != student_id:
            raise ValueError("This book was borrowed by a different student.")
        book.borrowed_by = None

    def delete_book(self, book_id):
        if self.get_book(book_id).borrowed_by is not None:
            raise ValueError("Return the book before deleting it.")
        del self.books[book_id]

    def save(self, path):
        # Save plain dictionaries so the file is independent of class import names.
        payload = {
            "books": [
                (book.book_id, book.title, book.borrowed_by)
                for book in self.books.values()
            ],
            "students": [
                (student.student_id, student.name) for student in self.students.values()
            ],
        }
        with NamedTemporaryFile(dir=path.parent, delete=False) as file:
            temporary_path = Path(file.name)
            try:
                pickle.dump(payload, file)
                file.close()
                temporary_path.replace(path)
            finally:
                temporary_path.unlink(missing_ok=True)

    @classmethod
    def load(cls, path):
        # Pickle can execute code when loading. Use only this app's trusted local file.
        try:
            with path.open("rb") as file:
                payload = pickle.load(file)
        except FileNotFoundError:
            return cls()

        books = {book_id: Book(book_id, title, borrower)
                 for book_id, title, borrower in payload["books"]}
        students = {student_id: Student(student_id, name)
                    for student_id, name in payload["students"]}
        return cls(books=books, students=students)


def ask(prompt):
    answer = input(prompt).strip()
    if not answer:
        raise ValueError("Please enter a value.")
    return answer


def run_library(path):
    library = Library.load(path)
    menu = (
        "\n1. Available books\n2. Lend a book\n3. Receive a book\n"
        "4. Add a book\n5. Delete a book\n6. Register a student\n7. Exit"
    )
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice == "7":
            return
        if choice == "1":
            available = library.available_books()
            if not available:
                print("No books are currently available.")
            for book in available:
                print(f"{book.book_id} | {book.title}")
            continue

        try:
            if choice == "2":
                library.lend(ask("Book ID: "), ask("Student ID: "))
            elif choice == "3":
                library.receive(ask("Book ID: "), ask("Student ID: "))
            elif choice == "4":
                library.add_book(ask("Book ID: "), ask("Title: "))
            elif choice == "5":
                library.delete_book(ask("Book ID: "))
            elif choice == "6":
                library.add_student(ask("Student ID: "), ask("Name: "))
            else:
                print("Choose a number from 1 to 7.")
                continue
        except ValueError as error:
            print(error)
            continue

        library.save(path)
        print("Saved.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("library_data.pkl"))
    args = parser.parse_args()
    try:
        run_library(args.data)
    except EOFError:
        print("\nExiting.")
    except (OSError, pickle.UnpicklingError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
