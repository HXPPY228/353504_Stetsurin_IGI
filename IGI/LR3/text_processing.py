# logic for task4
# Task4
# Stetsurin Elisey 353504
# 23.03.2025

from count_calculator import log_decorator

@log_decorator
def split_text(text):
    """
    Разделяет текст на слова по пробелам и запятым.
    """
    # Заменяем запятые на пробелы и разбиваем по пробелам
    return text.replace(',', ' ').split()

@log_decorator
def count_short_words(words, max_length=5):
    """
    Подсчитывает количество слов, длина которых меньше или равна max_length.
    """
    return sum(1 for word in words if len(word) <= max_length)

@log_decorator
def find_shortest_word_ending_with_w(words):
    """
    Находит самое короткое слово, заканчивающееся на 'w' (регистр не важен).
    """
    ending_with_w = [word for word in words if word.lower().endswith('w')]
    if not ending_with_w:
        return None
    return min(ending_with_w, key=len)

@log_decorator
def sort_words_by_length(words):
    """
    Сортирует слова по возрастанию их длин.
    """
    return sorted(words, key=len)