# count for task3
# Task3
# Stetsurin Elisey 353504
# 23.03.2025

from count_calculator import log_decorator

@log_decorator
def count_whitespace_and_apostrophes(text):
    """
    Подсчитывает количество пробельных символов и апострофов в тексте.
    """
    whitespace_count = 0
    apostrophe_count = 0
    
    for char in text:
        if char.isspace():  # check if space
            whitespace_count += 1
        elif char == "'":  # check if '
            apostrophe_count += 1
    
    return whitespace_count, apostrophe_count