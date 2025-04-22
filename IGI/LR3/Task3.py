# main for task3
# Task3 24
# Stetsurin Elisey 353504
# 23.03.2025

from text_processing import count_whitespace_and_apostrophes
    
def run_task3():
    """
    Executes Task 3: Analyzes user-input text for whitespace and apostrophe counts.

    This function repeatedly:
    - Prompts the user to input text.
    - Counts whitespace characters and apostrophes using count_whitespace_and_apostrophes.
    - Displays the results in a formatted table.
    - Asks if the user wants to analyze another text, exiting to the menu if not.

    Returns:
        None
    
    Notes:
        - Handles exceptions for empty input and unexpected errors.
        - Continues looping until the user chooses to stop (input other than 'да').
    """
    print("Добро пожаловать в программу анализа текста!")
    print("Эта программа подсчитывает количество пробельных символов и апострофов в введенном тексте.")
    while True:
        try:
            text = input("\nВведите текст для анализа: ")
            if not text:
                raise ValueError("Текст не может быть пустым")
            whitespace, apostrophes = count_whitespace_and_apostrophes(text)
            print(f"\n{'Тип символа':<20} {'Количество':<10}")
            print("-" * 30)
            print(f"{'Пробельные символы':<20} {whitespace:<10}")
            print(f"{'Апострофы':<20} {apostrophes:<10}")
        except ValueError as ve:
            print(f"Ошибка ввода: {ve}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
        again = input("\nАнализировать еще раз? (да/нет): ").strip().lower()
        if again != 'да':
            print("До свидания!")
            return