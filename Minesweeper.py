"""
Jason Xiong
Minesweeper Game
"""
from tkinter import *
from tkinter import messagebox
import random
class MinesweeperCell(Label):
    '''represents a Minesweeper cell'''

    def __init__(self, master, coord):
        '''creates a minesweeper cell'''
        Label.__init__(self,master, height=1,width=2,text='',bg='white',font=('Arial',20))
        self.coord=coord #row and column of the cell as a tuple
        self.isActivated=False #cell begins unactivated
        self.isFlagged=False #cell begins unflagged
        self.colorList=['blue','darkgreen','red','purple','maroon','cyan','black','gray'] #List of colors for the cell numbers
        self.bind('<Button-1>',self.activate) #Left click to activate the cell
        self.bind('<Button-3>',self.flag) #Right click to flag the cell
        self.number=0 #number of bombs near the cell
        #set the look of the unactivated cell
        self['relief']=RAISED
        self['bg']='light gray'
        self.isDisabled=False #cell stays enabled until game end
        
    def activate(self, event):
        'activates cell'
        if self.isDisabled: #check if the game is over
            return None
        elif not self.isActivated and not self.isFlagged: #cell is unactivated and unflagged
            self.isActivated=True #activate the cell
            if self.number==0: #check if the square is not next to any bombs
                self.master.activateAdj(self.coord) #activate the appropriate adjacent cells 
            self.master.updateCells() #update the minesweeper grid
        
    def flag(self, event):
        'flags or unflags cell'
        if self.isDisabled: #check if the game is over
            return None
        elif not self.isActivated: #check if the cell is activated
            if self.isFlagged:
                self.master.bombsLeft+=1 #increase the number of bombs left
                self.isFlagged=not self.isFlagged
            else:
                self.master.bombsLeft-=1
                self.isFlagged=not self.isFlagged
            self.master.updateLabel()
            self.updateDisplay()
            
    def setNum(self, num):
        'gives a number to the cell'
        self.number=num
        
    def manualActivate(self):
        'activates the cell without click'
        self.isActivated=True
        
    def getNum(self):
        'returns the cell number' 
        return self.number

    def is_activated(self):
        'returns the cell activation status'
        return self.isActivated

    def is_flagged(self):
        'returns the cell flagged status'
        return self.isFlagged
    
    def disable(self):
        'disables the cell when the game ends'
        self.isDisabled=True
        
    def incrBombCounter(self):
        'increases the counter for adjacent cells with bombs'
        if self.number!=9:
            self.number+=1
        
    def updateDisplay(self):
        'updates the cell display'
        if self.isActivated:#checks if the cell is activated
            self['relief']=SUNKEN
            self['bg']='snow'
            if self.number==9: #checks if the activated cell is a bomb
                self['bg']='orange'
                self['text']='*'
            elif self.number<=8 and self.number>0: 
                self['fg']=self.colorList[self.number-1] #set othe color of the text to match the cell number
                self['text']=str(self.number)
        elif self.isFlagged: #checks if the cell was flagged
            self['text']='*' 
        elif not self.isFlagged: #checks if the cell is unflagged
            self['text']=''
            
