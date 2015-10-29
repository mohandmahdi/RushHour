from Orientation import Orientation
from Copyable import Copyable
import collections

Coordinate = collections.namedtuple('Coordinate', ['x1', 'x2', 'y1', 'y2'])


class Car(Copyable):
    def __init__(self, label, x, y, size, orientation):
        self.label = label
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation

    def is_vertical(self): return self.orientation == Orientation.VERTICAL

    def is_horizontal(self): return self.orientation == Orientation.HORIZONTAL

    def coordinates(self):
        return Coordinate(self.x, self.x + self.size - 1, self.y, self.y) if self.is_horizontal() else Coordinate(self.x, self.x, self.y, self.y + self.size - 1)

    def intersects(self, other):
        c1 = self.coordinates()
        c2 = other.coordinates()
        intersects = False
        if self.is_horizontal():
            if other.is_horizontal():
                intersects = c1.y1 == c2.y1 and (c1.x1 < c2.x1 <= c1.x2 <= c2.x2 or c1.x1 <= c2.x2 <= c1.x2)
            else:
                intersects = c2.y1 <= c1.y1 <= c2.y2 and c1.x1 <= c2.x1 <= c1.x2
        elif other.is_horizontal():
            intersects = c2.x1 <= c1.x1 <= c2.x2 and c1.y1 <= c2.y1 <= c1.y2
        else:
            intersects = c1.x1 == c2.x1 and (c1.y1 < c2.y1 <= c1.y2 <= c2.y2 or c1.y1 <= c2.y2 <= c1.y2)
        return intersects

    def __str__(self):
        return 'Car[label={}, orientation={}, x={}, y={}, size={}]'.format(self.label, 'VERTICAL' if self.orientation == Orientation.VERTICAL else 'HORIZONTAL', self.x, self.y, self.size)