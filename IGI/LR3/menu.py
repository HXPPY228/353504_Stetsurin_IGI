from Task1 import run_task1
from Task2 import run_task2
from Task3 import run_task3
from Task4 import run_task4
from Task5 import run_task5

def main():
    """
    Displays the main menu and handles task selection.

    This function:
    - Presents a menu with options for Tasks 1-5 or exit (0).
    - Calls the corresponding task function based on user input.
    - Loops until the user chooses to exit.

    Returns:
        None
    
    Notes:
        - Invalid choices prompt an error message and re-display the menu.
    """
    while True:
        print("\nМеню выбора заданий:")
        print("1. Задание 1: Вычисление ln(1 - x)")
        print("2. Задание 2: Подсчет чисел в диапазоне")
        print("3. Задание 3: Анализ текста (пробелы и апострофы)")
        print("4. Задание 4: Анализ текста (слова)")
        print("5. Задание 5: Обработка списка чисел")
        print("0. Выход")
        #print(run_task1.__doc__)
        choice = input("Выберите задание (0-5): ").strip()
        
        if choice == '1':
            run_task1()
        elif choice == '2':
            run_task2()
        elif choice == '3':
            run_task3()
        elif choice == '4':
            run_task4()
        elif choice == '5':
            run_task5()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

if __name__ == "__main__":
    main()