class MinesweeperGrid(Frame):
    '''represents the Minesweeper Grid'''
    def __init__(self, master, height, length, numBombs):
        #Initialize new frame
        Frame.__init__(self, master, bg='gray')
        self.grid() #display the frame
        self.length=length #Length of the Grid
        self.height=height #Width of the Grid
        self.numBombs=numBombs #Number of bombs in the grid
        self.cells={} #create a dictionary for all the cells
        self.bombsLeft=numBombs #keep track of number of bombs left
        self.numActivated=0 #keeps track of the number of activated cells
        if(self.length*self.height<self.numBombs): #check if the number of bombs is greater than the total number of cells
            messagebox.showerror('Error', 'There are More Bombs Than Cells')
            return None
        else:
            #add lines to the odd columns
            for n in range(1, self.length,2):
                self.columnconfigure(n, minsize=1)
            #add lines to the odd rows
            for n in range(1, self.height,2):
                self.rowconfigure(n, minsize=1)
            #create the grid of minesweeper cells (that go in the even row and column numbers)
            for row in range(self.height):
                for column in range(self.length):
                    coord=(row, column)
                    self.cells[coord]=MinesweeperCell(self,coord)
                    self.cells[coord].grid(row=row*2,column=column*2)
            #create the label for the number of bombs remaining
            self.bombLabel=Label(self,text=str(self.bombsLeft), font=('Arial', 20))
            self.bombLabel.grid(row=2*self.height+1, column=self.length-2, columnspan=2)
            #pick random cells to contain bombs
            keys = random.sample(list(self.cells), self.numBombs)
            for i in range(self.numBombs):
                self.cells[keys[i]].setNum(9)
            #Give appropriate numbers to cells depending on the bomb arrangement
            coords=list(self.cells)
            for coord in self.cells:
                if self.cells[coord].getNum()==9: #Find the bombs and increase the bomb counter of adjacent cells
                    #check there is an adjacent cell on each side
                    if coord[0]+1<=self.height-1:
                        self.cells[(coord[0]+1, coord[1])].incrBombCounter()
                    if coord[1]+1<=self.length-1:
                        self.cells[(coord[0], coord[1]+1)].incrBombCounter()
                    if coord[0]+1<=self.height-1 and coord[1]+1<=self.length-1:
                        self.cells[(coord[0]+1, coord[1]+1)].incrBombCounter()
                    if coord[0]-1>=0:
                        self.cells[(coord[0]-1, coord[1])].incrBombCounter()
                    if coord[1]-1>=0:
                        self.cells[(coord[0], coord[1]-1)].incrBombCounter()
                    if coord[0]-1>=0 and coord[1]-1>=0:
                        self.cells[(coord[0]-1, coord[1]-1)].incrBombCounter()
                    if coord[0]-1>=0 and coord[1]+1<=self.length-1:
                        self.cells[(coord[0]-1, coord[1]+1)].incrBombCounter()
                    if coord[0]+1<=self.height-1 and coord[1]-1>=0:
                        self.cells[(coord[0]+1, coord[1]-1)].incrBombCounter()
            self.updateCells()
        
    def activateAdj(self,coord):
        'activates adjacent empty cells'
        #check there is an adjacent cell on each side
        if coord[0]+1<=self.height-1: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0]+1, coord[1])].is_activated() and not self.cells[(coord[0]+1, coord[1])].is_flagged():
                self.cells[(coord[0]+1, coord[1])].manualActivate()
                if self.cells[(coord[0]+1, coord[1])].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0]+1, coord[1])) #activate the adjacent cell and its adjacent cells
        if coord[1]+1<=self.length-1: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0], coord[1]+1)].is_activated() and not self.cells[(coord[0], coord[1]+1)].is_flagged():
                self.cells[(coord[0], coord[1]+1)].manualActivate()
                if self.cells[(coord[0], coord[1]+1)].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0], coord[1]+1)) #activate the adjacent cell and its adjacent cells
        if coord[0]+1<=self.height-1 and coord[1]+1<=self.length-1: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0]+1, coord[1]+1)].is_activated() and not self.cells[(coord[0]+1, coord[1]+1)].is_flagged():
                self.cells[(coord[0]+1, coord[1]+1)].manualActivate()
                if self.cells[(coord[0]+1, coord[1]+1)].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0]+1, coord[1]+1)) #activate the adjacent cell and its adjacent cells
        if coord[0]-1>=0: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0]-1, coord[1])].is_activated() and not self.cells[(coord[0]-1, coord[1])].is_flagged():
                self.cells[(coord[0]-1, coord[1])].manualActivate()
                if self.cells[(coord[0]-1, coord[1])].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0]-1, coord[1])) #activate the adjacent cell and its adjacent cells
        if coord[1]-1>=0: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0], coord[1]-1)].is_activated() and not self.cells[(coord[0], coord[1]-1)].is_flagged():
                self.cells[(coord[0], coord[1]-1)].manualActivate()
                if self.cells[(coord[0], coord[1]-1)].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0], coord[1]-1)) #activate the adjacent cell and its adjacent cells         
        if coord[0]-1>=0 and coord[1]-1>=0: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0]-1, coord[1]-1)].is_activated() and not self.cells[(coord[0]-1, coord[1]-1)].is_flagged():
                self.cells[(coord[0]-1, coord[1]-1)].manualActivate()
                if self.cells[(coord[0]-1, coord[1]-1)].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0]-1, coord[1]-1)) #activate the adjacent cell and its adjacent cells  
        if coord[0]-1>=0 and coord[1]+1<=self.length-1: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0]-1, coord[1]+1)].is_activated() and not self.cells[(coord[0]-1, coord[1]+1)].is_flagged():
                self.cells[(coord[0]-1, coord[1]+1)].manualActivate()
                if self.cells[(coord[0]-1, coord[1]+1)].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0]-1, coord[1]+1)) #activate the adjacent cell and its adjacent cells  
        if coord[0]+1<=self.height-1 and coord[1]-1>=0: #make sure the adjacent cell is in the grid
            if not self.cells[(coord[0]+1, coord[1]-1)].is_activated() and not self.cells[(coord[0]+1, coord[1]-1)].is_flagged():
                self.cells[(coord[0]+1, coord[1]-1)].manualActivate()
                if self.cells[(coord[0]+1, coord[1]-1)].getNum()==0: #check if the adjacent cell does not have a number
                    self.activateAdj((coord[0]+1, coord[1]-1)) #activate the adjacent cell and its adjacent cells       
    
    def updateLabel(self):
        'update the bombs remainding label'
        self.bombLabel['text']=str(self.bombsLeft)   
        
    def updateCells(self):
        'update all the cells display and information'
        bombCounter=0 #keep track of whether a bomb was triggered
        self.numFlagged=0 #number of cells flagged
        self.numActivated=0 #number of activated cells
        #update the display of each cell in the grid
        for coord in self.cells: 
            self.cells[coord].updateDisplay()
            if self.cells[coord].is_activated() and self.cells[coord].getNum()!=9:
                self.numActivated+=1
            if self.cells[coord].is_activated() and self.cells[coord].getNum()==9: #check if a cell was activated and contained a bomb
                bombCounter+=1
        if self.numActivated==self.height*self.length-self.numBombs: #check for win condition
            messagebox.showinfo('Minesweeper','Congratulations -- you won!') #winning message
            for coord in self.cells:
                #light up all the mines wight light green
                if not self.cells[coord].is_activated() and self.cells[coord].getNum()==9:
                    self.cells[coord]['bg']='light green'
                    self.cells[coord].updateDisplay()
                self.cells[coord].disable() #disable all the cells
        elif bombCounter>0: #check if any bombs were activated
            messagebox.showerror('Minesweeper','KABOOM! You lose.')#losing message
            for coord in self.cells:
                #find the mines and highlight them orange
                if not self.cells[coord].is_activated() and self.cells[coord].getNum()==9:
                    self.cells[coord]['bg']='orange'
                    self.cells[coord].updateDisplay()
                #find the wrongly flagged cells and mark them
                if self.cells[coord].is_flagged() and self.cells[coord].getNum()!=9:
                    self.cells[coord]['bg']='yellow'
                    self.cells[coord].updateDisplay()
                    self.cells[coord]['text']='X'
                self.cells[coord].disable()
root=Tk()
root.title('Minesweeper')
rowNum=int(input("Enter the number of rows: "))
columnNum=int(input("Enter the number of columns: "))
bombNum=int(input("Enter the number of bombs: "))
Minesweeper=MinesweeperGrid(root, rowNum, columnNum, bombNum)
root.mainloop()
