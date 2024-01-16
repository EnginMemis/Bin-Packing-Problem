class Rectangle:
    def __init__(self, width, height, index):
        self.width = width
        self.height = height
        self.index = index
        self.is_rotated = False

    def rotate(self):
        self.width, self.height = self.height, self.width
        self.is_rotated = not self.is_rotated

class Circle():
    def __init__(self, radius):
        self.radius = radius

class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.placement = []
        self.placeablePoint = [(0, height - 1)]
        self.matrix = [[0 for _ in range(width)] for _ in range(height)]