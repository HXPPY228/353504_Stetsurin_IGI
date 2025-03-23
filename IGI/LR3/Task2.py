# main task2
# Task2
# Stetsurin Elisey 353504
# 23.03.2025

from input_methods import generate_random_list, user_input_list
from count_calculator import count_in_range

print("Добро пожаловать в программу подсчета чисел!")
print("Эта программа подсчитывает количество чисел от 5 до 25 в списке.")
    
while True:
    print("\nВыберите метод инициализации:")
    print("1. Сгенерировать случайный список")
    print("2. Ввести числа вручную")
    choice = input("Выбор (1 или 2): ").strip()
    
    try:
        if choice == '1':
            size = int(input("Введите размер списка: "))
            numbers = generate_random_list(size)
            print(f"Сгенерированный список: {numbers}")
        elif choice == '2':
            numbers = user_input_list()
            print(f"Ваш список: {numbers}")
        else:
            print("Неверный выбор. Выберите 1 или 2.")
            continue
            
        count = count_in_range(numbers)
        print(f"Количество чисел от 5 до 25: {count}")
        
    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        
    again = input("\nАнализировать еще раз? (да/нет): ").strip().lower()
    if again != 'да':
        print("До свидания!")
        break
