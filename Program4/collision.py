import random
import math
import numpy as np
import pantograph
import time

class node:
    def __init__(self, x, y, item, bbox):
        self.x = x
        self.y = y
        self.item = item
        self.bbox = bbox
        self.children = [None, None, None, None]
        #self.children = {'NE': None, 'SE': None, 'SW': None, 'NW': None}
        
    def __str__(self):
        return "node at (%f,%f)" % (self.x, self.y)
    def __repr__(self):
        return "node at (%f,%f)" % (self.x, self.y)
        

class quadtree:
    def __init__(self, bounds):
        self.root = None
        self.bbox = [bounds.minX, bounds.minY, bounds.maxX, bounds.maxY]

    def insertBall(self, ball):
        newnode = node(ball.x, ball.y, ball, self.bbox)
        if self.root == None:
            newnode.bbox = self.bbox
            self.root = newnode
        else:
            self._insert(self.root, newnode)

    def insert(self, x, y, item):
        newnode = node(x, y, item, )
        if self.root == None:
            newnode.bbox = self.bbox
            self.root = newnode
        else:
            self._insert(self.root, newnode)
                
    def _insert(self, subroot, node):
        direction = self._compare(subroot, node)
        while subroot.children[direction] != None:
            subroot = subroot.children[direction]
            direction = self._compare(subroot, node)
        if direction == None:
            print "couldn't insert"
        else:
            if direction == 0:
                node.bbox = [subroot.x, subroot.y, subroot.bbox[2], subroot.bbox[3]]
            elif direction == 1:
                node.bbox = [subroot.x, subroot.bbox[1], subroot.bbox[2], subroot.y]
            elif direction == 2:
                node.bbox = [subroot.bbox[0], subroot.bbox[1], subroot.x, subroot.y]
            elif direction == 3:
                node.bbox = [subroot.bbox[0], subroot.y, subroot.x, subroot.bbox[3]]
            subroot.children[direction] = node
        
                
    def _compare(self, node1, node2):
        if node2.x >= node1.x and node2.y >= node1.y:
                return 0
        elif node2.x <= node1.x and node2.y <= node1.y:
                return 2
        elif node2.x > node1.x:
                return 1
        elif node2.y > node1.y:
                return 3
                
    def traversal(self):
        self._traversal(self.root)
        
    def _traversal(self, subroot):
        if subroot == None:
            return
        print subroot
        self._traversal(subroot.children[0])
        self._traversal(subroot.children[1])
        self._traversal(subroot.children[2])
        self._traversal(subroot.children[3])
        
    def getBBoxes(self):
        return self._getBBoxes(self.root)        
        
    def _getBBoxes(self, subroot):
        bboxes = []
        bboxes.append(subroot.bbox + [subroot.x, subroot.y])
        
        if subroot.children[0] != None:
                bboxes = bboxes + self._getBBoxes(subroot.children[0])
        if subroot.children[1] != None:
                bboxes = bboxes + self._getBBoxes(subroot.children[1])
        if subroot.children[2] != None:
                bboxes = bboxes + self._getBBoxes(subroot.children[2])
        if subroot.children[3] != None:
                bboxes = bboxes + self._getBBoxes(subroot.children[3])

        return bboxes
        
    def regionSearch(self, bbox, searchnode):
        return self._regionSearch(self.root, bbox, searchnode)
        
    def _regionSearch(self, subroot, searchbox, searchnode):
        nodes = []
        if self._inRegion(subroot, searchbox) and subroot.item != searchnode:
            nodes.append(subroot.item)
                
        if subroot.children[0] != None and self._rectangle_overlaps_region(searchbox, subroot.children[0].bbox):
            nodes = nodes + self._regionSearch(subroot.children[0], searchbox, searchnode)
        if subroot.children[1] != None and self._rectangle_overlaps_region(searchbox, subroot.children[1].bbox):
            nodes = nodes + self._regionSearch(subroot.children[1], searchbox, searchnode)
        if subroot.children[2] != None and self._rectangle_overlaps_region(searchbox, subroot.children[2].bbox):
            nodes = nodes + self._regionSearch(subroot.children[2], searchbox, searchnode)
        if subroot.children[3] != None and self._rectangle_overlaps_region(searchbox, subroot.children[3].bbox):
            nodes = nodes + self._regionSearch(subroot.children[3], searchbox, searchnode)
        return nodes
            
    def _inRegion(self, node, searchbox):
        return (node.x >= searchbox[0] and node.x <= searchbox[1] and node.y >= searchbox[2] and node.y <= searchbox[3])
            
    def _rectangle_overlaps_region(self, searchbox, bbox):
        return (searchbox[0] <= bbox[2] and searchbox[1] >= bbox[0] and searchbox[2] <= bbox[3] and searchbox[3] >= bbox[1])
        
        
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "(%f,%f)" % (self.x, self.y)

