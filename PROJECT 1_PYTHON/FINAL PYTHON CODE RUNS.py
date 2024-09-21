import mysql.connector

cmd = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Python123",
    database="Employeedb"
)

user_credentials = {"kaviya": "suji34"}
mycursor = cmd.cursor()

# Your database operations using mycursor here
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in user_credentials and user_credentials[username] == password:
        print("Login successful.")
        return True
    else:
        print("Invalid username or password.")
        return False


class Employee:
    def __init__(self, emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions):
        self.emp_id = emp_id
        self.name = name
        self.years_of_experience = years_of_experience
        self.age = age
        self.qualification = qualification
        self.salary = salary
        self.bonuses = bonuses
        self.deductions = deductions
        self.performance_scores = {}  # Initialize performance_scores as an empty dictionary

    def add_performance_score(self, criteria, score):
        self.performance_scores[criteria] = score

    def get_average_performance_score(self):
        if self.performance_scores:
            return sum(self.performance_scores.values()) / len(self.performance_scores)
        else:
            return 0


class PerformanceEvaluator:
    def __init__(self):
        self.employees = {}  # Initialize the employees dictionary to store employee objects
        self.load_employees_from_database()  # Load employee data from the database during initialization
    
    def load_employees_from_database(self):
        # Query the database to retrieve all employee details
        mycursor.execute("SELECT * FROM employees")
        employees_data = mycursor.fetchall()
        
        # Iterate through the retrieved employee details
        for emp_data in employees_data:
            # Unpack employee data
            emp_id = emp_data[0]  # Assuming emp_id is always the first column
            name = emp_data[1]  # Assuming name is the second column
            years_of_experience = emp_data[2]  # Assuming years_of_experience is the third column
            age = emp_data[3]  # Assuming age is the fourth column
            qualification = emp_data[4]  # Assuming qualification is the fifth column
            salary = emp_data[5]  # Assuming salary is the sixth column
            bonuses = emp_data[6]  # Assuming bonuses is the seventh column
            deductions = emp_data[7]  # Assuming deductions is the eighth column
            # Create an Employee object with the retrieved details
            employee = Employee(emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions)
            # Add the Employee object to the employees dictionary
            self.employees[emp_id] = employee



    # Method to add a new employee
    def add_employee(self):
        emp_id = int(input("\nEnter employee ID: "))  
        name = input("Enter employee name: ")  
        years_of_experience = int(input("Enter years of experience: "))  
        age = int(input("Enter age: "))  
        qualification = input("Enter qualification: ")
        salary = float(input("Enter salary: "))  # Add this line to get the salary input
        bonuses = float(input("Enter bonuses: "))  # Add this line to get the bonuses input
        deductions = float(input("Enter deductions: "))  # Add this line to get the deductions input
        
        if emp_id not in self.employees:
            self.employees[emp_id] = Employee(emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions)
            sql = "INSERT INTO employees (emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions)
            mycursor.execute(sql, val)
            cmd.commit()
            print("Employee added successfully!")
        else:
            print("Employee with this ID already exists.") 

    # Method to update employee details
    def update_employee(self):
        emp_id = int(input("\nEnter employee ID to update: "))
        print("Which field you want to update:")
        mycursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        employee = mycursor.fetchone()
        if employee:
            print(f"\nUpdating details for {employee[1]}:")
            while True:
                print("1. Name")
                print("2. Years of Experience")
                print("3. Age")
                print("4. Qualification")
                print("5. Salary")
                print("6. Bonuses")
                print("7. Deductions")
                print("8. Done")
                choice = int(input("Enter your choice: "))
                if choice == 8:
                    break
                self.update_field(emp_id, choice)

            print("Employee details updated successfully.")
        else:
            print("\nEmployee not found.")

    def update_field(self, emp_id, choice):
        field_names = {
            1: 'name',
            2: 'years_of_experience',
            3: 'age',
            4: 'qualification',
            5: 'salary',
            6: 'bonuses',
            7: 'deductions',
        }
        field_name = field_names.get(choice)
        if field_name:
            new_value = input(f"Enter new value to update in {field_name}: ")
            mycursor.execute(f"UPDATE employees SET {field_name} = %s WHERE emp_id = %s", (new_value, emp_id))
            if choice in [5, 6, 7]:  # Check if the chosen field affects payroll
                self.recalculate_payroll(emp_id)
            cmd.commit()
            print("Field updated successfully.")
        else:
            print("Invalid choice. Please select a valid option.")

    def recalculate_payroll(self, emp_id):
        query = "SELECT salary, bonuses, deductions FROM employees WHERE emp_id = %s"
        mycursor.execute(query, (emp_id,))
        employee_data = mycursor.fetchone()
        if employee_data:
            salary, bonuses, deductions = employee_data
            net_pay = salary + bonuses - deductions
            update_query = "UPDATE employees SET payroll = %s WHERE emp_id = %s"
            mycursor.execute(update_query, (net_pay, emp_id))
            print("Payroll recalculated and updated successfully.")
        else:
            print("Employee not found while recalculating payroll.")

    # Method to delete an employee
    def delete_employee(self):
        emp_id = int(input("\nEnter employee ID to delete: "))  

        # Construct the SQL query to delete the employee with the given ID
        query = "DELETE FROM employees WHERE emp_id = %s"

        # Execute the query
        mycursor.execute(query, (emp_id,))

        # Check if any rows were affected (employee deleted)
        if mycursor.rowcount > 0:
            print("Employee deleted successfully.")
            cmd.commit()  # Commit the transaction
        else:
            print("\nEmployee not found.")

    def show_employee_details(self):
        emp_id = int(input("\nEnter employee ID to show details: "))
        query = "SELECT * FROM employees WHERE emp_id = %s"
        mycursor.execute(query, (emp_id,))
        employee = mycursor.fetchone()
        if employee:
            print(f"\nEmployee Details for ID {emp_id}:")
            print("Name:", employee[1])
            print("Years of Experience:", employee[2])
            print("Age:", employee[3])
            print("Qualification:", employee[4])
            print("Payroll:", employee[8]) 
        else:
            print("\nEmployee not found.")

            
    # Method to conduct evaluation for an employee
    def conduct_evaluation(self):
        emp_id = int(input("\nEnter employee ID for evaluation: "))
        if emp_id in self.employees:
            employee = self.employees[emp_id]
            print(f"\nConducting evaluation for {employee.name}:")
            
            # Display menu of evaluation criteria
            print("Select evaluation criteria:")
            print("1. Leadership Skills")
            print("2. Teamwork")
            print("3. Problem Solving")
            print("4. Communication Skills")
            
            choice = int(input("Enter your choice: "))
            
            # Map user's choice to criteria
            criteria_map = {
                1: "Leadership Skills",
                2: "Teamwork",
                3: "Problem Solving",
                4: "Communication Skills"
            }
            
            # Retrieve the chosen criteria
            criteria = criteria_map.get(choice)
            
            if criteria:
                score = float(input("Enter performance score (0-10): "))
                employee.add_performance_score(criteria, score)
            else:
                print("Invalid choice.")
        else:
            print("\nEmployee not found.")

    # Method to get high performers
    def get_high_performers(self):
        high_performers = {}
        threshold_score = 8  # Define the threshold for high performance
        
        for emp_id, employee in self.employees.items():
            average_score = employee.get_average_performance_score()
            if average_score >= threshold_score:
                high_performers[employee.name] = average_score

        return high_performers 


