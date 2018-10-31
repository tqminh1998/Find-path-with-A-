#argument
import sys
import math
import queue
import time

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

def improvePath(myMap, OPEN, INCONS, CLOSED, list_of_tracktable):
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
                    else:
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




def ARA(myMap, tmax, ep, ep_decrease):
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
    isFoundBetterPath = improvePath(myMap, OPEN, INCONS, CLOSED, list_of_tracktable)
    

    path = tracking(myMap)
    first_print = True #To print to new file at the first time writing path
    printSolution(path, myMap, isFoundBetterPath, first_print, myMap.ep)
    first_print = False

    timeout = time.time() + tmax
    while time.time() < timeout and myMap.ep - 1 > 0.000001:
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
        isFoundBetterPath = improvePath(myMap, OPEN, INCONS, CLOSED, list_of_tracktable)
        #print solution

        path = tracking(myMap)
        printSolution(path, myMap, isFoundBetterPath, first_print, myMap.ep)
        

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

def printSolution(path, myMap, isFoundBetterPath, first_print, ep):
    file_type = ""
    if first_print:
        file_type = "w"
    else:
        file_type = "a"

    file_out = open(sys.argv[2], file_type)
    file_out.write("Epsilon: ")
    file_out.write(str(ep))
    file_out.write("\n")

    if isFoundBetterPath:
        n=len(myMap.matNode)
        cost = len(path)

        if cost:
            # set up display matrix
            display_mat = [['-' for i in range(n)] for j in range(n)]
            for i in range(n):
                for j in range(n):
                    if myMap.matNode[i][j].isObstacle == True:
                        display_mat[i][j] = 'o'

            # set path for display matrix
            for i in range(len(path)):
                display_mat[path[i][1]][path[i][0]] = 'x'


            display_mat[myMap.si][myMap.sj] = 'S'
            display_mat[myMap.gi][myMap.gj] = 'G'

            #print to file
            file_out.write(str(cost))
            file_out.write("\n")
            str_path = str(path)
            file_out.writelines(str_path[1:len(str_path)-1])
            file_out.write("\n")

            for i in range(n):
                for j in range(n):
                    file_out.write(display_mat[i][j])
                    file_out.write(" ")
                file_out.write("\n")

            file_out.write("\n")
        else:
            file_out.write("Khong tim thay duong di\n\n")

    else:
        file_out.write("Khong tim thay duong di tot hon\n\n")

    file_out.close()


def main():
    #read input into a matrix
    file_in = open(sys.argv[1],"r")

    n = int(file_in.readline())
    si, sj = list(map(int, file_in.readline().split()))
    gi, gj = list(map(int, file_in.readline().split()))

    si, sj = sj, si
    gi, gj = gj, gi

    mat = [] #create matrix
    for i in range(n):
        mat.append(list(map(int,file_in.readline().split())))

    file_in.close()

    #create map
    myMap = Map()

    myMap.create(n,mat,si,sj,gi,gj)
    print("Nhap thoi gian tmax: ")
    tmax = float(input())
    print("Nhap epsilon: ")
    ep = float(input())
    print("Nhap do giam epsilon: ")
    ep_decrease = float(input())

    ARA(myMap, tmax, ep, ep_decrease)


if __name__ == '__main__':
    main()
