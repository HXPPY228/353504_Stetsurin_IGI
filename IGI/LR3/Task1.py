# main Task1
# Task1
# Stetsurin Elisey 353504
# 23.03.2025
 
import math
from ln_approx import ln_approx

def run_task1():
    """
    Executes Task 1: Computes ln(1 - x) using series approximation.

    This function:
    - Prompts the user for x (|x| < 1) and precision (eps).
    - Computes ln(1 - x) using a series approximation (via ln_approx).
    - Compares the result with the exact value from math.log.
    - Displays results in a formatted table.
    - Repeats until the user chooses to stop, then returns to the menu.

    Returns:
        None
    
    Notes:
        - Handles invalid input with error messages.
        - Requires the ln_approx function and math module.
    """
    print("Добро пожаловать в программу вычисления ln(1 - x) с помощью ряда!")
    while True:
        try:
            x = float(input("Введите x (|x| < 1): "))
            eps = float(input("Введите eps (точность): "))
            approx, n_terms = ln_approx(x, eps)
            if approx is not None:
                math_value = math.log(1 - x)
                print(f"{'x':<10} {'n':<5} {'F(x)':<15} {'Math F(x)':<15} {'eps':<10}")
                print("-" * 56)
                print(f"{x:<10.5f} {n_terms:<5} {approx:<15.10f} {math_value:<15.10f} {eps:<10.5f}")
        except ValueError:
            print("Ошибка: введите корректные числовые значения")
        again = input("\nАнализировать еще раз? (да/нет): ").strip().lower()
        if again != 'да':
            print("До свидания!")
            return 