# Define the Volunteer and VolunteerCoordinator classes
class Volunteer:
    def __init__(self, emp_id, name):
        # Constructor to initialize volunteer details
        self.emp_id = emp_id  # Employee ID
        self.name = name  # Employee name
        self.activities = []  # List to store volunteered activities

    def add_activity(self, activity):
        # Method to add volunteered activity
        self.activities.append(activity)  # Add activity to the list

    def get_activities(self):
        # Method to get volunteered activities
        return self.activities  # Return list of activities


class VolunteerCoordinator:
    def __init__(self):
        # Constructor to initialize VolunteerCoordinator object
        self.volunteers = {}  # Dictionary to store volunteers
        self.activities_available = {
            # Dictionary to store available activities with corresponding numeric keys
            1: "Organizing Seminars or Workshops",
            2: "Mentoring Student Clubs or Societies",
            3: "Participating in Career Guidance Programs",
            4: "Coordinating Research Projects",
            5: "Leading Professional Development Sessions",
            6: "Hosting Conferences or Symposia",
            7: "Supervising Student Research or Internships",
            8: "Facilitating Industry-Academia Collaboration",
            9: "Contributing to Curriculum Development",
            10: "Serving on Academic Committees"
        }

    def add_volunteer(self):
        # Method to add a new volunteer
        print()  # Add spacing
        emp_id = int(input("Enter employee ID: "))  # Get employee ID from user
        name = input("Enter employee name: ")  # Get employee name from user
        if emp_id not in self.volunteers:
            # Check if employee ID already exists
            self.volunteers[emp_id] = Volunteer(emp_id, name)  # Create and add new Volunteer object
            print(f"Employee {name} added as a volunteer successfully.")  # Print success message
        else:
            print("Employee with this ID is already a volunteer.")  # Print error message if employee ID already exists

    def record_activity(self):
        # Method to record volunteered activity for an employee
        print()  # Add spacing
        emp_id = int(input("Enter employee ID for recording activity: "))  # Get employee ID for recording activity
        if emp_id in self.volunteers:
            # Check if employee ID exists
            volunteer = self.volunteers[emp_id]  # Get Volunteer object
            print()  # Add spacing
            print("Choose an activity:")
            for key, activity in self.activities_available.items():
                # Print available activities
                print(f"{key}: {activity}")
            print()  # Add spacing
            activity_choice = int(input("Enter activity choice: "))  # Get activity choice from user
            if activity_choice in self.activities_available:
                # Check if activity choice is valid
                activity = self.activities_available[activity_choice]  # Get selected activity
                volunteer.add_activity(activity)  # Add activity to the volunteer's activities
                print(f"Activity '{activity}' recorded for employee {volunteer.name}.")  # Print success message
            else:
                print("Invalid activity choice.")  # Print error message for invalid choice
        else:
                        print("Employee with this id is not a volunteer. ")  # Print error message if employee ID doesn't exist

