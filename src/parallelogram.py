from math import hypot
from operator import itemgetter

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return hypot(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'

    def __repr__(self):
        return "Point(%d, %d)" % (self.x, self.y)

class Parallelogram:
    def __init__(self, coords_ls, m=None, b=None):
        """
        :param `coords_ls` <list>: list of points that form the parallelogram. 
            If only 2 points in the list, they are assumed to be the top-left and 
                bottom-right coordinates of a parallelogram with right angles.
                Required: m and b (coefficents of equation for top border: y=mx+b).
            If 4 Points in the list, they are assumed to be the 4 corners of the shape.
        :param `m` <float>: slope of top border (y=mx+b).
        :param `b` <float>: when x = 0.

        Resulting calculations:
            self.p1 : top-left corner of bounding box.
            self.p2 : bottom-right corner of bounding box.
            self.p3: top-right corner of bounding box.
            self.p4: botton_left corner of bounding box.
        """
        num_points = len(coords_ls)
        
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None

        if num_points == 2 and m and b:
            pass
        elif num_points == 4:
            pass
        else:
            raise ValueError(f"Object takes a list with either 2 points (and line equation coefficients) or 4 points. {num_points} points were given")
        # get the point closest to the origin; that one will be the top-left corner point
        
    @staticmethod
    def __sort_by_distance(coords_ls):
        p0 = Point(0, 0) # origin for distance calculation
        dist_ls = [(p, p.distance(p0)) for p in coords_ls]
        return sorted(dist_ls,key=itemgetter(0))

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3 and self.p4 == other.p4

    def __str__(self):
        return "({self.p1}, {self.p2}, {self.p3}, {self.p4})"