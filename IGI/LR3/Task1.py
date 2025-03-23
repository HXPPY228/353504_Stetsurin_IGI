# main Task1
# Task1
# Stetsurin Elisey 353504
# 23.03.2025
 
import math

from ln_approx import ln_approx

print("Добро пожаловать в программу вычисления ln(1 - x) с помощью ряда!")

while True:
    try:
    # Get user inputs
        x = float(input("Введите x (|x| < 1): "))
        eps = float(input("Введите eps (точность): "))
    
    # Compute series approximation
        approx, n_terms = ln_approx(x, eps)
    
    # If computation was successful, display results
        if approx is not None:
            math_value = math.log(1 - x)
        
        # Print table header
            print(f"{'x':<10} {'n':<5} {'F(x)':<15} {'Math F(x)':<15} {'eps':<10}")
            print("-" * 56)
        # Print table row
            print(f"{x:<10.5f} {n_terms:<5} {approx:<15.10f} {math_value:<15.10f} {eps:<10.5f}")

    except ValueError:
        print("Ошибка: введите корректные числовые значения")

    again = input("\nАнализировать еще раз? (да/нет): ").strip().lower()
    if again != 'да':
        print("До свидания!")
        break