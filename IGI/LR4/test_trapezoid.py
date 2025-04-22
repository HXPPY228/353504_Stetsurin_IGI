import math
import unittest
from task4.geometry import IsoscelesTrapezoid
from task4.visualization import Visualizer

class TrapezoidTestCase(unittest.TestCase):
    """Test case for IsoscelesTrapezoid class."""

    def test_area(self):
        """Test the area calculation of the trapezoid."""
        trapezoid = IsoscelesTrapezoid(base_a=10, side_b=5, angle_y_degrees=60, color="red")
        # Expected area: (base_a + base_c) * height / 2
        height = 5 * math.sin(math.radians(60))  # height = side_b * sin(angle)
        base_diff = 5 * math.cos(math.radians(60))
        base_c = 10 - 2 * base_diff
        expected_area = (10 + base_c) * height / 2
        self.assertAlmostEqual(trapezoid.area(), expected_area, places=5)

    def test_draw(self):
        """Test the visualization method (should return None)."""
        trapezoid = IsoscelesTrapezoid(base_a=10, side_b=5, angle_y_degrees=60, color="red")
        visualizer = Visualizer(trapezoid, "Test Trapezoid")
        self.assertIsNone(visualizer.run())

    def test_figure_name(self):
        """Test setting and getting the figure name."""
        trapezoid = IsoscelesTrapezoid(base_a=10, side_b=5, angle_y_degrees=60, color="red")
        trapezoid.figure_name = "My Trapezoid"
        self.assertEqual(trapezoid.figure_name, "My Trapezoid")

    def test_str(self):
        """Test the string representation of the trapezoid."""
        trapezoid = IsoscelesTrapezoid(base_a=10, side_b=5, angle_y_degrees=60, color="red")
        trapezoid.figure_name = "My Trapezoid"
        expected_str = "My Trapezoid with base_a 10 units, side_b 5 units, color: red, area: 32.48 sq.units"
        self.assertEqual(str(trapezoid), expected_str)

if __name__ == '__main__':
    unittest.main()