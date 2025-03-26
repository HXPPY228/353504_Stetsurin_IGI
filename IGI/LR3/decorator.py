#  decorator for tasks
# Tasks
# Stetsurin Elisey 353504
# 23.03.2025

from datetime import datetime

def log_decorator(func):
    """
    A decorator that logs function calls and their results.
    
    This decorator prints the function name and arguments before calling the function,
    and prints the return value after the function call.
    
    Args:
        func (function): The function to be decorated.
    
    Returns:
        function: The wrapped function with logging.
    """
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print(f"Вызов функции {func.__name__} в {start_time} с аргументами: {args}")
        
        result = func(*args, **kwargs)
        
        end_time = datetime.now()
        print(f"Функция {func.__name__} завершила выполнение в {end_time}, вернула: {result}")
        
        execution_time = end_time - start_time
        print(f"Время выполнения функции: {execution_time.total_seconds()} секунд")
        
        return result
    return wrapper