import math
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, median, mode, variance, stdev

def ln_approx(x, eps, max_iter=500):
    """
    Computes the natural logarithm of (1 - x) using its power series expansion.
    
    Args:
        x (float): The input value, must satisfy |x| < 1.
        eps (float): The desired precision for the approximation.
        max_iter (int, optional): The maximum number of iterations. Defaults to 500.
    
    Returns:
        tuple: (approx, n_terms, partial_sums)
               - approx: the approximated value
               - n_terms: the number of terms used
               - partial_sums: list of partial sums during approximation
               Returns (None, None, None) if |x| >= 1.
    """
    if abs(x) >= 1:
        print("Ошибка: |x| должно быть меньше 1")
        return None, None, None
    
    sum_value = 0
    term = -x
    n = 0
    partial_sums = []
    
    while n < max_iter and abs(term) >= eps:
        sum_value += term
        partial_sums.append(sum_value)
        n += 1
        if n < max_iter:
            term = term * x * (n / (n + 1))
    
    if n == max_iter and abs(term) >= eps:
        print("Предупреждение: достигнуто максимальное количество итераций без достижения заданной точности")
    
    return sum_value, n, partial_sums

class LnApproximator:
    """Class for approximating ln(1 - x), computing statistics, and plotting results."""
    
    def __init__(self, x_start, x_end, x_step, eps):
        """
        Initialize the LnApproximator.
        
        Args:
            x_start (float): Starting value of x.
            x_end (float): Ending value of x.
            x_step (float): Step size for x.
            eps (float): Precision for approximation.
        """
        self.x_values = np.arange(x_start, x_end, x_step)
        self.eps = eps
        self.approximations = []
        self.exact_values = []
        self.n_terms = []
        self.partial_sums = []  # List of lists for partial sums of each x
    
    def compute_approximations(self):
        """Compute approximations and exact values for each x."""
        for x in self.x_values:
            if abs(x) >= 1:
                print(f"Пропуск x={x}, так как |x| >= 1")
                continue
            approx, n, partial = ln_approx(x, self.eps)
            if approx is not None:
                self.approximations.append(approx)
                self.exact_values.append(math.log(1 - x))
                self.n_terms.append(n)
                self.partial_sums.append(partial)
    
    def compute_statistics(self):
        """Compute and display statistics for partial sums of each x."""
        for i, partial in enumerate(self.partial_sums):
            if partial:
                print(f"\nСтатистика для x={self.x_values[i]:.5f}:")
                print(f"Среднее арифметическое: {mean(partial):.10f}")
                print(f"Медиана: {median(partial):.10f}")
                try:
                    print(f"Мода: {mode(partial):.10f}")
                except:
                    print("Мода: Нет уникальной моды")
                if len(partial) > 1:
                    try:
                        print(f"Дисперсия: {variance(partial):.10f}")
                        print(f"СКО: {stdev(partial):.10f}")
                    except:
                        print(f"Ошибка вычисления дисперсии/СКО")
                else:
                    print("Дисперсия: Невозможно вычислить (менее 2 элементов)")
                    print("СКО: Невозможно вычислить (менее 2 элементов)")
                    
    def display_table(self):
        """Display a table of approximation results."""
        print("\nЗдесь x — значение аргумента, F(x) — значение функции, n — количество просуммированных членов ряда, Math F(x) — значение функции, вычисленное с помощью модуля math.")
        print(f"{'x':<15} {'n':<10} {'F(x)':<20} {'Math F(x)':<20} {'eps':<15}")
        print("-" * 80)
        for i in range(len(self.approximations)):
            x = self.x_values[i]
            n = self.n_terms[i]
            approx = self.approximations[i]
            exact = self.exact_values[i]
            print(f"{x:<15.5f} {n:<10} {approx:<20.10f} {exact:<20.10f} {self.eps:<15.5f}")
            
    def plot_results(self):
        """Plot the approximation and exact function."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_values[:len(self.approximations)], self.approximations, label='Аппроксимация', color='blue')
        plt.plot(self.x_values[:len(self.exact_values)], self.exact_values, label='Точное ln(1 - x)', color='red', linestyle='--')
        plt.xlabel('x')
        plt.ylabel('ln(1 - x)')
        plt.title('Аппроксимация vs Точное значение ln(1 - x)')
        plt.legend()
        plt.grid(True)
        plt.annotate('Точное', xy=(self.x_values[len(self.exact_values)-1], self.exact_values[-1]), 
                     xytext=(self.x_values[len(self.exact_values)-1]-0.1, self.exact_values[-1]+0.5),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.savefig('ln_approx_plot.png')
        print("График сохранён в 'ln_approx_plot.png'")