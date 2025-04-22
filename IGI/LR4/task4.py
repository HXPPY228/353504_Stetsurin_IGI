from task4.geometry import IsoscelesTrapezoid
from task4.utils import get_positive_float, get_angle, get_string, continue_program
from task4.visualization import Visualizer

def main():
    """Main function to run the trapezoid program."""
    print("Isosceles Trapezoid Program")
    while True:
        try:
            base_a = get_positive_float("Enter base_a: ")
            side_b = get_positive_float("Enter side_b: ")
            angle_y = get_angle("Enter angle_y (degrees): ")
            color = get_string("Enter color (e.g., red, blue, green): ")
            text = get_string("Enter text for the figure: ")

            trapezoid = IsoscelesTrapezoid(base_a, side_b, angle_y, color)
            print(trapezoid)

            visualizer = Visualizer(trapezoid, text)
            visualizer.run()

            if not continue_program():
                break

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()