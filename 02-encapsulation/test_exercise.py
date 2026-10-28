import unittest

from exercise import BankAccount


class TestCreating(unittest.TestCase):
    def test_owner_and_balance(self):
        account = BankAccount("Alex Kim", 100)
        self.assertEqual(account.owner, "Alex Kim")
        self.assertEqual(account.balance, 100)

    def test_default_balance(self):
        self.assertEqual(BankAccount("Sam").balance, 0)

    def test_negative_start(self):
        with self.assertRaises(ValueError) as caught:
            BankAccount("Sam", -10)
        self.assertEqual(str(caught.exception), "Balance can't be negative")


class TestProtection(unittest.TestCase):
    def test_balance_is_read_only(self):
        account = BankAccount("Alex", 100)
        with self.assertRaises(AttributeError, msg="balance should be a property with no setter"):
            account.balance = 1_000_000
        self.assertEqual(account.balance, 100)

    def test_stored_in_underscore_attribute(self):
        self.assertEqual(BankAccount("Alex", 70)._balance, 70)

    def test_transactions_is_a_copy(self):
        account = BankAccount("Alex", 100)
        account.deposit(10)
        account.transactions.append(("deposit", 1_000_000))
        self.assertEqual(account.transactions, [("deposit", 10)], "Return a copy, so outside code can't change the history")


class TestDepositAndWithdraw(unittest.TestCase):
    def test_deposit(self):
        account = BankAccount("Alex", 100)
        account.deposit(50)
        self.assertEqual(account.balance, 150)

    def test_bad_deposit(self):
        account = BankAccount("Alex", 100)
        for amount in (0, -20):
            with self.assertRaises(ValueError) as caught:
                account.deposit(amount)
            self.assertEqual(str(caught.exception), "Deposit must be more than zero")
        self.assertEqual(account.balance, 100)

    def test_withdraw(self):
        account = BankAccount("Alex", 100)
        account.withdraw(30)
        self.assertEqual(account.balance, 70)

    def test_insufficient_funds(self):
        account = BankAccount("Alex", 100)
        with self.assertRaises(ValueError) as caught:
            account.withdraw(150)
        self.assertEqual(str(caught.exception), "Insufficient funds")
        self.assertEqual(account.balance, 100)
        self.assertEqual(account.transactions, [], "A failed withdrawal shouldn't be recorded")

    def test_bad_withdrawal(self):
        with self.assertRaises(ValueError) as caught:
            BankAccount("Alex", 100).withdraw(0)
        self.assertEqual(str(caught.exception), "Withdrawal must be more than zero")

    def test_transactions(self):
        account = BankAccount("Alex", 100)
        account.deposit(50)
        account.withdraw(30)
        self.assertEqual(account.transactions, [("deposit", 50), ("withdrawal", 30)])


class TestStatement(unittest.TestCase):
    def test_statement(self):
        account = BankAccount("Alex", 100)
        account.deposit(50)
        account.withdraw(30)
        self.assertEqual(account.statement(), "deposit: $50.00\nwithdrawal: $30.00\nBalance: $120.00")

    def test_empty_statement(self):
        self.assertEqual(BankAccount("Sam", 5).statement(), "Balance: $5.00")


if __name__ == "__main__":
    unittest.main()
