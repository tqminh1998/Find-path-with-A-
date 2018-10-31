import sys
import math
import queue
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
        self.track = -1
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
                    self.matNode[i][j].h = heristic_function(Point(i,j), Point(self.gi,self.gj))


#Our heuristic
def heristic_function(p1, p2):
    return math.sqrt(math.fabs(p1.i - p2.i)/2 + math.fabs(p1.j - p2.j)/2)

def AStar(myMap):
    n=len(myMap.matNode)
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
                    
                    myMap.matNode[new_i][new_j] = curNode

                


    return False

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

def printSolution(path, myMap, isFoundPath):
    file_out = open(sys.argv[2], "w")
    if isFoundPath:
        n=len(myMap.matNode)
        cost = len(path)

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
        file_out.write("-1")

    file_out.close()


def main():
    #read input into a matrix
    file_in = open(sys.argv[1],"r")

    n = int(file_in.readline())
    si, sj = list(map(int, file_in.readline().split()))
    gi, gj = list(map(int, file_in.readline().split()))

    # Change x, y coordinate to i, j coordinate
    si, sj = sj, si
    gi, gj = gj, gi

    mat = [] #create matrix
    for i in range(n):
        mat.append(list(map(int,file_in.readline().split())))

    file_in.close()

    #create map
    myMap = Map()
    myMap.create(n,mat,si,sj,gi,gj)

    isFoundPath = AStar(myMap)
    path = tracking(myMap)

    printSolution(path, myMap, isFoundPath)
    


if __name__ == '__main__':
    main()
