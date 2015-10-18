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

class BouncingPoint:
    """initializes the values for the bouncing shape"""
    def __init__(self, point, xvel, yvel, radius, color):
        self.x = point.x
        self.y = point.y
        self.xvel = xvel#random.randint(-4, 5)
        self.yvel = yvel#random.randint(-4, 5)
        self.radius = radius
        self.color = color

    """updates the position of the BouncingPoint"""
    def update(self, canvas):
        if self.x+self.radius <= 0 or self.x+self.radius >= canvas.width:
            self.xvel *= -1
            self.x += self.xvel
            self.y += self.yvel
        if self.y+self.radius <= 0 or self.y+self.radius >= canvas.height:
            self.yvel *= -1
            self.x += self.xvel
            self.y += self.yvel
        
        self.x += self.xvel
        self.y += self.yvel
        
    def multiplySpeed(self, multiplicity):
        self.xvel = self.xvel * multiplicity
        self.yvel = self.yvel * multiplicity

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
        self.numBalls = 200
        self.maxBallSize = 100
        self.BallSize = 5
        self.halfSize = self.BallSize / 2
        self.BallSpeeds = np.arange(-self.maxvelocity,self.maxvelocity+1,1)
        self.BallSpeeds = np.delete(self.BallSpeeds, self.maxvelocity)
        self.qt = quadtree(self.bounds)
        self.Balls = []
        self.Boxes = []
        self.BallColor = "#F00"
        self.freeze = False
        self.showBoxes = True
        
        for i in range(self.numBalls):
            ball = BouncingPoint(self.getRandomPosition(), random.choice(self.BallSpeeds), random.choice(self.BallSpeeds), self.BallSize, "#F00")
            self.Balls.append(ball)
            self.qt.insertBall(ball)
                
    """
    Generate some random point somewhere within the bounds of the canvas.
    """
    def getRandomPosition(self):
        x = random.randint(0+self.BallSize,int(self.width)-self.BallSize)
        y = random.randint(0+self.BallSize,int(self.height)-self.BallSize)
        return Point(x,y)

    """
    Runs the animation.
    """
    def update(self):
        if not self.freeze:
            self.moveBalls()
        self.clear_rect(0, 0, self.width, self.height)
        self.drawBalls()
        if self.showBoxes:        
            self.drawBoxes();

    """
    Moves the balls
    """
    def moveBalls(self):
        newqt = quadtree(self.bounds)
        self.checkCollisions()
        self.adjustSizes()
        for r in self.Balls:
            r.update(self)  
            newqt.insertBall(r)
        self.qt = newqt

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
                if (math.pow((nearball.x+nearball.xvel) - (ball.x+ball.xvel), 2) + 
                        math.pow((nearball.y+nearball.yvel) - (ball.y+ball.yvel), 2) <= 
                        math.pow(nearball.radius + ball.radius, 2)):
                    nearball.color = "#0F0"
                    ball.color = "#0F0"
                    xveltmp = ball.xvel
                    yveltmp = ball.yvel
                    ball.xvel = nearball.xvel
                    ball.yvel = nearball.yvel
                    nearball.xvel = xveltmp
                    nearball.yvel = yveltmp
     
    """
    When a ball will collide with at least one other ball in the next frame,
    its radius increases by one. If it has not and its radius is greater
    that BallSize, the radius decreases based on the current radius
    If the radius is larger than the maxBallSize, the ball "pops"
    """  
    def adjustSizes(self):
        for ball in self.Balls:
            if ball.color == "#0F0":
                ball.radius+=1
                if ball.radius > self.maxBallSize:
                    del self.Balls[self.Balls.index(ball)]
            elif ball.radius > self.BallSize:
                ball.radius-=(ball.radius-self.BallSize)*.1

    """
    Draw the balls
    """
    def drawBalls(self):
        for r in self.Balls:
            self.fill_circle(r.x,r.y,r.radius,r.color)
            self.draw_circle(r.x,r.y,r.radius,"#000")
            r.color = self.BallColor


    """
    Draw the bounding boxes fetched from the quadtree
    """
    def drawBoxes(self):
        boxes = self.qt.getBBoxes()
        for box in boxes:
            self.draw_line(box[0], box[5], box[2], box[5], color = "#000")
            self.draw_line(box[4], box[1], box[4], box[3], color = "#000")

    """
    Toggles movement on and off
    """
    def on_click(self,InputEvent):
        if self.freeze == False:
            self.freeze = True
        else:
            self.freeze = False

    """
    space turns drawboxes on/off
    up arrow will speed balls up by some factor
    down arrow will slow balls down by same factor
    left arrow will remove a ball
    right arrow will add a ball
    """
    def on_key_down(self,InputEvent):
        # User hits the space bar
        if InputEvent.key_code == 32:
            if self.showBoxes:
                self.showBoxes = False
            else:
                self.showBoxes = True
        # User hits the UP arrow
        if InputEvent.key_code == 38:
            for r in self.Balls:
                r.multiplySpeed(1.25)
        # User hits the DOWN arrow
        if InputEvent.key_code == 40:
            for r in self.Balls:
                r.multiplySpeed(0.75)
        # User hits the LEFT arrow
        if InputEvent.key_code == 37:
            del self.Balls[-1]
            self.numBalls-=1
        # User hits the RIGHT arrow
        if InputEvent.key_code == 39:
            self.Balls.append(BouncingPoint(self.getRandomPosition(), random.choice(self.BallSpeeds), random.choice(self.BallSpeeds), self.BallSize, "#F00"))
            self.numBalls+=1

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()      

