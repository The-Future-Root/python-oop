# Solution to lesson 3: payroll


class Employee:
    role = "Employee"

    def __init__(self, name, annual_salary):
        self.name = name
        self.annual_salary = annual_salary

    def monthly_pay(self):
        """Annual salary divided by 12, rounded to 2 decimal places."""
        return round(self.annual_salary / 12, 2)

    def describe(self):
        """Return "Alex Kim (Employee): $3,000.00 a month"."""
        return f"{self.name} ({self.role}): ${self.monthly_pay():,.2f} a month"


class Manager(Employee):
    role = "Manager"

    def __init__(self, name, annual_salary):
        super().__init__(name, annual_salary)
        self.team = []

    def add_to_team(self, employee):
        self.team.append(employee)

    def monthly_pay(self):
        """Normal pay plus $100 for each person in the team."""
        return round(super().monthly_pay() + 100 * len(self.team), 2)


class Contractor(Employee):
    role = "Contractor"

    def __init__(self, name, hourly_rate, hours_per_month):
        super().__init__(name, 0)
        self.hourly_rate = hourly_rate
        self.hours_per_month = hours_per_month

    def monthly_pay(self):
        """Hourly rate times hours per month, rounded to 2 decimal places."""
        return round(self.hourly_rate * self.hours_per_month, 2)


def payroll_total(staff):
    """Return the total monthly pay of everyone in the list, rounded to 2 decimal places."""
    total = 0
    for person in staff:
        total += person.monthly_pay()
    return round(total, 2)


if __name__ == "__main__":
    alex = Employee("Alex Kim", 36000)
    sam = Manager("Sam Rivera", 48000)
    sam.add_to_team(alex)
    jo = Contractor("Jo Park", 42.5, 80)
    for person in (alex, sam, jo):
        print(person.describe())
    print("Total:", payroll_total([alex, sam, jo]))
