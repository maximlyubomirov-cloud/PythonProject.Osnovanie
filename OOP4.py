
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calc_square(self):
        pass

    def display(self):
        print(f'Название: {self.name}')


class Rectangle(Shape):
    def __init__(self, name, height, width):
        super().__init__(name)
        self.height = height
        self.width = width

    def calc_square(self):
        return self.height * self.width

    def display(self):
        super().display()
        print(f'Высота: {self.height}\nШирина: {self.width}')