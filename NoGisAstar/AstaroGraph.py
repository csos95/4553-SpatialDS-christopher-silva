#Christopher Silva
#date 12/6/2015
# This program performs an A* Pathfinding algorithm on a grid of tiles
#with varying movement costs in an attempt ot find a path between
#a start and end point. If it is successfull it displays the path

#controls 
#keys 1-3 - select tile type
#    1 = wall
#    2 = sand
#    3 = water
#space - perform a search for a path with space
#p - change path display mode with pantograph
#    the default is to just show the path
#    the second mode shows an animation of the path search
#enter - creates a random grid of tiles with a start in
#    the top left and the end in bottom right

#movement costs
#brown(dirt) = 1, yellow(sand) = 2, blue(water) = 3, black(wall) = -1(can't move there)

#resources - starting A* code taken from http://www.redblobgames.com/pathfinding/a-star/implementation.html

from random import randint
from itertools import product
import pantograph
import math
import heapq

#a sorted queue, used for getting the best next move
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def isEmpty(self):
        return len(self.elements) == 0
    
    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.elements)[1]

#euclidean distance - for some reason the search path
#comes out looking like a breadth first search everytime
#so not good to use if showing the full pathing(slow to draw it all)
def heuristic1(a, b):
    x1,y1 = a
    x2,y2 = a
    return abs(x1 - x2) + abs(y1 - y2)
