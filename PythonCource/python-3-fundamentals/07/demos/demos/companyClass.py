# Import function import the module from the library
# from fucntion import the file from local directory

from employeeClass import Employee


class Company:
    def __init__(self):
        self.employees = []

    def add_employee(self, new_employee):
        self.employees.append(new_employee)


def main():
    my_company = Company()

    employee1 = Employee("Sarah", "Hess", 50000)
    my_company.add_employee(employee1)

    employee2 = Employee("Lee", "Smith", 25000)
    my_company.add_employee(employee2)

    employee3 = Employee("Bob", "Brown", 60000)
    my_company.add_employee(employee3)

    print(my_company.employees)


main()

# Example 2 , Display the Employess Name properly
from employeeClass import Employee


class Company:
    def __init__(self):
        self.employees = []

    def add_employee(self, new_employee):
        self.employees.append(new_employee)

    def display_employees(self):
        print("Current Employees:")
        for i in self.employees:
            print(i.fname, i.lname)
        print("----------")

    def pay_employees(self):
        print("Paying Employees:")
        for i in self.employees:
            print("Paycheck for:", i.fname, i.lname)
            print(
                "Amount:", i.calculate_paycheck()
            )  # Floting Value more than its required
            print(f"Amount:  ${i.calculate_paycheck():,.2f}")  # f string
            print("--------------------")


def main():
    my_company = Company()

    employee1 = Employee("Sarah", "Hess", 50000)
    my_company.add_employee(employee1)

    employee2 = Employee("Lee", "Smith", 25000)
    my_company.add_employee(employee2)

    employee3 = Employee("Bob", "Brown", 60000)
    my_company.add_employee(employee3)

    # print(my_company.employees)
    my_company.display_employees()
    my_company.pay_employees()


main()
