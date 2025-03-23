# input metods for task2
# Task2
# Stetsurin Elisey 353504
# 23.03.2025

import random

def generate_random_list(size):
    """
    Генерирует список случайных целых чисел.
    """
    if size <= 0:
        raise ValueError("Размер должен быть положительным целым числом")
    return [random.randint(1, 30) for _ in range(size)]

def user_input_list():
    """
    Собирает список целых чисел от пользователя до ввода 0.
    """
    numbers = []
    print("Введите целые числа (0 для завершения):")
    while True:
        try:
            num = int(input("> "))
            if num == 0:
                break
            numbers.append(num)
        except ValueError:
            print("Пожалуйста, введите корректное целое число.")
    return numbers