#manhattan distance
#looks much better if showing the full pathing(not as slow)
def heuristic2(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return math.sqrt((dx*dx)+(dy*dy))

#the move cost is just an int 1-3
def cost(grid, next):
    return grid[next[0]][next[1]]

#performs the A* search on a grid
def a_star_search(grid, start, end):
    path_order = [start]
    open = PriorityQueue()
    open.push(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    #while there is still a move to make
    while not open.isEmpty():
        #get next move
        current = open.pop()

        #add it to path_order
        path_order.append(current)
        
        #if it is the end stop, you've found a path
        if current == end:
            break
        
        #otherwise check neighbors for possible next moves
        for next in neighbors(grid, current):
            #if the neighbor isn't a wall continue checking it
            if grid[next[0]][next[1]] != -1:
                #calculate the cost of it
                new_cost = cost_so_far[current] + cost(grid, next)
                #if that spot hasn't already been checked or this is a lower 
                #cost way, add it as a possible next move and update values
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic2(end, next)
                    open.push(next, priority)
                    came_from[next] = current
    #create the path
    path = []
    #if a path was found, use came_from to put it in path
    if end in came_from:
        previous_step = came_from[end]
        path.append(end)
        while previous_step != None:
            path.append(previous_step)
            previous_step = came_from[previous_step]
        path.reverse()
    
    return path,path_order

#finds neighbors that are within the grid
def neighbors(grid, current):
    size = (len(grid), len(grid[0]))
    neighbors = []
    if current[0] > 0:
        neighbors.append((current[0]-1, current[1]))
    if current[0] < size[0]-1:
        neighbors.append((current[0]+1, current[1]))
    if current[1] > 0:
        neighbors.append((current[0], current[1]-1))
    if current[1] < size[1]-1:
        neighbors.append((current[0], current[1]+1))
    return neighbors

#The main driver
class Driver(pantograph.PantographHandler):
    def setup(self):
        self.blocksize = 40
        self.h = int(self.height/self.blocksize)
        self.w = int(self.width/self.blocksize)
        self.tiles = {}
        self.start = None
        self.end = None
        self.path = None
        self.currtile = 1
        self.tilecolors = ["fff", "#960", "#ff0", "#00f", "#000"]
        self.path_order = None
        self.path_so_far = []
        self.drawingPath = False
        self.currentStep = 0
        self.drawpath = False
        self.grid = []
        for x in range(0,self.w):
            self.grid.append([])
            for y in range(0,self.h):
                self.grid[x].append(1)
    
    #update method is called every frame
    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        self.drawTiles()
        self.drawGrid()
        if self.drawingPath and self.drawpath:
            self.drawPathing()
        elif self.path:
            self.drawPath()
            
    #draw the grid
    def drawGrid(self):
        for i in range(0,self.w*self.blocksize, self.blocksize):
           self.draw_line(i, 0, i, self.h*self.blocksize, "#AAAAAA")
           self.draw_line(0, i, self.w*self.blocksize, i , "#AAAAAA")
       
    #draw all of the tiles    
    def drawTiles(self):
        for x in range(0, self.w):
            for y in range(0, self.h):
                self.fill_rect(x*self.blocksize, y*self.blocksize, self.blocksize, self.blocksize, self.tilecolors[self.grid[x][y]])
        if self.start:
            self.fill_rect(self.start[0]*self.blocksize, self.start[1]*self.blocksize, self.blocksize, self.blocksize, "#0f0")
        if self.end:
            self.fill_rect(self.end[0]*self.blocksize, self.end[1]*self.blocksize, self.blocksize, self.blocksize, "#f00")
    
    #draw the pathing       
    def drawPathing(self):
        #if the currentStep is not the start location, add it to the path_so_far
        if self.path_order[self.currentStep] != self.start:
            self.path_so_far.append(self.path_order[self.currentStep])
        #draw the path_so_far
        for step in self.path_so_far:
            self.fill_rect(step[0]*self.blocksize, step[1]*self.blocksize, self.blocksize, self.blocksize, "#f00")
        #if at the end, stop drawing the pathing
        if self.currentStep == len(self.path_order) - 1:
            self.drawingPath = False
        #else, increment the step number
        else:
            self.currentStep+=1
    
    #draw the path
    def drawPath(self):
        for step in self.path[1:-1]:
            if step != self.start:
                self.draw_rect(step[0]*self.blocksize, step[1]*self.blocksize, self.blocksize, self.blocksize, "#f00")
            
    def on_mouse_down(self,e):
        x,y = (int(e.x/self.blocksize),int(e.y/self.blocksize))
        #reset values
        self.path = None
        self.path_order = None
        self.drawingPath = False
        self.currentStep = 0
        self.path_so_far = []
        #if no modifier keys are held, place tile or remove if 
        #there is already a tile of the same type
        if not e.alt_key and not e.ctrl_key and not e.shift_key:
            if (x*self.blocksize,y*self.blocksize) != self.start and (x*self.blocksize,y*self.blocksize) != self.end:
                if (x*self.blocksize,y*self.blocksize) in self.tiles and self.tiles[(x*self.blocksize,y*self.blocksize)] == self.currtile:
                    self.grid[x][y] = 1
                    del self.tiles[(x*self.blocksize,y*self.blocksize)]
                else:
                    if self.currtile == 4:
                        self.grid[x][y] = -1
                    else:
                        self.grid[x][y] = self.currtile
                    self.tiles[(x*self.blocksize,y*self.blocksize)] = self.currtile
                
        elif e.ctrl_key:
            self.grid[x][y] = 1
            self.start = (x,y)
        elif e.alt_key:
            self.grid[x][y] = 1
            self.end = (x,y)
            
    def on_key_down(self,e):
        #keys 1-3
        if e.key_code == 49:
            self.currtile = 4
        elif e.key_code == 50:
            self.currtile = 2
        elif e.key_code == 51:
            self.currtile = 3
        #space
        elif e.key_code == 32:
            if self.start and self.end:
                self.path,self.path_order = a_star_search(self.grid, self.start, self.end)
                if len(self.path) > 0:
                    self.drawingPath = True
        #p
        elif e.key_code == 80:
            if self.drawpath:
                self.drawpath = False
            else:
                self.drawpath = True
        #enter
        elif e.key_code == 13:
            #reset values
            self.path = None
            self.path_order = None
            self.drawingPath = False
            self.currentStep = 0
            self.path_so_far = []
            self.tiles = {}
            self.grid = []
            
            #create a new grid with random tiles
            for x in range(0, self.w):
                self.grid.append([])
                for y in range(0, self.h):
                    value = randint(1,20)
                    if value > 1 and value < 5:
                        if value == 4:
                            self.grid[x].append(-1)
                        else:
                            self.grid[x].append(value)
                        self.tiles[(x*self.blocksize,y*self.blocksize)] = value
                    else:
                        self.grid[x].append(1)
            self.start = (0,0)
            self.end = (int(self.width/self.blocksize)-1,int(self.height/self.blocksize)-1)
                
"""
Main Driver!!!
"""
if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
