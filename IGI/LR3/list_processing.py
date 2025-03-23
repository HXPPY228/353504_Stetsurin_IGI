# list logic for task5
# Task5
# Stetsurin Elisey 353504
# 23.03.2025

import random

def input_list():
    """
    Ввод списка вещественных чисел пользователем.
    """
    while True:
        try:
            input_str = input("Введите элементы списка через пробел: ")
            numbers = [float(num) for num in input_str.split()]
            if not numbers:
                print("Список не может быть пустым. Попробуйте снова.")
                continue
            return numbers
        except ValueError:
            print("Ошибка: Введите только вещественные числа, разделённые пробелами.")

def generate_random_list(size, min_val=-10.0, max_val=10.0):
    """
    Генерирует список случайных вещественных чисел.
    """
    return [random.uniform(min_val, max_val) for _ in range(size)]

def find_product_of_negatives(numbers):
    """
    Находит произведение всех отрицательных элементов списка.
    """
    product = 1
    for num in numbers:
        if num < 0:
            product *= num
    return product

def find_sum_before_max_abs(numbers):
    """
    Находит сумму всех положительных элементов до максимального по модулю элемента.
    """
    if not numbers:
        return 0
    
    # Находим индекс элемента с максимальным модулем
    max_abs_index = max(range(len(numbers)), key=lambda i: abs(numbers[i]))
    
    # Суммируем положительные элементы до этого индекса
    sum_positive = sum(num for num in numbers[:max_abs_index] if num > 0)
    return sum_positive

def print_list(numbers):
    """
    Выводит список на экран.
    """
    print("Список:", numbers)