"""
A vector can be determined from a single point when basing
it from the origin (0,0), but I'm going to assume 2 points.
Example:
    AB = Vector(Point(3,4),Point(6,7))
or if you want to use the origin
    AB = Vector(Point(0,0),Point(8,4))
"""
class Vector(object):
    def __init__(self,p1,p2):
        assert not p1 == None
        assert not p2 == None
        self.p1 = p1
        self.p2 = p2
        self.v = [self.p1.x - self.p2.x, self.p1.y - self.p2.y]
        self.a,self.b = self.v

    def _str__(self):
        return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\nb: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

    def __repr__(self):
        return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\nb: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

"""
VectorOps give the ability to apply some simple movement to an object.
@method: _bearing       -- private method to give the bearing going from p1 -> p2
@method: _magnitude     -- length in this context
@method: _step          -- a "motion vector" (not correct term) to apply to point p1
                           that will "step" it towards p2. The size of the "step" is
                           based on the velocity.
"""
class VectorOps(object):
    def __init__(self,p1=None,p2=None,velocity=1):
        self.p1 = p1
        self.p2 = p2
        self.dx = 0
        self.dy = 0
        if not self.p1 == None and not self.p2 == None:
            self.v = Vector(p1,p2)
            self.velocity = velocity
            self.magnitude = self._magnitude()
            self.bearing = self._bearing()
            self.step = self._step()
        else:
            self.v = None
            self.velocity = None
            self.bearing = None
            self.magnitude = None

    """
    Calculate the bearing (in radians) between p1 and p2
    """
    def _bearing(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        rads = math.atan2(-dy,dx)
        return rads % 2*math.pi         # In radians
        #degs = degrees(rads)
    """
    A vector by itself can have a magnitude when basing it on the origin (0,0),
    but in this context we want to calculate magnitude (length) based on another
    point (converted to a vector).
    """
    def _magnitude(self):
        assert not self.v == None
        return math.sqrt( (self.v.a**2) + (self.v.b**2) )

    """
    Create the step factor between p1 and p2 to allow a point to
    move toward p2 at some interval based on velocity. Greater velocity
    means bigger steps (less granular).
    """
    def _step(self):
        cosa = math.sin(self.bearing)
        cosb = math.cos(self.bearing)
        self.dx = cosa * self.velocity
        self.dy = cosb * self.velocity
        return [cosa * self.velocity, cosb * self.velocity]

    def _str__(self):
        return "[\n vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s\n, step: %s\n]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

    def __repr__(self):
        return "[\n vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s\n, step: %s\n]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

"""
Ball is an extension of a point. It doesn't truly "extend" the point class but it
probably should have! Having said that, I probably should extend the VectorOps class
as well.
@method: destination       -- private method to give the bearing going from p1 -> p2
@method: move              -- length in this context
@method: xInBounds         -- Helper class to check ... I'll let you guess
@method: yInBounds         -- Same as previous just vertically :)
This class is used as follows:
Given a point, p1, I want to move it somewhere, anywhere. So I do the following:
1) Create a random point somewhere else on the screen / world / board:
        distance = 100
        degrees = math.radians(random.randint(0,360))
        p2 = destination(distance,degrees)
2) Now I can calculate a vector between P1 and P2 at a given velocity (scalar value
    to adjust speed)
        velocity = random.randint(1,MaxSpeed) # 1-15 or 20
        vectorOps = VectorOps(p1,p2,velocity)
3) Finally I have a "step" (or incorrectly coined as a motion vector) that as applied to
    p1 will move it toward p2 at the given step.
        p1.x += vectorOps.dx
        p1.y += vectorOps.dy
"""
class Ball():
    def __init__(self, center, radius,velocity=1,color="#000"):
        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.x = center.x
        self.y = center.y
        self.center = center
        self.bearing = math.radians(random.randint(0,360))
        self.dest = self.destination(100,self.bearing)
        self.vectorOps = VectorOps(self.center,self.dest,self.velocity)
        self.color = color

    """
    Given a distance and a bearing find the point: P2 (where we would end up).
    """
    def destination(self,distance,bearing):
        cosa = math.sin(bearing)
        cosb = math.cos(bearing)
        return Point(self.x + (distance * cosa), self.y + (distance * cosb))

    """
    Applies the "step" to current location and checks for out of bounds
    """
    def move(self,bounds):
        x = self.x
        y = self.y

        #Move temporarily
        x += self.vectorOps.dx
        y += self.vectorOps.dy

        #Check if in bounds
        #If it's not, then change direction
        if not self._xInBounds(bounds,x):
            self.vectorOps.dx *= -1
            self._change_bearing(math.pi)
        if not self._yInBounds(bounds,y):
            self.vectorOps.dy *= -1


        # Move any way because If we hit boundaries then we'll
        # go in the other direction.
        self.x += self.vectorOps.dx
        self.y += self.vectorOps.dy

        # Update center value of ball
        self.center.x = self.x
        self.center.y = self.y


    def _xInBounds(self,bounds,x):
        if x >= bounds.maxX or x <= bounds.minX :
            return False

        return True

    def _yInBounds(self,bounds,y):
        if y >= bounds.maxY or y <= bounds.minY:
            return False

        return True

    """
    Change Bearing
    """
    def _change_bearing(self,change):
        self.bearing = (self.bearing + change) % (2 * math.pi)

    def changeSpeed(self,new_velocity):
        self.dest = self.destination(100,self.bearing)
        self.velocity = new_velocity
        self.vectorOps = VectorOps(self.center,self.dest,self.velocity)

    """
    @returns a tuple (x, y)
    """
    def as_tuple(self):
        return (self.x, self.y)


    def _str__(self):
        return "[\n center: %s,\n radius: %s,\n vector: %s,\n speed: %s\n ]" % (self.center,self.radius, self.vectorOps,self.velocity)

    def __repr__(self):
        return "[\n center: %s,\n radius: %s,\n vector: %s,\n speed: %s\n ]" % (self.center, self.radius, self.vectorOps,self.velocity)

"""
A class more or so to put all the boundary values together. Friendlier than
using a map type.
"""
class Bounds(object):
    def __init__(self,minx,miny,maxx,maxy):
        self.minX = minx
        self.minY = miny
        self.maxX = maxx
        self.maxY = maxy
    def __repr__(self):
        return "[%s %s %s %s]" % (self.minX, self.minY, self.maxX,self.maxY)

"""
The driver class that extends the Pantograph class that creates the html 5
canvas animations.
If you run this file from the command line "python visualizeQuadtree.py"
Pantograph will start a local server running at address: http://127.0.0.1:8080
Simply place "http://127.0.0.1:8080" in the address bar of a browser and hit enter.
Dependencies:
    Pantograph:
        pip install pantograph
    Numpy
    Point
    Rectangle
"""
class Driver(pantograph.PantographHandler):

    """
    Sets up canvas, generates balls, etc.
    """
    def setup(self):
        self.bounds = Bounds(0,0,self.width,self.height)
        self.maxvelocity = 10
        self.BallSpeeds = np.arange(1,self.maxvelocity,1)
        self.numBalls = 50
        self.BallSize = 5
        self.halfSize = self.BallSize / 2
        self.qt = quadtree(self.bounds)
        self.Balls = []
        self.Boxes = []
        self.freeze = False
        
        for i in range(self.numBalls):
            ball = Ball(self.getRandomPosition(), self.BallSize, random.choice(self.BallSpeeds), "#F00")
            self.Balls.append(ball)
            self.qt.insertBall(ball)

    """
    Runs the animation.
    """
    def update(self):
        if not self.freeze:
            self.moveBalls()
        self.clear_rect(0, 0, self.width, self.height)
        self.drawBalls()
        self.drawBoxes();
                
    """
    Generate some random point somewhere within the bounds of the canvas.
    """
    def getRandomPosition(self):
        x = random.randint(0+self.BallSize,int(self.width)-self.BallSize)
        y = random.randint(0+self.BallSize,int(self.height)-self.BallSize)
        return Point(x,y)


    """
    Draw the bounding boxes fetched from the quadtree
    """
    def drawBoxes(self):
        boxes = self.qt.getBBoxes()
        for box in boxes:
            self.draw_line(box[0], box[5], box[2], box[5], color = "#000")
            self.draw_line(box[4], box[1], box[4], box[3], color = "#000")

    """
    Draw the balls
    """
    def drawBalls(self):
        for r in self.Balls:
            self.fill_circle(r.x,r.y,r.radius,r.color)
            r.color = "#F00"

    """
    Not Implemented fully. The goal is to use the quadtree to check to see which
    balls collide, then change direction.
    """
    def checkCollisions(self):
        for ball in self.Balls:
            nearballs = self.qt.regionSearch([ball.x-ball.radius-self.maxvelocity, 
                ball.x+ball.radius+self.maxvelocity, ball.y-ball.radius-self.maxvelocity, 
                ball.y+ball.radius+self.maxvelocity], ball)
            for nearball in nearballs:
                nearball.color = "#0F0"
                ball.color = "#0f0"
     
    """
    When a ball has collided with at least one other ball in the last update,
    its radius increases by one. If it has not and its radius is greater
    that self.BallSize, the radius decreases based on the current radius
    """           
    def adjustSizes(self):
        for ball in self.Balls:
            if ball.color == "#0F0":
                ball.radius+=1
            elif ball.radius > self.BallSize:
                ball.radius-=(ball.radius-self.BallSize)*.1

    """
    Moves the balls
    """
    def moveBalls(self):
        newqt = quadtree(self.bounds)
        self.checkCollisions()
        self.adjustSizes()
        for r in self.Balls:
            r.move(self.bounds)
            newqt.insertBall(r)
        self.qt = newqt

    """
    Toggles movement on and off
    """
    def on_click(self,InputEvent):
        if self.freeze == False:
            self.freeze = True
        else:
            self.freeze = False

    """
    up arrow will speed balls up by some factor
    down arrow will slow balls down by same factor
    left arrow will remove a ball
    right arrow will add a ball
    """
    def on_key_down(self,InputEvent):
        # User hits the UP arrow
        if InputEvent.key_code == 38:
            for r in self.Balls:
                r.changeSpeed(r.velocity * 1.25)
        # User hits the DOWN arrow
        if InputEvent.key_code == 40:
            for r in self.Balls:
                r.changeSpeed(r.velocity * 0.75)
        # User hits the LEFT arrow
        if InputEvent.key_code == 37:
            del self.Balls[-1]
            self.numBalls-=1
        # User hits the RIGHT arrow
        if InputEvent.key_code == 39:
            self.Balls.append(Ball(self.getRandomPosition(), self.BallSize, random.choice(self.BallSpeeds), "#F00"))
            self.numBalls+=1

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()      

