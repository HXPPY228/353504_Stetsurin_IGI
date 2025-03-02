import os
from geometric_lib import circle

radius = float(os.getenv("RADIUS", 5))
area = circle.area(radius)
perimeter = circle.perimeter(radius)
print(f"Площадь круга с радиусом {radius}: {area}")
print(f"Периметр круга с радиусом {radius}: {perimeter}")