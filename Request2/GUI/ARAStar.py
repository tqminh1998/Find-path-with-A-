#argument
import sys
import math
import queue
import time
import GUI as gui

class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

class Node:
    def __init__(self,pos,h,g,ep,value):
        self.pos = pos
        self.h = h
        self.g = g
        self.ep = ep
        self.visited = False
        self.track = -1
        self.value = value
        self.isObstacle = False
        if self.value == 1:
            self.isObstacle = True
    def __lt__(self, other):
        return float(self.g + self.ep*self.h) <= float(other.g + self.ep*other.h)

class Map:
    def __init__(self):
        self.matNode = []
        self.si=self.sj=self.gi=self.gj=0
        self.ep = 5.0
    def create(self, n, mat,si,sj,gi,gj):    
        self.matNode = [[Node(Point(i,j),0,0,self.ep,mat[i][j]) for j in range(n)] for i in range(n)]

        self.matNode[gi][gj].g = float(math.inf)
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

def largerXorY(p1, p2):
    if abs(p1.i - p2.i) > abs(p1.j - p2.j):
        return abs(p1.i - p2.i)
    
    return abs(p1.j - p2.j)

def fvalue(g, h, ep):
    return g + ep*h

def improvePath(myMap, OPEN, INCONS, CLOSED, list_of_tracktable, appGui):
    n=len(myMap.matNode)
    goal = myMap.matNode[myMap.gi][myMap.gj]
    
    minOPEN = None
    if OPEN.empty() == False:
        minOPEN = OPEN.queue[0]

    while minOPEN != None and fvalue(goal.g, goal.h, goal.ep) > fvalue(minOPEN.g, minOPEN.h, minOPEN.ep):
        s = OPEN.get()
        CLOSED.append(myMap.matNode[s.pos.i][s.pos.j])

        pos = s.pos
        g = s.g

        di = [-1,-1,-1, 0, 1, 1, 1, 0]
        dj = [-1, 0, 1, 1, 1, 0,-1,-1]

        for k in range(8):
            new_i = pos.i + di[k]
            new_j = pos.j + dj[k]
            if new_i < n and new_i >= 0 and new_j < n and new_j >= 0  and myMap.matNode[new_i][new_j].isObstacle == False:
                curNode = myMap.matNode[new_i][new_j]
                if curNode.visited==False:
                    curNode.g = float(math.inf)
                if curNode.g > g+1:
                    curNode.g=g+1
                    curNode.visited = True
                    curNode.track = k
                    if curNode not in CLOSED:
                        OPEN.put(curNode)
                        if appGui.canvas.itemcget(appGui.grid[new_i][new_j],"fill") != 'red':
                            appGui.canvas.itemconfigure(appGui.grid[new_i][new_j], fill = 'white')
                        time.sleep(0.05)
                        appGui.canvas.update()
                    else:
                        if appGui.canvas.itemcget(appGui.grid[new_i][new_j],"fill") != 'red':
                            appGui.canvas.itemconfigure(appGui.grid[new_i][new_j], fill = 'blue')
                        time.sleep(0.05)
                        appGui.canvas.update()                        
                        INCONS.put(curNode)
                
                myMap.matNode[new_i][new_j] = curNode
        
        if OPEN.empty() == False:
            minOPEN = OPEN.queue[0]
        else:
            break

    track_table = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            track_table[i][j] = myMap.matNode[i][j].track

    if track_table not in list_of_tracktable:
        list_of_tracktable.append(track_table)
        return True

    return False


def ARA(myMap, ep, ep_decrease, appGui):
    n = len(myMap.matNode)
    #init epsilon
    myMap.ep = ep
    
    for i in range(n):
        for j in range(n):
            myMap.matNode[i][j].ep = myMap.ep
    
    #init OPEN, INCONS, CLOSED
    OPEN = queue.PriorityQueue()
    INCONS = queue.PriorityQueue()
    CLOSED = []

    OPEN.put(myMap.matNode[myMap.si][myMap.sj])
    
    list_of_tracktable = [] #List of track table by epsilon
    isFoundBetterPath = improvePath(myMap, OPEN, INCONS, CLOSED, list_of_tracktable, appGui)
    

    path = tracking(myMap)
    first_print = True #To print to new file at the first time writing path
    printSolution(path, myMap, isFoundBetterPath, first_print, myMap.ep, appGui)
    first_print = False


    while myMap.ep - 1 > 0:
        #decrease ep
        myMap.ep -= ep_decrease
        
        for i in range(n):
            for j in range(n):
                myMap.matNode[i][j].ep = myMap.ep

        #move state from Incons to OPEN
        while OPEN.empty() == False:
            INCONS.put(OPEN.get())

        while INCONS.empty() == False:
            state = INCONS.get()
            state.ep = myMap.ep
            OPEN.put(state)

        
        #Empty closed
        CLOSED = []

        #improve path    
        isFoundBetterPath = improvePath(myMap, OPEN, INCONS, CLOSED, list_of_tracktable, appGui)
        #print solution

        path = tracking(myMap)
        printSolution(path, myMap, isFoundBetterPath, first_print, myMap.ep, appGui)

        

def tracking(myMap):
    path = []

    i = myMap.gi
    j = myMap.gj

    if myMap.matNode[i][j].track == -1:
        return path

    di = [-1,-1,-1, 0, 1, 1, 1, 0]
    dj = [-1, 0, 1, 1, 1, 0,-1,-1]

    path.append((j,i))
    while i != myMap.si or j != myMap.sj:
        k = myMap.matNode[i][j].track
        i -= di[k]
        j -= dj[k]
        path.append((j, i))

    path.reverse()

    return path

def printSolution(path, myMap, isFoundBetterPath, first_print, ep, appGui):
    n = len(myMap.matNode)
    
    if isFoundBetterPath:
        cost = len(path)
        for i in range(n):
            for j in range(n):
                if appGui.canvas.itemcget(appGui.grid[i][j],"fill") == 'yellow':
                    appGui.canvas.itemconfig(appGui.grid[i][j], fill = 'white')

        if cost:
            for i in range(1,cost-1,1):
                appGui.canvas.itemconfigure(appGui.grid[path[i][1]][path[i][0]], fill = 'yellow')
            appGui.canvas.update()
            time.sleep(1.5)
            
        else:
            gui.messagebox.showinfo("Message", "No path!")


