#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

struct Student {
    string id;
    string name;
    int age;
    string gender;
    string phone_number;
    vector<int> marks;
    string message;
};
void printStudent(const Student& student) {
    cout << "ID: " << student.id << endl;
    cout << "Name: " << student.name << endl;
    cout << "Age: " << student.age << endl;
    cout << "Gender: " << student.gender << endl;
    cout << "Phone Number: " << student.phone_number << endl;
    cout << endl;
}
void addStudentBio(vector<Student>& students) {
    Student student;
    cout << "Enter student ID: ";
    cin >> student.id;
    cout << "Enter student name: ";
    cin >> student.name;
    cout << "Enter student age: ";
    cin >> student.age;
    cout << "Enter student gender: ";
    cin >> student.gender;

    // loop until a valid phone number is entered


while (true) {
    cout << "Enter parent phone number: ";
    string phone_str;
    cin >> phone_str;
    if (phone_str.length() != 10 || !std::all_of(phone_str.begin(), phone_str.end(), ::isdigit)) {
        cout << "Invalid phone number. Please enter a 10-digit number." << endl;
    } else {
        student.phone_number = phone_str;
        break;
    }
}
    students.push_back(student);
}


void addStudentMarks(vector<Student>& students) {
    string id;
    cout << "Enter student ID: ";
    cin >> id;
    for (auto& student : students) {
        if (student.id == id) {
            cout << "Enter marks for Tamil: ";
            int mark;
            cin >> mark;
            student.marks.push_back(mark);
            cout << "Enter marks for English: ";
            cin >> mark;
            student.marks.push_back(mark);
            cout << "Enter marks for Maths: ";
            cin >> mark;
            student.marks.push_back(mark);
            cout << "Enter marks for Science: ";
            cin >> mark;
            student.marks.push_back(mark);
            cout << "Enter marks for History: ";
            cin >> mark;
            student.marks.push_back(mark);
            cout << "Marks added for student with ID " << id << endl << endl;
            return;
        }
    }
    cout << "Student not found." << endl << endl;
}

void deleteStudentBiodata(vector<Student>& students) {
    string id;
    cout << "Enter student ID: ";
    cin >> id;
    for (auto it = students.begin(); it != students.end(); ++it) {
        if (it->id == id) {
            cout << "Deleting student with ID " << it->id << endl;
            students.erase(it);
            return;
        }
    }
    cout << "Student not found." << endl;
}

void deleteStudentMarks(vector<Student>& students) {
    string id;
    cout << "Enter student ID: ";
    cin >> id;
    for (auto& student : students) {
        if (student.id == id) {
            student.marks.clear();
            cout << "Marks deleted for student with ID " << id << endl;
            return;
        }
    }
    cout << "Student not found." << endl;
}

void displayAllStudents(const vector<Student>& students) {
    for (const auto& student : students) {
        printStudent(student);
    }
}

void displayStudentBiodata(const vector<Student>& students) {
    string id;
    cout << "Enter student ID: ";
    cin >> id;
    for (const auto& student : students) {
        if (student.id == id) {
            printStudent(student);
            return;
        }
    }
    cout << "Student not found." << endl;
}

