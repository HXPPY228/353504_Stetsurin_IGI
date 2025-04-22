import csv
import pickle
from task1.student import Student

class Serializer:
    """Abstract base class for serializers."""
    
    def save(self, students, filename):
        """Save students to a file."""
        raise NotImplementedError("Subclasses must implement save()")

    def load(self, filename):
        """Load students from a file."""
        raise NotImplementedError("Subclasses must implement load()")

class CSVSerializer(Serializer):
    """Serializer for CSV format."""
    
    def save(self, students, filename):
        """
        Save student list to a CSV file.

        Args:
            students (list): List of Student objects.
            filename (str): Name of the file to save to.
        """
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["surname", "needs_dormitory", "work_experience", "education", "language"])
            for student in students:
                writer.writerow([
                    student.surname,
                    student.needs_dormitory,
                    student.work_experience if student.work_experience is not None else "None",
                    student.education,
                    student.language
                ])

    def load(self, filename):
        """
        Load student list from a CSV file.

        Args:
            filename (str): Name of the file to load from.

        Returns:
            list: List of Student objects.
        """
        students = []
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                student = Student(row[0], row[1], row[2], row[3], row[4])
                students.append(student)
        return students

class PickleSerializer(Serializer):
    """Serializer for pickle format."""
    
    def save(self, students, filename):
        """
        Save student list to a pickle file.

        Args:
            students (list): List of Student objects.
            filename (str): Name of the file to save to.
        """
        with open(filename, 'wb') as file:
            pickle.dump(students, file)

    def load(self, filename):
        """
        Load student list from a pickle file.

        Args:
            filename (str): Name of the file to load from.

        Returns:
            list: List of Student objects.
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)