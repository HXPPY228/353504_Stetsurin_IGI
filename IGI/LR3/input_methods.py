# input metods for task2
# Task2
# Stetsurin Elisey 353504
# 23.03.2025

import random

def generate_random_list(size):
    """
    Generates a list of random integers.
    
    Args:
        size (int): The number of elements to generate.
    
    Returns:
        list: A list of random integers between 1 and 30.
    
    Raises:
        ValueError: If size is not a positive integer.
    """
    if size <= 0:
        raise ValueError("Размер должен быть положительным целым числом")
    return [random.randint(1, 30) for _ in range(size)]

def user_input_list():
    """
    Collects a list of integers from user input until 0 is entered.
    
    The function prompts the user to enter integers one by one, stopping when 0 is entered.
    It handles invalid inputs by asking the user to enter a valid integer.
    
    Returns:
        list: A list of integers entered by the user, excluding the terminating 0.
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