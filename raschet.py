from OOP4 import Shape
import math

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def calc_square(self):
        return math.pi * self.radius ** 2