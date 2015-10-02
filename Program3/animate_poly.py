"""
@author - Christopher Silva
@date -  10/1/2015
@description - This program uses pantograph to draw three
polygons and multiple points to an html canvas that can
be viewed in a browser at 127.0.0.1:8080
when polygons collide they bounce off of each other
when a point is within a polygon the point turns red

@resources - I modified the base geo.py and used the 
bouncing shape class from the pantograph bouncingball
example as a starting point for my BouncingShape and
BouncingPoint classes
"""
import pantograph
import math
import sys
import random
import itertools


class Point:

    """A point identified by (x,y) coordinates.
    
    supports: str, repr
    as_tuple  -- construct tuple (x,y)
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)

class BouncingPoint:
    """initializes the values for the bouncing shape"""
    def __init__(self, point, size):
        self.x = point[0]
        self.y = point[1]
        self.color = "#0f0"
        self.size = size
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)        

    """updates the position of the BouncingPoint"""
    def update(self, canvas):
        
        if self.x <= 0 or self.x >= canvas.width:
            self.xvel *= -1
            self.x += self.xvel
            self.y += self.yvel
        if self.y <= 0 or self.y >= canvas.height:
            self.yvel *= -1
            self.x += self.xvel
            self.y += self.yvel
        
        self.x += self.xvel
        self.y += self.yvel
        canvas.fill_oval(self.x, self.y, self.size, self.size, self.color)
        
        
        

class BouncingShape(object):
    """initializes the values for the BouncingShape"""
    def __init__(self, shape):
        self.shape = shape
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)
        self.theta = 0

    """updates the position of the BouncingShape"""
    def update(self, canvas):
        rect = self.shape.get_bounding_rect()

        if rect.left <= 0 or rect.right >= canvas.width:
            self.xvel *= -1
            self.shape.translate(self.xvel, self.yvel)
        if rect.top <= 0 or rect.bottom >= canvas.height:
            self.yvel *= -1
            self.shape.translate(self.xvel, self.yvel)

        self.shape.translate(self.xvel, self.yvel)
        self.shape.rotate(self.theta)
        self.shape.draw(canvas)
       
    """checks if a given point is within the Bouncing shape
    and returns true/false"""
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
    """creates the BouncingShapes and BouncingPoints that will be displayed on the canvas"""
    def setup(self):
        self.static_points = []
        self.static_shapes = [pantograph.Polygon([(65, 51),  (90, 74),  (145, 60),  (201, 69),  (265, 46),  (333, 61),  (352, 99),  (370, 129),  (474, 138),  (474, 178),  (396, 225),  (351, 275),  (376, 312),  (382, 356),  (338, 368),  (287, 302),  (224, 304),  (128, 338),  (110, 316),  (129, 270),  (83, 231),  (103, 201),  (126, 162),  (83, 163)], None, "#00f")]
        self.static_shapes.append(pantograph.Polygon([(500,500), (500,600), (600,600), (600,500)], None, "#00f"))  
        self.static_shapes.append(pantograph.Polygon([(700,700), (700,800), (800,800), (800,700)], None, "#00f"))
            
        for i in range(10):
            self.static_points.append((random.randint(0,self.width), random.randint(0,self.height)))

        self.points = [BouncingPoint(shp, 10) for shp in self.static_points]
        self.shapes = [BouncingShape(shp) for shp in self.static_shapes]

    """this clears the screen, checks for collisions, and calls the update
    method for all of the polygons and points"""
    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        """checking for points inside of polygons"""
        for shape in self.shapes:
            for point in self.points:
                if shape.point_inside_polygon(point):
                    point.color = "#f00"
        
        """calling update methods for points and then resetting the color to green"""
        for point in self.points: 
            point.update(self)
            point.color = "#0f0"

        """checking for collision between polygons and calling update methods for polygons
        for collision it first checks if the mbr's of the polygons overlap and if they do it
        does a more accurate brute force collision method. this saves some processing power
        in that you don't need to compare every combination of points in all polygons each frame"""
        for a in self.shapes:
            for b in self.shapes:
                if a != b:
                    if a.shape.intersects(b.shape):
                        for point in b.shape.points:
                            if a.point_inside_polygon(Point(point[0], point[1])):
                                xveltmp = a.xvel
                                yveltmp = a.yvel
                                a.xvel = b.xvel
                                a.yvel = b.yvel
                                b.xvel = xveltmp
                                b.yvel = yveltmp
            a.update(self)

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
