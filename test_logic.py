import unittest
import os
import tempfile
import json
from student import Student
from manager import StudentManager

class TestStudentManagementSystem(unittest.TestCase):
    def setUp(self):
        # Create a temporary JSON file to avoid polluting workspace data during testing
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.temp_filepath = self.temp_file.name
        self.temp_file.close()
        
        # Initialize an empty database
        with open(self.temp_filepath, "w", encoding="utf-8") as f:
            json.dump([], f)
            
        self.manager = StudentManager(filepath=self.temp_filepath)

    def tearDown(self):
        # Remove temporary file
        if os.path.exists(self.temp_filepath):
            os.remove(self.temp_filepath)

    def test_valid_student_creation(self):
        s = Student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", "Excellent CS student.")
        self.assertEqual(s.student_id, "STD01")
        self.assertEqual(s.name, "Alice")
        self.assertEqual(s.age, 20)
        self.assertEqual(s.gender, "Female")
        self.assertEqual(s.course, "CS")
        self.assertEqual(s.marks, 90.5)
        self.assertEqual(s.email, "alice@example.com")
        self.assertEqual(s.description, "Excellent CS student.")
        self.assertEqual(s.grade, "A")
        self.assertEqual(s.status, "Pass")

    def test_student_grade_ranges(self):
        # A: >= 90
        self.assertEqual(Student("S1", "N", 20, "M", "C", 90.0, "e@e.com", "Desc").grade, "A")
        # B: 80 - 89
        self.assertEqual(Student("S2", "N", 20, "M", "C", 85.0, "e@e.com", "Desc").grade, "B")
        # C: 70 - 79
        self.assertEqual(Student("S3", "N", 20, "M", "C", 75.0, "e@e.com", "Desc").grade, "C")
        # D: 60 - 69
        self.assertEqual(Student("S4", "N", 20, "M", "C", 65.0, "e@e.com", "Desc").grade, "D")
        # E: 50 - 59
        self.assertEqual(Student("S5", "N", 20, "M", "C", 55.0, "e@e.com", "Desc").grade, "E")
        self.assertEqual(Student("S5", "N", 20, "M", "C", 55.0, "e@e.com", "Desc").status, "Pass")
        # F: < 50
        self.assertEqual(Student("S6", "N", 20, "M", "C", 45.0, "e@e.com", "Desc").grade, "F")
        self.assertEqual(Student("S6", "N", 20, "M", "C", 45.0, "e@e.com", "Desc").status, "Fail")

    def test_invalid_email_validation(self):
        invalid_emails = [
            "plainaddress",
            "#@%^%#$@#$@#.com",
            "@example.com",
            "Joe Smith <email@example.com>",
            "email.example.com",
            "email@example@example.com",
            "email@example"
        ]
        for email in invalid_emails:
            with self.assertRaises(ValueError):
                Student("STD01", "Alice", 20, "Female", "CS", 90.5, email, "Desc")

    def test_invalid_age_validation(self):
        invalid_ages = [0, -5, -99]
        for age in invalid_ages:
            with self.assertRaises(ValueError):
                Student("STD01", "Alice", age, "Female", "CS", 90.5, "alice@example.com", "Desc")

    def test_invalid_marks_validation(self):
        invalid_marks = [-1, 100.1, -0.5, 120]
        for marks in invalid_marks:
            with self.assertRaises(ValueError):
                Student("STD01", "Alice", 20, "Female", "CS", marks, "alice@example.com", "Desc")

    def test_invalid_description_validation(self):
        # Empty description
        with self.assertRaises(ValueError):
            Student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", " ")
        
        # Over-length description (> 200 chars)
        long_desc = "a" * 201
        with self.assertRaises(ValueError):
            Student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", long_desc)

    def test_add_student(self):
        # Check standard addition
        s = self.manager.add_student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", "Desc")
        self.assertEqual(len(self.manager.view_students()), 1)
        self.assertEqual(self.manager.search_student("STD01").name, "Alice")
        self.assertEqual(self.manager.search_student("STD01").description, "Desc")

    def test_add_duplicate_student_id(self):
        self.manager.add_student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", "Desc")
        with self.assertRaises(ValueError):
            self.manager.add_student("STD01", "Bob", 22, "Male", "Math", 85.0, "bob@example.com", "Desc2")

    def test_search_student_not_found(self):
        self.assertIsNone(self.manager.search_student("NONEXISTENT"))

    def test_update_student(self):
        self.manager.add_student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", "Desc")
        
        # Partial update
        self.manager.update_student("STD01", name="Alice Smith", marks=95.0, description="New Description")
        updated = self.manager.search_student("STD01")
        self.assertEqual(updated.name, "Alice Smith")
        self.assertEqual(updated.marks, 95.0)
        self.assertEqual(updated.description, "New Description")
        self.assertEqual(updated.age, 20) # Keep age
        
        # Test update validation
        with self.assertRaises(ValueError):
            self.manager.update_student("STD01", email="invalid-email")

    def test_delete_student(self):
        self.manager.add_student("STD01", "Alice", 20, "Female", "CS", 90.5, "alice@example.com", "Desc")
        self.manager.delete_student("STD01")
        self.assertEqual(len(self.manager.view_students()), 0)
        
        # Delete non-existent
        with self.assertRaises(ValueError):
            self.manager.delete_student("STD01")

    def test_sorting(self):
        self.manager.add_student("STD01", "Charlie", 20, "Male", "CS", 80.0, "charlie@example.com", "Desc C")
        self.manager.add_student("STD02", "Alice", 22, "Female", "Math", 95.5, "alice@example.com", "Desc A")
        self.manager.add_student("STD03", "Bob", 21, "Male", "CS", 60.0, "bob@example.com", "Desc B")

        # Sort by Name ascending
        sorted_name = self.manager.get_sorted_by_name()
        self.assertEqual(sorted_name[0].name, "Alice")
        self.assertEqual(sorted_name[1].name, "Bob")
        self.assertEqual(sorted_name[2].name, "Charlie")

        # Sort by Marks descending
        sorted_marks = self.manager.get_sorted_by_marks()
        self.assertEqual(sorted_marks[0].name, "Alice")     # 95.5
        self.assertEqual(sorted_marks[1].name, "Charlie")   # 80.0
        self.assertEqual(sorted_marks[2].name, "Bob")       # 60.0

if __name__ == "__main__":
    unittest.main()
