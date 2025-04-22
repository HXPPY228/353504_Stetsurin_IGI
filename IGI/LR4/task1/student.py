class Student:
    """Class representing a student with personal and educational details."""
    
    # Static attribute to track total number of students
    total_students = 0

    def __init__(self, surname, needs_dormitory, work_experience, education, language):
        """
        Initialize a Student instance.

        Args:
            surname (str): Student's surname.
            needs_dormitory (str or bool): Whether the student needs a dormitory.
            work_experience (str or int or None): Years of work experience.
            education (str): Type of education completed (e.g., 'техникум').
            language (str): Language studied by the student.
        """
        self._surname = surname
        # Convert string to boolean if loaded from CSV
        self._needs_dormitory = needs_dormitory == "True" if isinstance(needs_dormitory, str) else needs_dormitory
        # Convert work experience to int or None
        self._work_experience = None if work_experience == "None" or work_experience is None else int(work_experience)
        self._education = education
        self._language = language
        Student.total_students += 1

    # Property for surname with getter and setter
    @property
    def surname(self):
        """Get the student's surname."""
        return self._surname

    @surname.setter
    def surname(self, value):
        """Set the student's surname with validation."""
        if not isinstance(value, str) or not value:
            raise ValueError("Surname must be a non-empty string")
        self._surname = value

    # Property for needs_dormitory
    @property
    def needs_dormitory(self):
        """Get whether the student needs a dormitory."""
        return self._needs_dormitory

    @property
    def work_experience(self):
        """Get the student's work experience."""
        return self._work_experience

    @property
    def education(self):
        """Get the student's education type."""
        return self._education

    @property
    def language(self):
        """Get the language studied by the student."""
        return self._language

    def __str__(self):
        """Return a string representation of the student."""
        return (f"{self.surname}, needs dormitory: {self.needs_dormitory}, "
                f"experience: {self.work_experience}, education: {self.education}, "
                f"language: {self.language}")

    def __repr__(self):
        """Return a detailed string representation for debugging."""
        return f"Student('{self.surname}', {self.needs_dormitory}, {self.work_experience}, '{self.education}', '{self.language}')"