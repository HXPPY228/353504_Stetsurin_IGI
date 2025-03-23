# func for ln(1-x)
# Task1
# Stetsurin Elisey 353504
# 23.03.2025

def ln_approx(x, eps, max_iter=500):
    """
    Compute ln(1 - x) using its power series expansion.
    Returns the approximated sum and number of terms used.
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