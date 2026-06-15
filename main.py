import sys
from manager import StudentManager

def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)

def get_input(prompt, required=True):
    val = input(prompt).strip()
    if required and not val:
        print("Error: This field is required.")
        return get_input(prompt, required)
    return val

def display_student_table(students):
    if not students:
        print("No student records found.")
        return
    
    # Print formatted headers
    print(f"\n{'ID':<10} | {'Name':<18} | {'Age':<5} | {'Gender':<8} | {'Course':<12} | {'Marks':<6} | {'Grade':<5} | {'Status':<6} | {'Email':<22} | {'Description':<25}")
    print("-" * 144)
    for s in students:
        desc = (s.description[:22] + "...") if len(s.description) > 25 else s.description
        print(f"{s.student_id:<10} | {s.name:<18} | {s.age:<5} | {s.gender:<8} | {s.course:<12} | {s.marks:<6.1f} | {s.grade:<5} | {s.status:<6} | {s.email:<22} | {desc:<25}")
    print("-" * 144 + "\n")

def menu_add_student(manager):
    print_header("Add New Student")
    student_id = get_input("Enter Student ID: ")
    name = get_input("Enter Name: ")
    
    while True:
        try:
            age = int(get_input("Enter Age: "))
            break
        except ValueError:
            print("Error: Age must be a valid integer.")
            
    gender = get_input("Enter Gender: ")
    course = get_input("Enter Course: ")
    
    while True:
        try:
            marks = float(get_input("Enter Marks (0-100): "))
            break
        except ValueError:
            print("Error: Marks must be a valid number.")
            
    email = get_input("Enter Email: ")
    description = get_input("Enter Description (max 200 chars): ")

    try:
        manager.add_student(student_id, name, age, gender, course, marks, email, description)
        print("\nSuccess: Student added successfully!")
    except ValueError as e:
        print(f"\nError: {e}")

def menu_view_students(manager):
    print_header("All Students")
    display_student_table(manager.view_students())

def menu_search_student(manager):
    print_header("Search Student")
    student_id = get_input("Enter Student ID: ")
    student = manager.search_student(student_id)
    if student:
        student.display()
    else:
        print(f"Error: Student with ID '{student_id}' not found.")

def menu_update_student(manager):
    print_header("Update Student Details")
    student_id = get_input("Enter Student ID: ")
    student = manager.search_student(student_id)
    if not student:
        print(f"Error: Student with ID '{student_id}' not found.")
        return
    
    print("\nPress Enter to keep current values:")
    name = input(f"Name [{student.name}]: ").strip() or None
    
    age_input = input(f"Age [{student.age}]: ").strip()
    age = None
    if age_input:
        try:
            age = int(age_input)
        except ValueError:
            print("Error: Invalid input for Age. Update aborted.")
            return

    gender = input(f"Gender [{student.gender}]: ").strip() or None
    course = input(f"Course [{student.course}]: ").strip() or None
    
    marks_input = input(f"Marks [{student.marks}]: ").strip()
    marks = None
    if marks_input:
        try:
            marks = float(marks_input)
        except ValueError:
            print("Error: Invalid input for Marks. Update aborted.")
            return
            
    email = input(f"Email [{student.email}]: ").strip() or None
    description = input(f"Description [{student.description}]: ").strip() or None

    try:
        manager.update_student(
            student_id=student_id,
            name=name,
            age=age,
            gender=gender,
            course=course,
            marks=marks,
            email=email,
            description=description
        )
        print("\nSuccess: Student details updated successfully!")
    except ValueError as e:
        print(f"\nError: {e}")

def menu_delete_student(manager):
    print_header("Delete Student")
    student_id = get_input("Enter Student ID: ")
    try:
        manager.delete_student(student_id)
        print("\nSuccess: Student deleted successfully!")
    except ValueError as e:
        print(f"\nError: {e}")

def menu_sort_by_name(manager):
    print_header("Students Sorted by Name")
    sorted_students = manager.get_sorted_by_name()
    display_student_table(sorted_students)

def menu_sort_by_marks(manager):
    print_header("Students Sorted by Marks (High to Low)")
    sorted_students = manager.get_sorted_by_marks()
    display_student_table(sorted_students)

def main():
    manager = StudentManager()
    
    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort by Name")
        print("7. Sort by Marks")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            menu_add_student(manager)
        elif choice == '2':
            menu_view_students(manager)
        elif choice == '3':
            menu_search_student(manager)
        elif choice == '4':
            menu_update_student(manager)
        elif choice == '5':
            menu_delete_student(manager)
        elif choice == '6':
            menu_sort_by_name(manager)
        elif choice == '7':
            menu_sort_by_marks(manager)
        elif choice == '8':
            print("\nExiting. Thank you for using the Student Management System!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select from options 1-8.")

if __name__ == "__main__":
    main()
