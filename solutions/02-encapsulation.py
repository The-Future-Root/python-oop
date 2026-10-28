# Solution to lesson 2: a bank account


class BankAccount:
    def __init__(self, owner, balance=0):
        """Store owner, the balance in _balance, and an empty _transactions list."""
        if balance < 0:
            raise ValueError("Balance can't be negative")
        self.owner = owner
        self._balance = balance
        self._transactions = []

    @property
    def balance(self):
        """The current balance (read-only)."""
        return self._balance

    def deposit(self, amount):
        """Add amount, and record ("deposit", amount)."""
        if amount <= 0:
            raise ValueError("Deposit must be more than zero")
        self._balance += amount
        self._transactions.append(("deposit", amount))

    def withdraw(self, amount):
        """Take amount away, and record ("withdrawal", amount)."""
        if amount <= 0:
            raise ValueError("Withdrawal must be more than zero")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append(("withdrawal", amount))

    @property
    def transactions(self):
        """A copy of the transaction history (read-only)."""
        return list(self._transactions)

    def statement(self):
        """Return one line per transaction, then the balance."""
        lines = [f"{kind}: ${amount:.2f}" for kind, amount in self._transactions]
        lines.append(f"Balance: ${self._balance:.2f}")
        return "\n".join(lines)


if __name__ == "__main__":
    account = BankAccount("Alex Kim", 100)
    account.deposit(50)
    account.withdraw(30)
    print(account.statement())
