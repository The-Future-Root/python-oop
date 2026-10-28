# Project 8: library system
#
# Build it in the steps described in README.md, running the tests after each step:
#     python3 -m unittest -v
# The class and method names are all here. Replace each `pass` with your code,
# and decide which methods of Item need @abstractmethod.

from abc import ABC, abstractmethod
from datetime import date, timedelta


class LibraryError(Exception):
    """Raised when a library operation isn't allowed."""


# Step 1: items

class Item(ABC):
    daily_fine = 0.25

    def __init__(self, item_id, title):
        pass

    def loan_days(self):
        """How many days this kind of item can be borrowed for."""
        pass

    def __str__(self):
        """A one-line description."""
        pass


class Book(Item):
    def __init__(self, item_id, title, author):
        pass

    def loan_days(self):
        pass

    def __str__(self):
        pass


class DVD(Item):
    daily_fine = 1.00

    def __init__(self, item_id, title, minutes):
        pass

    def loan_days(self):
        pass

    def __str__(self):
        pass


# Step 2: members and loans

class Member:
    def __init__(self, member_id, name, max_loans=3):
        """Store the values, and start with an empty loans list."""
        pass

    def can_borrow(self):
        """True if the member has fewer loans than max_loans."""
        pass


class Loan:
    def __init__(self, item, member, borrowed_on):
        """Store the values, and set due to borrowed_on plus the item's loan_days()."""
        pass

    def days_overdue(self, today):
        """Days past the due date (0 if not overdue)."""
        pass

    def fine(self, today):
        """days_overdue times the item's daily_fine, rounded to 2 decimal places."""
        pass


# Step 3: the library

class Library:
    def __init__(self):
        """Start with no items, members or loans."""
        pass

    def add_item(self, item):
        """Add an item, keyed by its item_id."""
        pass

    def add_member(self, member):
        """Add a member, keyed by their member_id."""
        pass

    def __len__(self):
        """The number of items in the library."""
        pass

    def __contains__(self, item_id):
        """True if the library has an item with this id."""
        pass

    def find(self, text):
        """Items whose title or author contains text (any case), in the order they were added."""
        pass

    def is_available(self, item_id):
        """True if the item exists and isn't on loan."""
        pass

    def available_items(self):
        """A list of the items that aren't on loan."""
        pass

    def checkout(self, item_id, member_id, today):
        """Lend an item to a member and return the new Loan. Raise LibraryError if it isn't allowed."""
        pass

    def return_item(self, item_id, today):
        """End the loan and return the fine owed. Raise LibraryError if the item isn't on loan."""
        pass

    def overdue(self, today):
        """Loans that are past their due date, the most overdue first."""
        pass


if __name__ == "__main__":
    library = Library()
    library.add_item(Book("B1", "Clean Code", "Robert C. Martin"))
    library.add_item(DVD("D1", "Arrival", 116))
    library.add_member(Member("M1", "Alex Kim"))
    loan = library.checkout("D1", "M1", date(2026, 3, 1))
    print(loan.item, "is due back on", loan.due)
    print("Fine:", library.return_item("D1", date(2026, 3, 11)))
