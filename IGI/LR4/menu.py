import subprocess
import os

def run_task(task_name):
    """
    Run the specified task script using subprocess.
    
    Args:
        task_name (str): The name of the task, e.g., 'task1'
    """
    script_path = os.path.join(os.path.dirname(__file__), f"{task_name}.py")
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {task_name}.py: {e}")
    except FileNotFoundError:
        print(f"Script {task_name}.py not found.")

def main():
    """
    Main function to display the menu and handle user choices.
    """
    while True:
        print("\n=== Main Menu ===")
        print("1. Run Task 1")
        print("2. Run Task 2")
        print("3. Run Task 3")
        print("4. Run Task 4")
        print("5. Run Task 5")
        print("0. Exit")
        choice = input("Enter your choice (0-5): ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice in ["1", "2", "3", "4", "5"]:
            task_name = f"task{choice}"
            run_task(task_name)
        else:
            print("Invalid choice. Please enter a number between 0 and 5.")

if __name__ == "__main__":
    main()