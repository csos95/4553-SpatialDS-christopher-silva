"""
@author - Christopher Silva
@date -  10/18/2015
@description - This program displays moving balls on a html canvas and uses
a quadtree to assist in collision detection
"""
import random
import math
import numpy
import pantograph

"""
The node class holds an item, the x and y of the item, and a bbox for the item
"""
class node:
    def __init__(self, x, y, item, bbox):
        self.x = x
        self.y = y
        self.item = item
        self.bbox = bbox
        self.children = [None, None, None, None]

    """
    Returns a string representation of the node
    """
    def __str__(self):
        return "node at (%f,%f) containing %s" % (self.x, self.y, self.item)

"""
Stores nodes in a quadtree structure and includes the usual quadtree methods
such as insert, traverse, and region search
"""
class quadtree:
    def __init__(self, bounds):
        self.root = None
        self.bbox = [bounds.minX, bounds.minY, bounds.maxX, bounds.maxY]

    """
    Public method that inserts a ball into the quadtree
    """
    def insertBall(self, ball):
        newnode = node(ball.x, ball.y, ball, self.bbox)
        if self.root == None:
            self.root = newnode
        else:
            self._insert(self.root, newnode)

    """
    Public method that inserts a generic item into the quadtree
    """
    def insert(self, x, y, item):
        newnode = node(x, y, item, self.bbox)
        if self.root == None:
            self.root = newnode
        else:
            self._insert(self.root, newnode)

    """
    Private insertion method
    it goes down the quadtree until it finds the appropriate place to insert
    the node and then does so
    """
    def _insert(self, subroot, node):
        direction = self._compare(subroot, node)
        while subroot.children[direction] != None:
            subroot = subroot.children[direction]
            direction = self._compare(subroot, node)
        if direction == 0:
            node.bbox = [subroot.x, subroot.y, subroot.bbox[2], subroot.bbox[3]]
        elif direction == 1:
            node.bbox = [subroot.x, subroot.bbox[1], subroot.bbox[2], subroot.y]
        elif direction == 2:
            node.bbox = [subroot.bbox[0], subroot.bbox[1], subroot.x, subroot.y]
        elif direction == 3:
            node.bbox = [subroot.bbox[0], subroot.y, subroot.x, subroot.bbox[3]]
        subroot.children[direction] = node

    """
    Private method that compares two nodes and returns which direction
    the second node is in relation to the first
    """
    def _compare(self, node1, node2):
        if node2.x >= node1.x and node2.y >= node1.y:
                return 0
        elif node2.x <= node1.x and node2.y <= node1.y:
                return 2
        elif node2.x > node1.x:
                return 1
        elif node2.y > node1.y:
                return 3

    """
    Public traversal method that calls the private one
    """
    def traversal(self):
        self._traversal(self.root)

    """
    Private traversal method that does through the quadtree and prints the
    string representation of each node
    """
    def _traversal(self, subroot):
        if subroot == None:
            return
        print subroot
        self._traversal(subroot.children[0])
        self._traversal(subroot.children[1])
        self._traversal(subroot.children[2])
        self._traversal(subroot.children[3])

    """
    Private method that calls the private method and returns a list of the
    bounding boxes of all nodes
    """
    def getBBoxes(self):
        return self._getBBoxes(self.root)

    """
    Private method that goes through the quadtree and appends each nodes
    bounding box to a list that is returned
    """
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

    """
    Public method that calls the private method and returns a list of found nodes
    """
    def regionSearch(self, bbox, searchnode):
        return self._regionSearch(self.root, bbox, searchnode)

    """
    Private method that does a region search on the quadtree using a bounding
    box as the search criteria
    """
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

    """
    Private method that returns true or false depending on whether or not a
    node is within the search box
    """
    def _inRegion(self, node, searchbox):
        return (node.x >= searchbox[0] and node.x <= searchbox[1] and node.y >= searchbox[2] and node.y <= searchbox[3])

    """
    Private method that returns true or false depending on whether or not the
    bounding box is within the search box
    """
    def _rectangle_overlaps_region(self, searchbox, bbox):
        return (searchbox[0] <= bbox[2] and searchbox[1] >= bbox[0] and searchbox[2] <= bbox[3] and searchbox[3] >= bbox[1])

