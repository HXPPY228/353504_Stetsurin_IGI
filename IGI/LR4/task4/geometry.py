from abc import ABC, abstractmethod
import math

class GeometricShape(ABC):
    """Abstract base class for geometric shapes."""
    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass

    @classmethod
    def shape_name(cls):
        """Return the name of the shape."""
        return cls._shape_name

class Color:
    """Class to manage the color of a geometric shape."""
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        """Get the color of the shape."""
        return self._color

    @color.setter
    def color(self, value):
        """Set the color of the shape."""
        if not isinstance(value, str) or not value:
            raise ValueError("Color must be a non-empty string")
        self._color = value

class IsoscelesTrapezoid(GeometricShape):
    """Class representing an isosceles trapezoid."""
    _shape_name = "Isosceles Trapezoid"

    def __init__(self, base_a, side_b, angle_y_degrees, color):
        """Initialize trapezoid with base, side, angle, and color."""
        if base_a <= 0 or side_b <= 0 or angle_y_degrees <= 0 or angle_y_degrees >= 90:
            raise ValueError("Invalid parameters: base_a, side_b must be positive; angle_y must be 0 < y < 90")
        self._base_a = base_a
        self._side_b = side_b
        self._angle_y = math.radians(angle_y_degrees)
        self._color = Color(color)
        self._height = self._side_b * math.sin(self._angle_y)
        self._base_diff = self._side_b * math.cos(self._angle_y)
        self._base_c = self._base_a - 2 * self._base_diff
        self._figure_name = self.shape_name()  # Default figure name
        if self._base_c <= 0:
            raise ValueError("Invalid parameters: top base must be positive")

    @property
    def base_a(self):
        """Get base_a."""
        return self._base_a

    @base_a.setter
    def base_a(self, value):
        """Set base_a."""
        if value <= 0:
            raise ValueError("Base_a must be positive")
        self._base_a = value

    @property
    def side_b(self):
        """Get side_b."""
        return self._side_b

    @side_b.setter
    def side_b(self, value):
        """Set side_b."""
        if value <= 0:
            raise ValueError("Side_b must be positive")
        self._side_b = value

    @property
    def angle_y_degrees(self):
        """Get angle_y in degrees."""
        return math.degrees(self._angle_y)

    @angle_y_degrees.setter
    def angle_y_degrees(self, value):
        """Set angle_y in degrees."""
        if value <= 0 or value >= 90:
            raise ValueError("Angle_y must be between 0 and 90 degrees")
        self._angle_y = math.radians(value)

    @property
    def figure_name(self):
        """Get the figure name."""
        return self._figure_name

    @figure_name.setter
    def figure_name(self, value):
        """Set the figure name."""
        if not isinstance(value, str) or not value:
            raise ValueError("Figure name must be a non-empty string")
        self._figure_name = value

    def area(self):
        """Calculate the area of the trapezoid."""
        return (self._base_a + self._base_c) * self._height / 2

    def __str__(self):
        """Return string representation of the trapezoid."""
        return f"{self.figure_name} with base_a {self._base_a} units, side_b {self._side_b} units, color: {self._color.color}, area: {self.area():.2f} sq.units"