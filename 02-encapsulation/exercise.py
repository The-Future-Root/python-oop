# Lesson 2: a bank account
#
# Write the BankAccount class. The table in README.md says what each part does.
# Test with:  python3 -m unittest -v


class BankAccount:
    def __init__(self, owner, balance=0):
        """Store owner, the balance in _balance, and an empty _transactions list.
        Raise ValueError("Balance can't be negative") for a negative balance."""
        pass

    # Add the read-only `balance` property here.

    def deposit(self, amount):
        """Add amount, and record ("deposit", amount)."""
        pass

    def withdraw(self, amount):
        """Take amount away, and record ("withdrawal", amount)."""
        pass

    # Add the read-only `transactions` property here. It returns a copy of the list.

    def statement(self):
        """Return one line per transaction, then the balance."""
        pass


if __name__ == "__main__":
    account = BankAccount("Alex Kim", 100)
    account.deposit(50)
    account.withdraw(30)
    print(account.statement())
