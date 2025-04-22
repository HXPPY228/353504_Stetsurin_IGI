def get_positive_float(prompt):
    """Получить положительное число от пользователя."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Значение должно быть положительным.")
                continue
            return value
        except ValueError:
            print("Введите число.")
            
def get_x_value(prompt):
    """Получить число от пользователя, удовлетворяющее |x| < 1."""
    while True:
        try:
            value = float(input(prompt))
            if abs(value) >= 1:
                print("Значение должно удовлетворять |x| < 1.")
                continue
            return value
        except ValueError:
            print("Введите число.")

def get_angle(prompt):
    """Получить угол от 0 до 90 градусов."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0 or value >= 90:
                print("Угол должен быть от 0 до 90 градусов.")
                continue
            return value
        except ValueError:
            print("Введите число.")

def get_string(prompt):
    """Получить непустую строку."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Строка не может быть пустой.")
            continue
        return value

def get_positive_int(prompt):
    """Get a positive integer from user input."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Value must be a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
def continue_program():
    """Продолжить программу?"""
    return input("Do you want to continue? (yes/no): ").lower().startswith('y')