import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import json
import matplotlib.patches as patches
import time
from shapes import *
from get_data import readFile

class BottomLeftFill():
    def __init__(self, bin, polygons):
        self.bin = bin
        self.polygons = polygons
        self.density = 0.0

    def placePoly(self, rect, position, count):
        x, y = position
        for i in range(y, y - rect.height, -1):
            for j in range(x, x + rect.width):
                if i < 0 or i >= self.bin.height or j < 0 or j >= self.bin.width:
                    return False
                elif self.bin.matrix[i][j] != 0:
                    return False

        for i in range(y, y - rect.height, -1):
            for j in range(x, x + rect.width):
                self.bin.matrix[i][j] = count

        if x + rect.width < self.bin.width and self.bin.matrix[y][x + rect.width] == 0:
            if (x + rect.width, y) not in self.bin.placeablePoint:
                self.bin.placeablePoint.append((x + rect.width, y))
        if y - rect.height < self.bin.height and self.bin.matrix[y - rect.height][x] == 0:
            if (x, y - rect.height) not in self.bin.placeablePoint:
                self.bin.placeablePoint.append((x, y - rect.height))

        self.bin.placeablePoint.remove(position)

        return True
        

    def place(self):
        count = 1
        for j in range(len(self.polygons)):
            self.bin.placeablePoint = sorted(self.bin.placeablePoint, key=lambda x: (-x[1], x[0]))
            isPlaced = False
            index = 0
            while index < len(self.bin.placeablePoint) and not isPlaced:
                position = self.bin.placeablePoint[index]
                if self.placePoly(self.polygons[j], position, count):
                    isPlaced = True
                index += 1
            """if isPlaced == False:
                print(f"{rectangles[j].width} - {rectangles[j].height} Yerlestirilemedi")"""
            if isPlaced == True:
                count += 1
                self.density += (self.polygons[j].width * self.polygons[j].height) / (self.bin.height * self.bin.width)
                self.bin.placement.append([(position[0], self.bin.height - position[1] - 1),(self.polygons[j].width, self.polygons[j].height)]) 