void displayStudentResults(const vector<Student>& students) {
    string id;
    cout << "Enter student ID: ";
    cin >> id;
    for (const auto& student : students) {
        if (student.id == id) {
            int total = 0;
            for (int mark : student.marks) {
                total += mark;
            }
            double average = static_cast<double>(total) / student.marks.size();
            double percentage = (static_cast<double>(total) / (student.marks.size() * 100)) * 100;
            bool pass = true;
            for (int mark : student.marks) {
                if (mark < 35) {
                    pass = false;
                    break;
                }
            }
            cout << "Marks for " << student.name << endl;
            cout << "+--------------+-------+--------+" << endl;
            cout << "| Subject      | Marks | Remarks|" << endl;
            cout << "+--------------+-------+--------+" << endl;
            cout << "| Tamil        | " << student.marks[0] << "    | " << (student.marks[0] >= 35 ? "Pass" : "Fail") << "   |" << endl;
            cout << "| English      | " << student.marks[1] << "    | " << (student.marks[1] >= 35 ? "Pass" : "Fail") << "   |" << endl;
            cout << "| Maths        | " << student.marks[2] << "    | " << (student.marks[2] >= 35 ? "Pass" : "Fail") << "   |" << endl;
            cout << "| Science      | " << student.marks[3] << "    | " << (student.marks[3] >= 35 ? "Pass" : "Fail") << "   |" << endl;
            cout << "| History      | " << student.marks[4] << "    | " << (student.marks[4] >= 35 ? "Pass" : "Fail") << "   |" << endl;
            cout << "+--------------+-------+--------+"<< endl;
            cout<<  "|Total Marks   | " << total<<"   |"<< endl;
            cout << "+--------------+-------+---------|"<< endl;
            cout << "Result: " << (pass ? "Pass" : "Fail") << endl;
            cout << "+--------------+-------+---------|"<< endl;
            cout << "Average Marks: " << average << endl;
            cout << "Percentage: " << percentage << "%" << endl;
            cout << endl;
            return;
        }
    }
    cout << "Student not found." << endl;
}

void sendStudentResults(const vector<Student>& students) {
    string id;
    cout << "Enter student ID: ";
    cin >> id;

    for (const auto& student : students) {
        if (student.id == id) {
            int total = 0;
            for (int mark : student.marks) {
                total += mark;
            }
            double average = static_cast<double>(total) / student.marks.size();
            double percentage = (static_cast<double>(total) / (student.marks.size() * 100)) * 100;
            bool pass = true;
            for (int mark : student.marks) {
                if (mark < 35) {
                    pass = false;
                    break;
                }
            }
            string message = "";  // declare the message variable here
            message += " Tamil         " + to_string(student.marks[0]) + "\n";
            message += " English       " + to_string(student.marks[1]) + "\n";
            message += " Mathematics   " + to_string(student.marks[2]) + "\n";
            message += " Science       " + to_string(student.marks[3]) + "\n";
            message += " Social        " + to_string(student.marks[4]) + "\n";
            message += "Total marks: " + to_string(total) + "\n";
            message += "Average marks: " + to_string(average) + "\n";
            message += "Percentage: " + to_string(percentage) + "%\n";

          //  message += "Result: " + (pass ? "Pass" : "Fail") + "\n";
string result = (pass ? "Pass" : "Fail");
message += "Result: " + result + "\n";
            message += "Thank you.";

            cout << "Sending SMS to " << student.phone_number << endl;
            cout << "Dear parent, your child " << student.name << " has scored "
            << percentage << "% in the exams. Result: " << (pass ? "Pass" : "Fail")
            << endl << message << endl;
            return;
        }
    }
    cout << "Student not found." << endl;
}

int main() {
    vector<Student> students;

    while (true) {
        cout << "Menu:" << endl;
        cout << "1. Add student biodata" << endl;
        cout << "2. Add student marks" << endl;
        cout << "3. Display student biodata" << endl;
        cout << "4. Display student results" << endl;
        cout << "5. Display all students" << endl;
        cout << "6. Send SMS results" << endl;
        cout << "7. Delete student biodata" << endl;
        cout << "8. Delete student marks" << endl;
        cout << "9. Quit" << endl;
        int choice;
        cout << "Enter your choice: ";
        cin >> choice;
        switch (choice) {
        case 1:
            addStudentBio(students);
            break;
        case 2:
            addStudentMarks(students);
            break;
        case 3:
            displayStudentBiodata(students);
            break;
        case 4:
            displayStudentResults(students);
            break;
        case 5:
            displayAllStudents(students);
            break;
        case 6:
            sendStudentResults(students);
            break;
        case 7:
            deleteStudentBiodata(students);
            break;
        case 8:
            deleteStudentMarks(students);
            break;
        case 9:
             return 0;

        default:
            cout << "Invalid choice. Please try again." << endl;
        }
    }

    return 0;
}
