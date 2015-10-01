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
    def __init__(self, point, size):
        self.x = point[0]
        self.y = point[1]
        self.color = "#0f0"
        self.size = size
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)        
        
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
    def __init__(self, shape):
        self.shape = shape
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)
        self.theta = 0
        self.rvel = 0#(math.pi / 2) * random.random()

    def update(self, canvas):
        rect = self.shape.get_bounding_rect()

        if rect.left <= 0 or rect.right >= canvas.width:
            self.xvel *= -1
            self.shape.translate(self.xvel, self.yvel)
        if rect.top <= 0 or rect.bottom >= canvas.height:
            self.yvel *= -1
            self.shape.translate(self.xvel, self.yvel)

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
        self.static_points = []
        self.static_shapes = [pantograph.Polygon([(65, 51),  (90, 74),  (145, 60),  (201, 69),  (265, 46),  (333, 61),  (352, 99),  (370, 129),  (474, 138),  (474, 178),  (396, 225),  (351, 275),  (376, 312),  (382, 356),  (338, 368),  (287, 302),  (224, 304),  (128, 338),  (110, 316),  (129, 270),  (83, 231),  (103, 201),  (126, 162),  (83, 163)], None, "#00f")]
        self.static_shapes.append(pantograph.Polygon([(500,500), (500,600), (600,600), (600,500)], None, "#00f"))  
        self.static_shapes.append(pantograph.Polygon([(700,700), (700,800), (800,800), (800,700)], None, "#00f"))
            
        for i in range(10):
            self.static_points.append((random.randint(0,self.width), random.randint(0,self.height)))

        self.points = [BouncingPoint(shp, 10) for shp in self.static_points]
        self.shapes = [BouncingShape(shp) for shp in self.static_shapes]

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)

        for shape in self.shapes:
            for point in self.points:
                if shape.point_inside_polygon(point):
                    point.color = "#f00"
            
        for point in self.points: 
            point.update(self)
            point.color = "#0f0"

        for a in self.shapes:
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
            a.update(self)

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
