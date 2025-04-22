import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from task4.geometry import IsoscelesTrapezoid

class Visualizer:
    """Class for visualizing a trapezoid using Matplotlib."""
    def __init__(self, trapezoid, text):
        self.trapezoid = trapezoid
        self.text = text

    def run(self):
        """Draw the trapezoid and save it to a file."""
        base_a = self.trapezoid.base_a
        base_c = self.trapezoid._base_c
        height = self.trapezoid._height
        base_diff = self.trapezoid._base_diff

        points = [
            (0, 0),
            (base_a, 0),
            (base_a - base_diff, height),
            (base_diff, height)
        ]

        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        polygon = Polygon(points, closed=True, fill=True, color=self.trapezoid._color.color.lower())
        ax.add_patch(polygon)

        text_x = base_a / 2
        text_y = -2
        ax.text(text_x, text_y, self.text, fontsize=12, ha='center')

        ax.set_xlim(-1, base_a + 1)
        ax.set_ylim(text_y - 0.5, height + 1)

        plt.savefig("trapezoid.png")
        plt.show()
