"""Point and Rectangle classes.

This code is in the public domain.

Point  -- point with (x,y) coordinates
Rect  -- two points, forming a rectangle
"""
import pantograph
import math
import sys
import random
import itertools


class Point:

    """A point identified by (x,y) coordinates.

    supports: +, -, *, /, str, repr

    length  -- calculate length of vector to point from origin
    distance_to  -- calculate distance between two points
    as_tuple  -- construct tuple (x,y)
    clone  -- construct a duplicate
    integerize  -- convert x & y to integers
    floatize  -- convert x & y to floats
    move_to  -- reset x & y
    slide  -- move (in place) +dx, +dy, as spec'd by point
    slide_xy  -- move (in place) +dx, +dy
    rotate  -- rotate around the origin
    rotate_about  -- rotate around another point
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, p):
        """Point(x1+x2, y1+y2)"""
        return Point(self.x+p.x, self.y+p.y)

    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Point(self.x-p.x, self.y-p.y)

    def __mul__( self, scalar ):
        """Point(x1*x2, y1*y2)"""
        return Point(self.x*scalar, self.y*scalar)

    def __div__(self, scalar):
        """Point(x1/x2, y1/y2)"""
        return Point(self.x/scalar, self.y/scalar)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()

    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)

    def clone(self):
        """Return a full copy of this point."""
        return Point(self.x, self.y)

    def integerize(self):
        """Convert co-ordinate values to integers."""
        self.x = int(self.x)
        self.y = int(self.y)

    def floatize(self):
        """Convert co-ordinate values to floats."""
        self.x = float(self.x)
        self.y = float(self.y)

    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y

    def slide(self, p):
        '''Move to new (x+dx,y+dy).

        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + p.x
        self.y = self.y + p.y

    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).

        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + dx
        self.y = self.y + dy

    def rotate(self, rad):
        """Rotate counter-clockwise by rad radians.

        Positive y goes *up,* as in traditional mathematics.

        Interestingly, you can use this in y-down computer graphics, if
        you just remember that it turns clockwise, rather than
        counter-clockwise.

        The new position is returned as a new Point.
        """
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
        return Point(x,y)

    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees.

        Positive y goes *up,* as in traditional mathematics.

        The new position is returned as a new Point.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result

    def set_direction(self,direction):
        assert direction in ['N','NE','E','SE','S','SW','W','NW']

        self.direction = direction

    def update_position(self):
        if self.direction == "N":
            self.y -= 1
        if self.direction == "NE":
            self.y -= 1
            self.x += 1
        if self.direction == "E":
            self.x += 1
        if self.direction == "SE":
            self.x += 1
            self.y += 1
        if self.direction == "S":
            self.y += 1
        if self.direction == "SW":
            self.x -= 1
            self.y += 1
        if self.direction == "W":
            self.x -= 1
        if self.direction == "NW":
            self.y -= 1
            self.x -= 1



class Rect:

    """A rectangle identified by two points.

    The rectangle stores left, top, right, and bottom values.

    Coordinates are based on screen coordinates.

    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom

    set_points  -- reset rectangle coordinates
    contains  -- is a point inside?
    overlaps  -- does a rectangle overlap?
    top_left  -- get top-left corner
    bottom_right  -- get bottom-right corner
    expanded_by  -- grow (or shrink)
    """

    def __init__(self, pt1, pt2):
        """Initialize a rectangle from two points."""
        self.set_points(pt1, pt2)

    def set_points(self, pt1, pt2):
        """Reset the rectangle coordinates."""
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)

    def contains(self, pt):
        """Return true if a point is inside the rectangle."""
        x,y = pt.as_tuple()
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    def overlaps(self, other):
        """Return true if a rectangle overlaps this rectangle."""
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    def top_left(self):
        """Return the top-left corner as a Point."""
        return Point(self.left, self.top)

    def bottom_right(self):
        """Return the bottom-right corner as a Point."""
        return Point(self.right, self.bottom)

    def expanded_by(self, n):
        """Return a rectangle with extended borders.

        Create a new rectangle that is wider and taller than the
        immediate one. All sides are extended by "n" points.
        """
        p1 = Point(self.left-n, self.top-n)
        p2 = Point(self.right+n, self.bottom+n)
        return Rect(p1, p2)

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,                                         self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,                             Point(self.left, self.top),                             Point(self.right, self.bottom))
"""
class taken from pantograph bouncing ball example and modified
"""
class BouncingShape(object):
    def __init__(self, shape):
        self.shape = shape
        self.theta = 0
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)
        self.rvel = 0#(math.pi / 2) * random.random()

    def update(self, canvas):
        rect = self.shape.get_bounding_rect()

        if rect.left <= 0 or rect.right >= canvas.width:
            self.xvel *= -1
        if rect.top <= 0 or rect.bottom >= canvas.height:
            self.yvel *= -1

        self.theta += self.rvel
        if self.theta > math.pi:
            self.theta -= 2 * math.pi

        self.shape.translate(self.xvel, self.yvel)
        self.shape.rotate(self.theta)
        self.shape.draw(canvas)
        
    def point_inside_polygon(self, p):
        
        if type(self.shape) is not pantograph.shapes.Polygon:
            raise NotImplementedError
        
        n = len(self.shape.points)
        inside =False

        p1x,p1y = (self.shape.points[0].x, self.shape.points[0].y)
        for i in range(n+1):
            p2x,p2y = (self.shape.points[i % n].x, self.shape.points[i % n].y)
            if p.y > min(p1y,p2y):
                if p.y <= max(p1y,p2y):
                    if p.x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (p.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or p.x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside
        
class Driver(pantograph.PantographHandler):

    def setup(self):
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)
        
        static_points = []
        static_shapes = [pantograph.Polygon([(65, 51),  (90, 74),  (145, 60),  (201, 69),  (265, 46),  (333, 61),  (352, 99),  (370, 129),  (474, 138),  (474, 178),  (396, 225),  (351, 275),  (376, 312),  (382, 356),  (338, 368),  (287, 302),  (224, 304),  (128, 338),  (110, 316),  (129, 270),  (83, 231),  (103, 201),  (126, 162),  (83, 163)], None, "#00f")]
        static_shapes.append(pantograph.Polygon([(500,500), (500,600), (600,600), (600,500)], None, "#00f"))  
        static_shapes.append(pantograph.Polygon([(700,700), (700,800), (800,800), (800,700)], None, "#00f"))
            
        for i in range(10):
            static_points.append(pantograph.Circle(random.randint(0,self.width), random.randint(0,self.height), 7, "0f0"))

        self.points = [BouncingShape(shp) for shp in static_points]
        self.shapes = [BouncingShape(shp) for shp in static_shapes]

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)

        for shape in self.shapes:
            for point in self.points:
                if shape.point_inside_polygon(Point(point.shape.x, point.shape.y)):
                    point.shape.fill_color = "#f00"
            
        for point in self.points: 
            point.update(self)
            point.shape.fill_color = "#0f0"

        for a in self.shapes:
            a.update(self)
            for b in self.shapes:
                if a != b:
                    for point in b.shape.points:
                        if a.point_inside_polygon(Point(point[0], point[1])):
                            xveltmp = a.xvel
                            yveltmp = a.yvel
                            a.xvel = b.xvel
                            a.yvel = b.yvel
                            b.xvel = xveltmp
                            b.yvel = yveltmp

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
