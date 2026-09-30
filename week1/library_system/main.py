class BorrowLimitError(Exception):
    pass


class BookUnavailableError(Exception):
    pass


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.borrowed = False


class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []
        self.borrow_limit = 3

    def borrow_book(self, book):
        if len(self.borrowed_books) >= self.borrow_limit:
            raise BorrowLimitError(
                f"You cannot borrow more than {self.borrow_limit} books"
            )

        if book.borrowed:
            raise BookUnavailableError(
                "Book is not available at the moment"
            )

        book.borrowed = True
        self.borrowed_books.append(book)

    def return_book(self, book):
        book.borrowed = False
        self.borrowed_books.remove(book)


class PremiumMember(Member):
    def __init__(self, name):
        super().__init__(name)
        self.borrow_limit = 5


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def add_member(self, member):
        self.members.append(member)

    def __str__(self):
        result = "Library:\n"

        result += "Books:\n"
        for book in self.books:
            status = "Borrowed" if book.borrowed else "Available"
            result += f"- {book.title} by {book.author} ({status})\n"

        result += "\nMembers:\n"
        for member in self.members:
            result += f"- {member.name}: {len(member.borrowed_books)} books borrowed\n"

        return result