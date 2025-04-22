from task5.matrix_operations import MatrixOperations
from task5.stats import Statistics
from task4.utils import get_positive_int, continue_program

def main():
    """Main function to run the matrix operations program."""
    print("Welcome to the NumPy Matrix Operations Program (Lab 5)")
    while True:
        try:
            # Get matrix dimensions from user
            rows = get_positive_int("Enter the number of rows: ")
            cols = get_positive_int("Enter the number of columns (at least 2): ")
            if cols < 2:
                raise ValueError("Number of columns must be at least 2 for correlation.")

            # Create and display matrix
            matrix_ops = MatrixOperations(rows, cols)
            print("\nOriginal Matrix:")
            print(matrix_ops)

            # Swap maximum elements in first and last columns
            matrix_ops.swap_max_elements()
            print("\nMatrix after swapping max elements in first and last columns:")
            print(matrix_ops)

            # Perform statistical operations
            stats = Statistics(matrix_ops.matrix)
            print("\nStatistical Results:")
            print(f"Mean: {stats.mean():.2f}")
            print(f"Median: {stats.median():.2f}")
            print(f"Variance: {stats.variance():.2f}")
            print(f"Standard Deviation: {stats.std_dev():.2f}")
            print(f"Correlation between first and last columns: {stats.correlation(0, -1)}")

            # Ask to continue
            if not continue_program():
                print("Exiting program. Goodbye!")
                break

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()