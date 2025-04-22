from task1.StudentManager import StudentManager
from task1.serializer import CSVSerializer, PickleSerializer

def display_menu():
    """Display the main menu options."""
    print("\n=== Student Data Management System ===")
    print("1. Load data from CSV")
    print("2. Load data from pickle")
    print("3. Save data to CSV")
    print("4. Save data to pickle")
    print("5. Count students needing dormitory")
    print("6. Get students with experience > 2 years")
    print("7. Get students educated from 'техникум'")
    print("8. Get language groups")
    print("9. Find student by surname")
    print("0. Exit")

def main():
    """Main function to run the program."""
    manager = StudentManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (0-9): ").strip()
        
        try:
            if choice == "0":
                print("Goodbye!")
                break
                
            elif choice == "1":
                filename = input("Enter CSV filename: ").strip()
                if not filename:
                    raise ValueError("Filename cannot be empty")
                serializer = CSVSerializer()
                manager.load_data(serializer, filename)
                
            elif choice == "2":
                filename = input("Enter pickle filename: ").strip()
                if not filename:
                    raise ValueError("Filename cannot be empty")
                serializer = PickleSerializer()
                manager.load_data(serializer, filename)
                
            elif choice == "3":
                filename = input("Enter CSV filename: ").strip()
                if not filename:
                    raise ValueError("Filename cannot be empty")
                serializer = CSVSerializer()
                manager.save_data(serializer, filename)
                
            elif choice == "4":
                filename = input("Enter pickle filename: ").strip()
                if not filename:
                    raise ValueError("Filename cannot be empty")
                serializer = PickleSerializer()
                manager.save_data(serializer, filename)
                
            elif choice == "5":
                count = manager.count_needing_dormitory()
                print(f"Number of students needing dormitory: {count}")
                
            elif choice == "6":
                students = manager.get_students_with_experience_more_than(2)
                print("Students with experience > 2 years:")
                for student in students:
                    print(student)
                    
            elif choice == "7":
                students = manager.get_students_educated_from("техникум")
                print("Students who graduated from 'техникум':")
                for student in students:
                    print(student)
                    
            elif choice == "8":
                groups = manager.get_language_groups()
                print("Language groups:")
                for language, students in groups.items():
                    print(f"\n{language}:")
                    for student in students:
                        print(f"  {student}")
                        
            elif choice == "9":
                surname = input("Enter student surname: ").strip()
                if not surname:
                    raise ValueError("Surname cannot be empty")
                student = manager.find_student_by_surname(surname)
                if student:
                    print(f"Found student: {student}")
                else:
                    print(f"No student found with surname '{surname}'")
                    
            else:
                print("Invalid choice. Please enter a number between 0 and 9.")
                
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()