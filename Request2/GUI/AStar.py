#argument
import sys
import math
import queue
import GUI as gui
import time

class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

class Node:
    def __init__(self,pos,h,g,value):
        self.pos = pos
        self.h = h
        self.g = g
        self.visited = False
        self.track = 0
        self.value = value
        self.isObstacle = False
        if self.value == 1:
            self.isObstacle = True
    def __lt__(self, other):
        return float(self.g + self.h) <= float(other.g + other.h)

class Map:
    def __init__(self):
        self.matNode = []
        self.si=self.sj=self.gi=self.gj=0
    def create(self, n, mat,si,sj,gi,gj):    
        self.matNode = [[Node(Point(i,j),0,0,mat[i][j]) for j in range(n)] for i in range(n)]

        self.si = si
        self.sj = sj
        self.gi = gi
        self.gj = gj

        #count heuristic
        for i in range(n):
            for j in range(n):
                if mat[i][j] != 1:
                    self.matNode[i][j].h = euclidean_distance(Point(i,j), Point(self.gi,self.gj))


def euclidean_distance(p1, p2):
    return math.sqrt((p1.i - p2.i)**2 + (p1.j - p2.j)**2)

#Our heuristic
def heristic_function(p1, p2):
    return math.sqrt(math.fabs(p1.i - p2.i)/2 + math.fabs(p1.j - p2.j)/2)

def computeHeuristic(myMap, str_type, gi, gj):
    n = len(myMap.matNode)
    if str_type == "A* euclidean":
        for i in range(n):
            for j in range(n):
                myMap.matNode[i][j].h = euclidean_distance(Point(i,j), Point(gi,gj))
    else:
        for i in range(n):
            for j in range(n):
                myMap.matNode[i][j].h = heristic_function(Point(i,j), Point(gi,gj))

    

def AStar(myMap, appGui):
    n=len(myMap.matNode)
    computeHeuristic(myMap, appGui.str_algo, myMap.gi, myMap.gj)
    pq = queue.PriorityQueue()
    pq.put(myMap.matNode[myMap.si][myMap.sj])
    myMap.matNode[myMap.si][myMap.sj].visited = True

    while pq.empty() == False:
        top = pq.get()
        pos = top.pos
        g = top.g

        if pos.i == myMap.gi and pos.j == myMap.gj:
            return True
        else:
            di = [-1,-1,-1, 0, 1, 1, 1, 0]
            dj = [-1, 0, 1, 1, 1, 0,-1,-1]

            for k in range(8):
                new_i = pos.i+di[k]
                new_j = pos.j+dj[k]
                
                if new_i < n and new_i >= 0 and new_j < n and new_j >= 0 and myMap.matNode[new_i][new_j].isObstacle == False:
                    curNode = myMap.matNode[new_i][new_j]
                    if curNode.visited==False:
                        curNode.g = float(math.inf)
                    if curNode.g > g+1:
                        curNode.g=g+1
                        curNode.visited = True
                        curNode.track = k
                        pq.put(curNode)
                        if appGui.canvas.itemcget(appGui.grid[new_i][new_j],"fill") != 'red':
                            appGui.canvas.itemconfigure(appGui.grid[new_i][new_j], fill = 'white')
                        time.sleep(0.03)
                        appGui.canvas.update()
                    
                    myMap.matNode[new_i][new_j] = curNode


    return False