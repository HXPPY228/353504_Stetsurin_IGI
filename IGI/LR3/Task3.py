# main for task3
# Task3
# Stetsurin Elisey 353504
# 23.03.2025

from text_analysis import count_whitespace_and_apostrophes

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
        break