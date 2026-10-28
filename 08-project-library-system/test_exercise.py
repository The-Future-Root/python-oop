import unittest
from datetime import date

import exercise
from exercise import LibraryError

MARCH_1 = date(2026, 3, 1)


def get(name):
    cls = getattr(exercise, name, None)
    if cls is None:
        raise AssertionError(f"Write a class called {name} in exercise.py")
    return cls


def sample_library():
    Library, Book, DVD, Member = get("Library"), get("Book"), get("DVD"), get("Member")
    library = Library()
    library.add_item(Book("B1", "Clean Code", "Robert C. Martin"))
    library.add_item(Book("B2", "The Pragmatic Programmer", "Andy Hunt"))
    library.add_item(Book("B3", "Python Crash Course", "Eric Matthes"))
    library.add_item(DVD("D1", "Arrival", 116))
    library.add_member(Member("M1", "Alex Kim"))
    library.add_member(Member("M2", "Sam Rivera", max_loans=1))
    return library


class TestStep1Items(unittest.TestCase):
    def test_item_is_abstract(self):
        with self.assertRaises(TypeError, msg="Item should be an abstract base class"):
            get("Item")("X1", "Something")

    def test_book(self):
        book = get("Book")("B1", "Clean Code", "Robert C. Martin")
        self.assertIsInstance(book, get("Item"))
        self.assertEqual((book.item_id, book.title, book.author), ("B1", "Clean Code", "Robert C. Martin"))
        self.assertEqual(book.loan_days(), 21)
        self.assertEqual(book.daily_fine, 0.25)
        self.assertEqual(str(book), "Book: Clean Code by Robert C. Martin")

    def test_dvd(self):
        dvd = get("DVD")("D1", "Arrival", 116)
        self.assertIsInstance(dvd, get("Item"))
        self.assertEqual(dvd.loan_days(), 7)
        self.assertEqual(dvd.daily_fine, 1.00)
        self.assertEqual(str(dvd), "DVD: Arrival (116 min)")


class TestStep2MembersAndLoans(unittest.TestCase):
    def test_member(self):
        alex = get("Member")("M1", "Alex Kim")
        self.assertEqual((alex.member_id, alex.name, alex.max_loans, alex.loans), ("M1", "Alex Kim", 3, []))
        self.assertTrue(alex.can_borrow())

    def test_loan_due_date(self):
        Loan = get("Loan")
        alex = get("Member")("M1", "Alex Kim")
        self.assertEqual(Loan(get("Book")("B1", "Clean Code", "R. M."), alex, MARCH_1).due, date(2026, 3, 22))
        self.assertEqual(Loan(get("DVD")("D1", "Arrival", 116), alex, MARCH_1).due, date(2026, 3, 8))

    def test_overdue_and_fines(self):
        loan = get("Loan")(get("DVD")("D1", "Arrival", 116), get("Member")("M1", "Alex"), MARCH_1)
        self.assertEqual(loan.days_overdue(date(2026, 3, 8)), 0)
        self.assertEqual(loan.fine(date(2026, 3, 8)), 0)
        self.assertEqual(loan.days_overdue(date(2026, 3, 11)), 3)
        self.assertEqual(loan.fine(date(2026, 3, 11)), 3.0)

    def test_book_fine(self):
        loan = get("Loan")(get("Book")("B1", "Clean Code", "R. M."), get("Member")("M1", "Alex"), MARCH_1)
        self.assertEqual(loan.fine(date(2026, 3, 28)), 1.5)


class TestStep3Library(unittest.TestCase):
    def test_len_and_in(self):
        library = sample_library()
        self.assertEqual(len(library), 4)
        self.assertIn("B2", library)
        self.assertNotIn("B9", library)

    def test_find(self):
        library = sample_library()
        self.assertEqual([i.item_id for i in library.find("python")], ["B3"])
        self.assertEqual([i.item_id for i in library.find("hunt")], ["B2"], "Search authors too")
        self.assertEqual([i.item_id for i in library.find("ARRIVAL")], ["D1"])
        self.assertEqual(library.find("knitting"), [])

    def test_checkout_and_return(self):
        library = sample_library()
        loan = library.checkout("D1", "M1", MARCH_1)
        self.assertEqual(loan.due, date(2026, 3, 8))
        self.assertFalse(library.is_available("D1"))
        self.assertNotIn("D1", [i.item_id for i in library.available_items()])
        self.assertEqual(library.return_item("D1", date(2026, 3, 11)), 3.0)
        self.assertTrue(library.is_available("D1"))

    def test_member_tracks_loans(self):
        library = sample_library()
        library.checkout("B1", "M1", MARCH_1)
        loan = library.checkout("B2", "M1", MARCH_1)
        self.assertIn(loan, loan.member.loans)
        library.return_item("B2", MARCH_1)
        self.assertNotIn(loan, loan.member.loans, "Returning an item should remove the loan from the member")

    def test_checkout_errors(self):
        library = sample_library()
        cases = [(("B9", "M1"), "No item with id B9"), (("B1", "M9"), "No member with id M9")]
        for args, message in cases:
            with self.assertRaises(LibraryError) as caught:
                library.checkout(*args, MARCH_1)
            self.assertEqual(str(caught.exception), message)
        library.checkout("B1", "M1", MARCH_1)
        with self.assertRaises(LibraryError) as caught:
            library.checkout("B1", "M1", MARCH_1)
        self.assertEqual(str(caught.exception), "Clean Code is already on loan")

    def test_loan_limit(self):
        library = sample_library()
        library.checkout("B1", "M2", MARCH_1)
        with self.assertRaises(LibraryError) as caught:
            library.checkout("B2", "M2", MARCH_1)
        self.assertEqual(str(caught.exception), "Sam Rivera has reached the loan limit")

    def test_return_not_on_loan(self):
        with self.assertRaises(LibraryError) as caught:
            sample_library().return_item("B1", MARCH_1)
        self.assertEqual(str(caught.exception), "B1 isn't on loan")

    def test_overdue_most_overdue_first(self):
        library = sample_library()
        library.checkout("B1", "M1", MARCH_1)               # due 22 March
        library.checkout("D1", "M1", MARCH_1)               # due 8 March
        library.checkout("B2", "M1", date(2026, 3, 20))     # due 10 April
        late = library.overdue(date(2026, 3, 25))
        self.assertEqual([loan.item.item_id for loan in late], ["D1", "B1"])

    def test_library_error_is_an_exception(self):
        self.assertTrue(issubclass(LibraryError, Exception))


if __name__ == "__main__":
    unittest.main()
