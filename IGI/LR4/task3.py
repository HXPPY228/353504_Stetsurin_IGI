from task3.ln_aprox import LnApproximator
from task4.utils import get_x_value, get_positive_float

def main():
    print("Добро пожаловать в программу вычисления ln(1 - x) с помощью ряда!")
    while True:
        try:
            x_start = get_x_value("Введите начальное x (|x| < 1): ")
            x_end = get_x_value("Введите конечное x (|x| < 1): ")
            x_step = get_positive_float("Введите шаг для x: ")
            eps = get_positive_float("Введите точность (eps): ")
            approximator = LnApproximator(x_start, x_end, x_step, eps)
            approximator.compute_approximations()
            approximator.display_table()
            approximator.compute_statistics()
            approximator.plot_results()
        except ValueError:
            print("Ошибка: введите корректные числовые значения")
        again = input("\nАнализировать еще раз? (да/нет): ").strip().lower()
        if again != 'да':
            print("До свидания!")
            break

if __name__ == "__main__":
    main()