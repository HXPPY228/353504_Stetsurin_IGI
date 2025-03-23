# count and decorator for task2
# Task2
# Stetsurin Elisey 353504
# 23.03.2025

def log_decorator(func):
    """Декоратор для логирования вызовов функции и результатов."""
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами: {args}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула: {result}")
        return result
    return wrapper

@log_decorator
def count_in_range(numbers, min_val=5, max_val=25):
    """
    Подсчитывает количество чисел в заданном диапазоне.
    """
    count = 0
    for num in numbers:
        if min_val <= num <= max_val:
            count += 1
    return count