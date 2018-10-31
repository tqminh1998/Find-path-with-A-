import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import AStar as algo
import ARAStar as ara

class MainMenu:
    def __init__(self):
        self.menuGUI = tk.Tk()
        self.menuGUI.geometry('300x300')
        self.menuGUI.title('Menu')

        #label size
        self.lbSize = tk.Label(self.menuGUI, text = 'Size: ')
        self.lbSize.place(x = 0, y = 0)
        
        #combo box size
        self.gridSize = tk.StringVar()
        self.comboSize = ttk.Combobox(self.menuGUI, width = 10, textvariable = self.gridSize)
        self.comboSize['values'] = ("15", "30", "60")
        self.comboSize.place(x = 100,  y = 0)


        # coordinate text
        self.lbStart = tk.Label(self.menuGUI, text = 'Toa do bat dau')
        self.lbStart.place(x=0,y=20)
        self.lbGoal = tk.Label(self.menuGUI, text = 'Toa do dich')
        self.lbGoal.place(x = 0, y = 40)
        self.txtStart = tk.Text(self.menuGUI, height = 1, width = 10)
        self.txtStart.place(x=100,y=20)

        self.txtGoal = tk.Text(self.menuGUI, height = 1, width = 10)
        self.txtGoal.place(x=100,y=40)

        #label algo
        self.lbAlgo = tk.Label(self.menuGUI, text = 'Algorithm: ')
        self.lbAlgo.place(x = 0, y = 60)

        # type of algo
        self.type_of_algo = tk.StringVar()
        self.comboAlgo = ttk.Combobox(self.menuGUI, width = 20, textvariable = self.type_of_algo)
        self.comboAlgo['values'] = ("A* euclidean", "A* our heuristic", "ARA*")
        self.comboAlgo.place(x = 100,  y = 60)

        #start button
        self.btnStart = tk.Button(self.menuGUI, text = 'Start', command = self.Start)
        self.btnStart.place(x=0,y=80)



    def Run(self):
        self.menuGUI.mainloop()

    def checkInput(self, str, gridSize):
        cnt = 0
        for c in str:
            if c.isdigit() == False and c != ' ':
                return False
            if c == ' ':
                cnt +=1
        
        flag = False
        if cnt == 1:
            a, b = map(int, str.split())

            if 0 <= a < gridSize and 0 <= b < gridSize:
                flag = True
            
        return flag
        

    def Start(self):
        str_gridSize = self.gridSize.get()
        gridSize = int(str_gridSize)

        str_algo = self.type_of_algo.get()
        
        str_startxy = self.txtStart.get("1.0",'end-1c')
        str_goalxy = self.txtGoal.get("1.0",'end-1c')
        if self.checkInput(str_goalxy, gridSize) and self.checkInput(str_startxy, gridSize):
            si, sj = list(map(int, str_startxy.split()))
            gi, gj = list(map(int, str_goalxy.split()))

            si, sj = sj, si
            gi, gj = gj, gi
            
            startNode = algo.Node(algo.Point(si,sj), 0, 0, 0)
            goalNode = algo.Node(algo.Point(gi,gj),0,0,0)

            app = AppGUI(startNode, goalNode, gridSize, str_algo) 
        else:
            messagebox.showinfo("Warning", "Invalid coordinate")

    

class AppGUI:
    def __init__(self, startNode, goalNode, gridSize, str_algo):
        # init param
        self.startNode = startNode
        self.goalNode = goalNode
        self.gridSize = gridSize
        self.str_algo = str_algo

        #create app gui
        self.mapGui = tk.Tk()
        self.mapGui.geometry('900x700')
        self.mapGui.title('A star visual') 
       
        #create canvas (grid map)
        self.canvas = tk.Canvas(self.mapGui, width=620, height=620)
        self.canvas.grid(row = 0, column = 0)
        
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.grid = [[0 for x in range(self.gridSize)] for y in range(self.gridSize)]
        rows = 0
        cols = 0

        step = int(600 / self.gridSize)

        for i in range(20,620,step):
            cols=0
            for j in range(20,620,step):
                self.grid[rows][cols] = self.canvas.create_rectangle(j,i,j+step,i+step,outline='black', fill = 'gray')
                cols+=1
            rows+=1
        
        # set color for start and goal
        self.setColorStartGoal()

        #create Run button
        self.btnRun = tk.Button(self.mapGui, text = 'Run', command = self.Run)
        self.btnRun.place(x = 630, y = 20)        

    
    def setColorStartGoal(self):
        si = self.startNode.pos.i
        sj = self.startNode.pos.j
        gi = self.goalNode.pos.i
        gj = self.goalNode.pos.j

        self.canvas.itemconfigure(self.grid[si][sj], fill = 'green')
        self.canvas.itemconfigure(self.grid[gi][gj], fill='red')

    def tracking(self, myMap):
        di = [-1,-1,-1, 0, 1, 1, 1, 0]
        dj = [-1, 0, 1, 1, 1, 0,-1,-1]


        tmp_i = myMap.gi
        tmp_j = myMap.gj
        while tmp_i != myMap.si or tmp_j != myMap.sj:
            k = myMap.matNode[tmp_i][tmp_j].track
            tmp_i -= di[k]
            tmp_j -= dj[k]
            self.canvas.itemconfigure(self.grid[tmp_i][tmp_j], fill = 'yellow')

        self.canvas.itemconfigure(self.grid[myMap.si][myMap.sj], fill = 'green')

        return 1
    
    def Run(self):
        f = open("de.txt", "w")
        gridSize = self.gridSize
        mat = [[0 for i in range(gridSize)] for j in range(gridSize)]
        for i in range(gridSize):
            for j in range(gridSize):
                if self.canvas.itemcget(self.grid[i][j],"fill") == 'black':
                    mat[i][j] = 1
                f.write(str(mat[i][j]))
                f.write(" ")
            f.write("\n")

        si = self.startNode.pos.i
        sj = self.startNode.pos.j
        gi = self.goalNode.pos.i
        gj = self.goalNode.pos.j

        if self.str_algo != "ARA*":
            myMap = algo.Map()
            myMap.create(gridSize, mat, si, sj, gi, gj)
            flagFind = algo.AStar(myMap, self)


            if flagFind:
                res = self.tracking(myMap)
                messagebox.showinfo("Message", "Complete finding path")
            else:
                messagebox.showinfo("Message", "No path!")
        else:
            myMap = ara.Map()
            myMap.create(gridSize, mat, si, sj,gi,gj)
            
            ara.ARA(myMap, 2.5, 0.5, self)
            messagebox.showinfo("Message", "Complete finding path")

        
        f.close()

    def on_click(self, event):
        self._dragging = True
        self.on_move(event)

    def on_move(self, event):
        if self._dragging:
            items = self.canvas.find_closest(event.x, event.y)
            if items and self.canvas.itemcget(items, "fill") == 'gray':
                rect_id = items[0]
                self.canvas.itemconfigure(rect_id, fill="black")

    def on_release(self, event):
        self._dragging = False
