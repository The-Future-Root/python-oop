# Lesson 3: payroll
#
# Write Employee, Manager (inherits from Employee) and Contractor (inherits
# from Employee), and the payroll_total function. See README.md for the details.
# Test with:  python3 -m unittest -v


class Employee:
    role = "Employee"

    def __init__(self, name, annual_salary):
        pass

    def monthly_pay(self):
        """Annual salary divided by 12, rounded to 2 decimal places."""
        pass

    def describe(self):
        """Return "Alex Kim (Employee): $3,000.00 a month", using self.role and self.monthly_pay()."""
        pass


# Write the Manager class here: class Manager(Employee): ...


# Write the Contractor class here: class Contractor(Employee): ...


def payroll_total(staff):
    """Return the total monthly pay of everyone in the list, rounded to 2 decimal places."""
    pass


if __name__ == "__main__":
    alex = Employee("Alex Kim", 36000)
    print(alex.describe())
