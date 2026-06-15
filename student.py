import re

class Student:
    """
    Represents a student and handles validation of their information.
    """
    def __init__(self, student_id, name, age, gender, course, marks, email, description):
        # Validate ID
        if not str(student_id).strip():
            raise ValueError("Student ID cannot be empty.")
        self.student_id = str(student_id).strip()
        
        # Validate Name
        if not str(name).strip():
            raise ValueError("Name cannot be empty.")
        self.name = str(name).strip()
        
        # Validate Age
        try:
            self.age = int(age)
        except (ValueError, TypeError):
            raise ValueError("Age must be a valid integer.")
        if self.age <= 0:
            raise ValueError("Age must be greater than 0.")
            
        # Validate Gender
        if not str(gender).strip():
            raise ValueError("Gender cannot be empty.")
        self.gender = str(gender).strip()
        
        # Validate Course
        if not str(course).strip():
            raise ValueError("Course cannot be empty.")
        self.course = str(course).strip()
        
        # Validate Marks
        try:
            self.marks = float(marks)
        except (ValueError, TypeError):
            raise ValueError("Marks must be a valid number.")
        if not (0 <= self.marks <= 100):
            raise ValueError("Marks must be between 0 and 100 (inclusive).")
            
        # Validate Email
        self.email = str(email).strip()
        self.validate_email(self.email)

        # Validate Description
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Description cannot be empty.")
        if len(description.strip()) > 200:
            raise ValueError("Description must be 200 characters or less.")
        self.description = description.strip()

    @staticmethod
    def validate_email(email):
        """
        Validates email format using regex.
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email format: '{email}'")

    @property
    def grade(self):
        """
        Calculates letter grade based on marks.
        """
        if self.marks >= 90:
            return "A"
        elif self.marks >= 80:
            return "B"
        elif self.marks >= 70:
            return "C"
        elif self.marks >= 60:
            return "D"
        elif self.marks >= 50:
            return "E"
        else:
            return "F"

    @property
    def status(self):
        """
        Determines Pass/Fail status. Pass mark is 50.
        """
        return "Pass" if self.marks >= 50 else "Fail"

    def display(self):
        """
        Prints the student details in a visually clean layout to the console.
        """
        print(f"----------------------------------------")
        print(f"ID:          {self.student_id}")
        print(f"Name:        {self.name}")
        print(f"Age:         {self.age}")
        print(f"Gender:      {self.gender}")
        print(f"Course:      {self.course}")
        print(f"Marks:       {self.marks} ({self.grade} - {self.status})")
        print(f"Email:       {self.email}")
        print(f"Description: {self.description}")
        print(f"----------------------------------------")

    def to_dict(self):
        """
        Returns student attributes as a dictionary for easy JSON serialization.
        """
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "course": self.course,
            "marks": self.marks,
            "email": self.email,
            "description": self.description,
            "grade": self.grade,
            "status": self.status
        }