# Define functions for each module
def add_employee():
    evaluator.add_employee()

def update_employee():
    evaluator.update_employee()

def delete_employee():
    evaluator.delete_employee()
    
def performance_evaluation():
    evaluator.conduct_evaluation()
    high_performers = evaluator.get_high_performers()
    print("\nHigh Performers:")
    for employee, category in high_performers.items():
        print(f"{employee}: {category}")

def add_volunteer():
    coordinator.add_volunteer()

def record_volunteer_activity():
    coordinator.record_activity()

def payroll():
    # Your payroll related logic goes here
    emp_id = int(input("Enter the employee ID for which you want to calculate payroll: "))

    # Construct the SQL query to retrieve employee details
    query = "SELECT emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions FROM employees WHERE emp_id = %s"
    mycursor.execute(query, (emp_id,))
    employee = mycursor.fetchone()

    if not employee:
        print("Employee with the provided ID does not exist.")
        return

    if len(employee) != 8:
        print("Unexpected data format retrieved from the database.")
        return
    
    # Extract relevant employee information
    emp_id, name, years_of_experience, age, qualification, salary, bonuses, deductions = employee

    # Calculate net pay
    net_pay = salary + bonuses - deductions
    print(f"Payroll for Employee {name} (ID: {emp_id}): ${net_pay}")

    # Update payroll column in the database
    update_query = "UPDATE employees SET payroll = %s WHERE emp_id = %s"
    mycursor.execute(update_query, (net_pay, emp_id))
    cmd.commit()
    

def record_attendance():
    print("\nRecord Attendance:")
    emp_id = int(input("Enter employee ID: "))
    if emp_id in evaluator.employees:
        # Employee exists, record attendance
        total_days = int(input("Enter total working days: "))
        present_days = int(input("Enter days present: "))
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days) * 100

        print(f"Attendance recorded for employee {evaluator.employees[emp_id].name}:")
        print(f"Total Days: {total_days}")
        print(f"Present Days: {present_days}")
        print(f"Absent Days: {absent_days}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")
    else:
        print("Employee not found.")
        
def show_employee_details():
    evaluator.show_employee_details()

menu_options = {
    1: add_employee,
    2: update_employee,
    3: delete_employee,
    4: performance_evaluation,
    5: add_volunteer,
    6: record_volunteer_activity,
    7: payroll,
    8: record_attendance,
    9: show_employee_details,  # Attendance recording option
    10: exit  # Exit option
}

if __name__ == "__main__":
    evaluator = PerformanceEvaluator()  
    coordinator = VolunteerCoordinator()
    logged_in = False
    print(f"default credentials(username:password) - {user_credentials}")
        
    while True:
        if not logged_in:
            print("\nLogin:")
            login_success = login()
            if not login_success:
                continue
            logged_in = True
        else:
            print("\nMenu:")
            print("1. Add Employee")
            print("2. Update Employee")
            print("3. Delete Employee")
            print("4. Performance Evaluation")
            print("5. Add Volunteer")
            print("6. Record Volunteer Activity")
            print("7. Payroll")
            print("8. Record Attendance")
            print("9. Show employee details")
            print("10. Exit")

            choice = int(input("Enter your choice: "))

            selected_function = menu_options.get(choice)
            if selected_function:
                if choice == 11:
                    break  # Exit the loop if the user chooses to exit
                else:
                    selected_function()
            else:
                print("Invalid choice. Please enter a valid option.")