"""
Stores the x and y value as a point
"""
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    """
    returns a string representation of the point
    """
    def __str__(self):
        return "A point at (%f,%f)" % (self.x, self.y)

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
A point that has radius, color, velocity, and stays within the screen bounds
"""
class BouncingPoint:
    def __init__(self, point, xvel, yvel, radius, color):
        self.x = point.x
        self.y = point.y
        self.xvel = xvel#random.randint(-4, 5)
        self.yvel = yvel#random.randint(-4, 5)
        self.radius = radius
        self.color = color

    """
    updates the position of the BouncingPoint
    """
    def update(self, canvas):
        if self.x-self.radius <= 0 or self.x+self.radius >= canvas.width:
            self.xvel *= -1
            self.x += self.xvel
            self.y += self.yvel
        if self.y-self.radius <= 0 or self.y+self.radius >= canvas.height:
            self.yvel *= -1
            self.x += self.xvel
            self.y += self.yvel

        self.x += self.xvel
        self.y += self.yvel

    """
    multiplies the velocity of the ball
    """
    def multiplySpeed(self, multiplicity):
        self.xvel = self.xvel * multiplicity
        self.yvel = self.yvel * multiplicity

"""
The driver class that extends the Pantograph class that creates the html 5
canvas animations.
If you run this file from the command line "python collision.py"
Pantograph will start a local server running at address: http://127.0.0.1:8080
Simply place "http://127.0.0.1:8080" in the address bar of a browser and hit enter.
Dependencies:
    Pantograph:
        pip install pantograph
    Numpy
"""
class Driver(pantograph.PantographHandler):

    """
    Sets up canvas, generates balls, etc.
    """
    def setup(self):
        self.bounds = Bounds(0,0,self.width,self.height)
        self.GrowthAmount = 1
        self.maxvelocity = 10
        self.numBalls = 250
        self.maxBallSize = 100
        self.BallSize = 5
        self.halfSize = self.BallSize / 2
        self.BallSpeeds = numpy.arange(-self.maxvelocity,self.maxvelocity+1,1)
        self.BallSpeeds = numpy.delete(self.BallSpeeds, self.maxvelocity)
        self.qt = quadtree(self.bounds)
        self.Balls = []
        self.Boxes = []
        self.BallColor = "#F00"
        self.freeze = False
        self.showBoxes = True
        self.BallShrink = True

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
    For each ball a region search is done on the quadtree using a bounding box around the
    ball that is twice as big as the max velocity and then for each returned ball
    a simple collision is used (is the distance between balls thess than the sum of their radius)
    to detect if they will collide in the next update and if they will they are changed to
    green(to mark they will collide for the adjustSize method) and their velocities are swapped
    """
    def checkCollisions(self):
        for ball in self.Balls:
            nearballs = self.qt.regionSearch([ball.x-self.maxBallSize-self.maxvelocity,
                ball.x+self.maxBallSize+self.maxvelocity, ball.y-self.maxBallSize-self.maxvelocity,
                ball.y+self.maxBallSize+self.maxvelocity], ball)
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
                ball.radius+=self.GrowthAmount
                if ball.radius > self.maxBallSize:
                    del self.Balls[self.Balls.index(ball)]
            elif ball.radius > self.BallSize and self.BallShrink:
                ball.radius-=(ball.radius-self.BallSize)*.1

    """
    Draw the balls
    """
    def drawBalls(self):
        for r in self.Balls:
            self.fill_circle(r.x,r.y,r.radius,r.color)
            #self.draw_circle(r.x,r.y,r.radius,"#000")
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
    shift changes the grow/shrink mode
    space turns drawboxes on/off
    up arrow will speed balls up by some factor
    down arrow will slow balls down by same factor
    left arrow will remove a ball
    right arrow will add a ball
    """
    def on_key_down(self,InputEvent):
        # User hits shift
        if InputEvent.key_code == 16:
            if self.BallShrink:
                self.BallShrink = False
                self.GrowthAmount = .1
            else:
                self.BallShrink = True
                self.GrowthAmount = 1
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
