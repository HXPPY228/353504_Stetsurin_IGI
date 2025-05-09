# main for task5
# Task5 24
# Stetsurin Elisey 353504
# 23.03.2025

from list_processing import input_list, generate_random_list, find_product_of_negatives, find_sum_before_max_abs, print_list

def run_task5():
    """
    Executes Task 5: Processes a list of numbers for specific calculations.

    This function:
    - Allows the user to input a list manually or generate a random list.
    - Calculates the product of all negative numbers.
    - Calculates the sum of positive numbers before the element with the maximum absolute value.
    - Displays the list and results.
    - Repeats until the user chooses to stop, then returns to the menu.

    Returns:
        None
    
    Notes:
        - Handles invalid input with error messages.
        - Depends on external functions: input_list, generate_random_list, find_product_of_negatives, 
          find_sum_before_max_abs, print_list.
    """
    print("Добро пожаловать в программу обработки списка!")
    print("Вы можете ввести список вручную или сгенерировать его случайным образом.")
    while True:
        try:
            choice = input("\nВыберите способ заполнения (1 - вручную, 2 - случайно): ").strip()
            if choice == '1':
                numbers = input_list()
            elif choice == '2':
                size = int(input("Введите количество элементов в списке: "))
                numbers = generate_random_list(size)
            else:
                print("Неверный выбор. Выберите 1 или 2.")
                continue
            print_list(numbers)
            product_neg = find_product_of_negatives(numbers)
            sum_pos = find_sum_before_max_abs(numbers)
            print(f"Произведение отрицательных элементов: {product_neg}")
            print(f"Сумма положительных до максимального по модулю: {sum_pos}")
        except ValueError as ve:
            print(f"Ошибка ввода: {ve}")
        except Exception as e:
            print(f"Ошибка: {e}")
        again = input("\nХотите обработать ещё один список? (да/нет): ").strip().lower()
        if again != 'да':
            print("До свидания!")
            return