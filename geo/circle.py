"""
points (any dimension).
"""
# region Imports
from math import sqrt

from geo.shape import Shape
from geo.quadrant import Quadrant
from geo.animation import Animation
# endregion Imports

class Circle(Shape):
    """
    a point is defined as a vector of any given dimension.

    for example:

    - create a point at x=2, y=5:

    my_point = Point([2, 5])

    - find distance between two points:

    distance = point1.distance_to(point2)
    """
    def __init__(self, coordinates, rayon=10, id=None, opacity=None, animation=False, style=True):
        """
        Instantiate a displayable circle
        """
        super().__init__(id=id, animation=Animation if animation else None, style=style, opacity=opacity)
        self.set_animation_start(coordinates, opacity)
        self.start_coordinates = coordinates
        self.coordinates = list(coordinates) # Copy coordinates for animation
        self.rayon = rayon

    def copy(self):
        """
        return copy of given point.
        """
        return Circle(list(self.coordinates), self.rayon)

    def distance_to(self, other):
        """
        euclidean distance between two points.
        """
        if self < other:
            return other.distance_to(self)  # we are now a symmetric function

        total = sum(((c1 - c2) ** 2 for c1, c2 in zip(self.coordinates, other.coordinates)))
        return sqrt(total)

    def apply_translation(self, value):
        for i, v in enumerate(value.coordinates):
            self.coordinates[i] += v

    def apply_inflation(self, value):
        self.rayon += value

    def reset(self):
        self.animations.reset()
        self.coordinates = list(self.start_coordinates)

    # region SVG
    def bounding_quadrant(self):
        """
        Return a quadrant who contain polygon
        :return: the quadrant who contain polygon
        """
        return Quadrant(self.coordinates, self.coordinates)

    def svg_content(self):
        """
        Return a quadrant who contain polygon
        :return: the quadrant who contain polygon
        """
        return '<circle cx="{}" cy="{}" r="{}" {}/>\n'.format(*self.coordinates, self.rayon, self.get_styles())
    # endregion SVG

    # region Override
    # region Math Operation
    def __add__(self, other):
        """
        addition operator. (useful for translations)
        """
        return Circle([i + j for i, j in zip(self.coordinates, other.coordinates)])

    def __sub__(self, other):
        """
        substraction operator. (useful for translations)
        """
        return Circle([i - j for i, j in zip(self.coordinates, other.coordinates)])

    def __mul__(self, factor):
        """
        multiplication by scalar operator. (useful for scaling)
        """
        return Circle([c * factor for c in self.coordinates])

    def __truediv__(self, factor):
        """
        division by scalar operator. (useful for scaling)
        """
        return Circle([c / factor for c in self.coordinates])

    def __abs__(self):
        return Circle([abs(c) for c in self.coordinates])

    def __eq__(self, other):
        return isinstance(other, Circle) and self.coordinates == other.coordinates and self.rayon == other.rayon

    def __ne__(self, other):
        return not isinstance(other, Circle) or self.coordinates != other.coordinates or self.rayon != other.rayon
    # endregion Math Operation

    def __str__(self):
        """
        print code generating the point.
        """
        return f"{self.__class__.__name__}({', '.join(str(c) for c in self.coordinates)})"

    def __repr__(self):
        return f"{self.__class__.__name__[0]}({', '.join(str(c) for c in self.coordinates)})"

    def __hash__(self):
        return sum((hash(c) for c in self.coordinates)) + hash(self.rayon)

    def __lt__(self, other):
        """
        lexicographical comparison
        """
        return self.coordinates < other.coordinates

    def __iter__(self):
        for value in self.coordinates:
            yield value
    # endregion Override
