import unittest

import exercise
from exercise import Employee, payroll_total


def get(name):
    cls = getattr(exercise, name, None)
    if cls is None:
        raise AssertionError(f"Write a class called {name} in exercise.py")
    return cls


class TestEmployee(unittest.TestCase):
    def test_attributes(self):
        alex = Employee("Alex Kim", 36000)
        self.assertEqual((alex.name, alex.annual_salary), ("Alex Kim", 36000))

    def test_monthly_pay(self):
        self.assertEqual(Employee("Alex Kim", 36000).monthly_pay(), 3000.0)
        self.assertEqual(Employee("Priya", 40000).monthly_pay(), 3333.33)

    def test_describe(self):
        self.assertEqual(Employee("Alex Kim", 36000).describe(), "Alex Kim (Employee): $3,000.00 a month")


class TestManager(unittest.TestCase):
    def test_is_an_employee(self):
        Manager = get("Manager")
        self.assertTrue(issubclass(Manager, Employee), "Manager should inherit from Employee")

    def test_team_starts_empty_and_separate(self):
        Manager = get("Manager")
        a, b = Manager("Sam", 48000), Manager("Jo", 48000)
        a.add_to_team(Employee("Alex", 36000))
        self.assertEqual(len(a.team), 1)
        self.assertEqual(b.team, [], "Each manager needs their own team list")

    def test_pay_with_team(self):
        Manager = get("Manager")
        sam = Manager("Sam Rivera", 48000)
        self.assertEqual(sam.monthly_pay(), 4000.0)
        sam.add_to_team(Employee("Alex", 36000))
        sam.add_to_team(Employee("Priya", 36000))
        self.assertEqual(sam.monthly_pay(), 4200.0)

    def test_describe_inherited(self):
        Manager = get("Manager")
        sam = Manager("Sam Rivera", 48000)
        sam.add_to_team(Employee("Alex", 36000))
        self.assertEqual(sam.describe(), "Sam Rivera (Manager): $4,100.00 a month")
        self.assertNotIn("describe", vars(Manager), "Don't write describe() again in Manager; inherit it")


class TestContractor(unittest.TestCase):
    def test_is_an_employee(self):
        Contractor = get("Contractor")
        self.assertTrue(issubclass(Contractor, Employee), "Contractor should inherit from Employee")

    def test_pay(self):
        Contractor = get("Contractor")
        jo = Contractor("Jo Park", 42.5, 80)
        self.assertEqual(jo.name, "Jo Park")
        self.assertEqual(jo.annual_salary, 0)
        self.assertEqual(jo.monthly_pay(), 3400.0)

    def test_describe(self):
        Contractor = get("Contractor")
        self.assertEqual(Contractor("Jo Park", 42.5, 80).describe(), "Jo Park (Contractor): $3,400.00 a month")


class TestPayroll(unittest.TestCase):
    def test_mixed_staff(self):
        Manager, Contractor = get("Manager"), get("Contractor")
        sam = Manager("Sam", 48000)
        alex = Employee("Alex", 36000)
        sam.add_to_team(alex)
        staff = [alex, sam, Contractor("Jo", 42.5, 80)]
        self.assertEqual(payroll_total(staff), 10500.0)

    def test_empty(self):
        self.assertEqual(payroll_total([]), 0)


if __name__ == "__main__":
    unittest.main()
