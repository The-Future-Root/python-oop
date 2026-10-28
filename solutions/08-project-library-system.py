# Solution to project 8: library system

from abc import ABC, abstractmethod
from datetime import date, timedelta


class LibraryError(Exception):
    """Raised when a library operation isn't allowed."""


# Step 1: items

class Item(ABC):
    daily_fine = 0.25

    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title

    @abstractmethod
    def loan_days(self):
        """How many days this kind of item can be borrowed for."""

    @abstractmethod
    def __str__(self):
        """A one-line description."""


class Book(Item):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title)
        self.author = author

    def loan_days(self):
        return 21

    def __str__(self):
        return f"Book: {self.title} by {self.author}"


class DVD(Item):
    daily_fine = 1.00

    def __init__(self, item_id, title, minutes):
        super().__init__(item_id, title)
        self.minutes = minutes

    def loan_days(self):
        return 7

    def __str__(self):
        return f"DVD: {self.title} ({self.minutes} min)"


# Step 2: members and loans

class Member:
    def __init__(self, member_id, name, max_loans=3):
        """Store the values, and start with an empty loans list."""
        self.member_id = member_id
        self.name = name
        self.max_loans = max_loans
        self.loans = []

    def can_borrow(self):
        """True if the member has fewer loans than max_loans."""
        return len(self.loans) < self.max_loans


class Loan:
    def __init__(self, item, member, borrowed_on):
        """Store the values, and set due to borrowed_on plus the item's loan_days()."""
        self.item = item
        self.member = member
        self.borrowed_on = borrowed_on
        self.due = borrowed_on + timedelta(days=item.loan_days())

    def days_overdue(self, today):
        """Days past the due date (0 if not overdue)."""
        return max(0, (today - self.due).days)

    def fine(self, today):
        """days_overdue times the item's daily_fine, rounded to 2 decimal places."""
        return round(self.days_overdue(today) * self.item.daily_fine, 2)


# Step 3: the library

class Library:
    def __init__(self):
        """Start with no items, members or loans."""
        self._items = {}
        self._members = {}
        self._loans = {}

    def add_item(self, item):
        """Add an item, keyed by its item_id."""
        self._items[item.item_id] = item

    def add_member(self, member):
        """Add a member, keyed by their member_id."""
        self._members[member.member_id] = member

    def __len__(self):
        """The number of items in the library."""
        return len(self._items)

    def __contains__(self, item_id):
        """True if the library has an item with this id."""
        return item_id in self._items

    def find(self, text):
        """Items whose title or author contains text (any case), in the order they were added."""
        text = text.lower()
        results = []
        for item in self._items.values():
            author = getattr(item, "author", "")
            if text in item.title.lower() or text in author.lower():
                results.append(item)
        return results

    def is_available(self, item_id):
        """True if the item exists and isn't on loan."""
        return item_id in self._items and item_id not in self._loans

    def available_items(self):
        """A list of the items that aren't on loan."""
        return [item for item_id, item in self._items.items() if item_id not in self._loans]

    def checkout(self, item_id, member_id, today):
        """Lend an item to a member and return the new Loan. Raise LibraryError if it isn't allowed."""
        if item_id not in self._items:
            raise LibraryError(f"No item with id {item_id}")
        if member_id not in self._members:
            raise LibraryError(f"No member with id {member_id}")
        item = self._items[item_id]
        member = self._members[member_id]
        if item_id in self._loans:
            raise LibraryError(f"{item.title} is already on loan")
        if not member.can_borrow():
            raise LibraryError(f"{member.name} has reached the loan limit")
        loan = Loan(item, member, today)
        self._loans[item_id] = loan
        member.loans.append(loan)
        return loan

    def return_item(self, item_id, today):
        """End the loan and return the fine owed. Raise LibraryError if the item isn't on loan."""
        if item_id not in self._loans:
            raise LibraryError(f"{item_id} isn't on loan")
        loan = self._loans.pop(item_id)
        loan.member.loans.remove(loan)
        return loan.fine(today)

    def overdue(self, today):
        """Loans that are past their due date, the most overdue first."""
        late = [loan for loan in self._loans.values() if loan.days_overdue(today) > 0]
        late.sort(key=lambda loan: loan.days_overdue(today), reverse=True)
        return late


if __name__ == "__main__":
    library = Library()
    library.add_item(Book("B1", "Clean Code", "Robert C. Martin"))
    library.add_item(DVD("D1", "Arrival", 116))
    library.add_member(Member("M1", "Alex Kim"))
    loan = library.checkout("D1", "M1", date(2026, 3, 1))
    print(loan.item, "is due back on", loan.due)
    print("Fine:", library.return_item("D1", date(2026, 3, 11)))
