import os
import json
from student import Student

class StudentManager:
    """
    Manages collection of students, performing CRUD, persistence, and sorting.
    """
    def __init__(self, filepath=None):
        if filepath is None:
            # Default directory structure relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "data")
            self.filepath = os.path.join(data_dir, "students.json")
        else:
            self.filepath = filepath
            
        self.students = {}
        self.load_data()

    def load_data(self):
        """
        Loads students from JSON file, instantiating Student objects.
        """
        self.students = {}
        if not os.path.exists(self.filepath):
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            # Create an empty list in json
            self.save_data()
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # data is expected to be a list of student dicts
                for s_dict in data:
                    try:
                        student = Student(
                            student_id=s_dict["student_id"],
                            name=s_dict["name"],
                            age=s_dict["age"],
                            gender=s_dict["gender"],
                            course=s_dict["course"],
                            marks=s_dict["marks"],
                            email=s_dict["email"],
                            description=s_dict.get("description", "No description provided.")
                        )
                        self.students[student.student_id] = student
                    except (ValueError, KeyError) as e:
                        # Print error or log, but skip invalid entries
                        print(f"Skipping invalid student record: {s_dict}. Error: {e}")
        except json.JSONDecodeError:
            # File might be empty or corrupted, start fresh
            self.save_data()

    def save_data(self):
        """
        Saves student collection back to JSON file.
        """
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        # Convert dictionary values to lists of dicts
        data = [student.to_dict() for student in self.students.values()]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_student(self, student_id, name, age, gender, course, marks, email, description):
        """
        Creates and adds a new Student instance to collection.
        Raises ValueError if ID already exists or inputs fail validation.
        """
        s_id_str = str(student_id).strip()
        if s_id_str in self.students:
            raise ValueError(f"Student ID '{s_id_str}' already exists.")

        # Instantiate (will validate fields inside Student constructor)
        new_student = Student(s_id_str, name, age, gender, course, marks, email, description)
        self.students[s_id_str] = new_student
        self.save_data()
        return new_student

    def view_students(self):
        """
        Returns a list of all Student objects.
        """
        return list(self.students.values())

    def search_student(self, student_id):
        """
        Searches student by ID. Returns Student object or None.
        """
        return self.students.get(str(student_id).strip())

    def update_student(self, student_id, name=None, age=None, gender=None, course=None, marks=None, email=None, description=None):
        """
        Updates fields of an existing student. Validation is rerun.
        Returns the updated Student object.
        """
        s_id_str = str(student_id).strip()
        student = self.students.get(s_id_str)
        if not student:
            raise ValueError(f"Student with ID '{s_id_str}' not found.")

        # Gather updated parameters or retain existing ones
        temp_name = student.name if name is None or name == "" else str(name).strip()
        
        try:
            temp_age = student.age if age is None or age == "" else int(age)
        except (ValueError, TypeError):
            raise ValueError("Age must be a valid integer.")
            
        temp_gender = student.gender if gender is None or gender == "" else str(gender).strip()
        temp_course = student.course if course is None or course == "" else str(course).strip()
        
        try:
            temp_marks = student.marks if marks is None or marks == "" else float(marks)
        except (ValueError, TypeError):
            raise ValueError("Marks must be a valid number.")
            
        temp_email = student.email if email is None or email == "" else str(email).strip()
        temp_description = student.description if description is None or description == "" else str(description).strip()

        # Validate by constructing a temporary Student object to ensure compatibility
        validated_temp = Student(s_id_str, temp_name, temp_age, temp_gender, temp_course, temp_marks, temp_email, temp_description)

        # Update actual student properties if valid
        student.name = validated_temp.name
        student.age = validated_temp.age
        student.gender = validated_temp.gender
        student.course = validated_temp.course
        student.marks = validated_temp.marks
        student.email = validated_temp.email
        student.description = validated_temp.description

        self.save_data()
        return student

    def delete_student(self, student_id):
        """
        Deletes a student from database by ID.
        Raises ValueError if student does not exist.
        """
        s_id_str = str(student_id).strip()
        if s_id_str not in self.students:
            raise ValueError(f"Student with ID '{s_id_str}' not found.")
        
        del self.students[s_id_str]
        self.save_data()

    def get_sorted_by_name(self, reverse=False):
        """
        Returns list of Student objects sorted by name alphabetically.
        """
        return sorted(self.students.values(), key=lambda s: s.name.lower(), reverse=reverse)

    def get_sorted_by_marks(self, reverse=True):
        """
        Returns list of Student objects sorted by marks. Default is high-to-low (reverse=True).
        """
        return sorted(self.students.values(), key=lambda s: s.marks, reverse=reverse)
