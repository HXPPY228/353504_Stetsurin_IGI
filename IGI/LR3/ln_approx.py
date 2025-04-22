# func for ln(1-x)
# Task1 24
# Stetsurin Elisey 353504
# 23.03.2025

def ln_approx(x, eps, max_iter=500):
    """
    Computes the natural logarithm of (1 - x) using its power series expansion.
    
    The function uses an iterative approach to approximate ln(1 - x) with a given precision.
    It stops when the absolute value of the next term is less than the specified epsilon or
    when the maximum number of iterations is reached.
    
    Args:
        x (float): The input value, must satisfy |x| < 1.
        eps (float): The desired precision for the approximation.
        max_iter (int, optional): The maximum number of iterations. Defaults to 500.
    
    Returns:
        tuple: A tuple containing the approximated value and the number of terms used.
               Returns (None, None) if |x| >= 1.
    
    Notes:
        Prints a warning if the maximum iterations are reached without achieving the desired precision.
    """
    # Check if |x| < 1
    if abs(x) >= 1:
        print("Ошибка: |x| должно быть меньше 1")
        return None, None
    
    # Initialize variables
    sum_value = 0
    term = -x  # First term for n=1
    n = 0
    
    # Compute series until term < eps or max iterations reached
    while n < max_iter and abs(term) >= eps:
        sum_value += term
        n += 1
        if n < max_iter:
            # Next term: term_n+1 = term_n * x * (n / (n+1))
            term = term * x * (n / (n + 1))
    
    # Warn if max iterations reached without achieving accuracy
    if n == max_iter and abs(term) >= eps:
        print("Предупреждение: достигнуто максимальное количество итераций без достижения заданной точности")
    
    return sum_value, n