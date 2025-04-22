from collections import defaultdict
from task1.student import Student

class StudentManager:
    """Class to manage a list of students and perform queries."""
    
    def __init__(self):
        """Initialize an empty student list."""
        self.students = []

    def load_data(self, serializer, filename):
        """
        Load student data using the specified serializer.

        Args:
            serializer (Serializer): Serializer instance to use.
            filename (str): File to load from.
        """
        try:
            self.students = serializer.load(filename)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def save_data(self, serializer, filename):
        """
        Save student data using the specified serializer.

        Args:
            serializer (Serializer): Serializer instance to use.
            filename (str): File to save to.
        """
        try:
            serializer.save(self.students, filename)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def count_needing_dormitory(self):
        """Count students who need a dormitory."""
        return sum(1 for student in self.students if student.needs_dormitory)

    def get_students_with_experience_more_than(self, years):
        """
        Get students with work experience greater than specified years.

        Args:
            years (int): Minimum years of experience.

        Returns:
            list: List of matching Student objects.
        """
        return [student for student in self.students 
                if student.work_experience is not None and student.work_experience > years]

    def get_students_educated_from(self, education_type):
        """
        Get students who completed a specific type of education.

        Args:
            education_type (str): Type of education (e.g., 'техникум').

        Returns:
            list: List of matching Student objects.
        """
        return [student for student in self.students if student.education == education_type]

    def get_language_groups(self):
        """
        Group students by the language they studied.

        Returns:
            defaultdict: Dictionary mapping languages to lists of students.
        """
        groups = defaultdict(list)
        for student in self.students:
            groups[student.language].append(student)
        return groups

    def find_student_by_surname(self, surname):
        """
        Find a student by surname.

        Args:
            surname (str): Surname to search for.

        Returns:
            Student or None: Matching student or None if not found.
        """
        for student in self.students:
            if student.surname == surname:
                return student
        return None