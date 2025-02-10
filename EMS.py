import os
import json
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# File for data persistence
DATABASE_FILE = "employee_data.json"


class Employee:
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
        }


class Department:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def department_performance_report(data):
        print(Fore.CYAN + "\n=== Department Performance Summary ===")
        departments = {}
        for emp in data:
            dep = emp["department"]
            if dep not in departments:
                departments[dep] = 0
            departments[dep] += emp["salary"]

        for dep, total_salary in departments.items():
            print(f"{dep}: Total Salary - ${total_salary}")
        print(Fore.CYAN + "=======================================")


class PerformanceReview:
    def __init__(self, employee_id, review):
        self.employee_id = employee_id
        self.review = review

    @staticmethod
    def add_review(employee_id, review, data):
        for emp in data:
            if emp["id"] == employee_id:
                emp["performance_review"] = review
                return True
        return False


class EmployeeManagementSystem:
    def __init__(self):
        self.employees = self.load_data()

    def load_data(self):
        if not os.path.exists(DATABASE_FILE):
            return []
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)

    def save_data(self):
        with open(DATABASE_FILE, "w") as file:
            json.dump(self.employees, file, indent=4)

    def create_employee(self):
        id = input("Enter Employee ID: ")
        name = input("Enter Employee Name: ")
        department = input("Enter Department: ")
        salary = float(input("Enter Salary: "))
        new_employee = Employee(id, name, department, salary)
        self.employees.append(new_employee.to_dict())
        self.save_data()
        print(Fore.GREEN + "Employee record added successfully!")

    def read_employees(self):
        print(Fore.CYAN + "\n=== Employee Records ===")
        for emp in self.employees:
            print(f"ID: {emp['id']}, Name: {emp['name']}, "
                  f"Department: {emp['department']}, Salary: ${emp['salary']}")
        print(Fore.CYAN + "=========================")

    def update_employee(self):
        id = input("Enter Employee ID to Update: ")
        for emp in self.employees:
            if emp["id"] == id:
                emp["name"] = input("Enter New Name: ")
                emp["department"] = input("Enter New Department: ")
                emp["salary"] = float(input("Enter New Salary: "))
                self.save_data()
                print(Fore.GREEN + "Employee record updated successfully!")
                return
        print(Fore.RED + "Employee not found!")

    def delete_employee(self):
        id = input("Enter Employee ID to Delete: ")
        self.employees = [emp for emp in self.employees if emp["id"] != id]
        self.save_data()
        print(Fore.GREEN + "Employee record deleted successfully!")

    def search_employee(self):
        criteria = input("Search by (id/name/department): ").lower()
        keyword = input("Enter Search Keyword: ")
        print(Fore.CYAN + "\n=== Search Results ===")
        for emp in self.employees:
            if (criteria == "id" and emp["id"] == keyword) or \
               (criteria == "name" and keyword.lower() in emp["name"].lower()) or \
               (criteria == "department" and keyword.lower() in emp["department"].lower()):
                print(f"ID: {emp['id']}, Name: {emp['name']}, "
                      f"Department: {emp['department']}, Salary: ${emp['salary']}")
        print(Fore.CYAN + "=======================")

    def manage_promotions(self):
        id = input("Enter Employee ID for Promotion: ")
        increment = float(input("Enter Salary Increment: "))
        for emp in self.employees:
            if emp["id"] == id:
                emp["salary"] += increment
                self.save_data()
                print(Fore.GREEN + "Salary updated successfully!")
                return
        print(Fore.RED + "Employee not found!")

    def add_performance_review(self):
        id = input("Enter Employee ID for Review: ")
        review = input("Enter Performance Review: ")
        if PerformanceReview.add_review(id, review, self.employees):
            self.save_data()
            print(Fore.GREEN + "Performance review added successfully!")
        else:
            print(Fore.RED + "Employee not found!")

    def department_summary(self):
        Department.department_performance_report(self.employees)

    def display_menu(self):
        print(Fore.YELLOW + """
=== Employee Management System ===
1. Add Employee
2. View Employees
3. Update Employee
4. Delete Employee
5. Search Employee
6. Manage Promotions
7. Add Performance Review
8. Department Summary
9. Exit
===================================
""")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_employee()
            elif choice == "2":
                self.read_employees()
            elif choice == "3":
                self.update_employee()
            elif choice == "4":
                self.delete_employee()
            elif choice == "5":
                self.search_employee()
            elif choice == "6":
                self.manage_promotions()
            elif choice == "7":
                self.add_performance_review()
            elif choice == "8":
                self.department_summary()
            elif choice == "9":
                print(Fore.MAGENTA + "Exiting the system. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid choice! Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.run()
