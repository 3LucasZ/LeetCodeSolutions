from tkinter import *
from tkinter import messagebox
import random

class SweeperCell(Label):
    '''represents a Sweeper cell'''

    def __init__(self,master,coord):
        '''SweeperCell(master,coord) -> SweeperCell
        creates a new blank SweeperCell with (row,column) coord'''
        #set up attributes
        self.flagged = False
        self.exposed = False
        self.isBomb = False
        self.adjBombs = 0
        self.coord = coord

        #initialize new label
        Label.__init__(self,master,height=1,width=2,text='',\
                       bg='white',bd=5,relief=RAISED,font=('Arial',24))
        
        #set up listeners
        self.bind('<Button-1>',self.cellClicked)
        self.bind('<Button-2>',self.toggle_flag)

    def cellClicked(self,event):
        '''SweeperCell.cellClicked(event)
        handler function for left click
        '''
        #if game is still running
        if self.master.get_game_status() == 'running':
            # expose the cell
            self.expose()
            # exposing is finished - check if game over
            self.master.check_game_won()
            if self.master.get_game_status() == 'won':
                messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)

                

    def expose(self):
        '''SweeperCell.expose()
        exposes the cell
        auto expose feature
        whenever a blank square is exposed,
        all its adjacent squares are exposed too'''
        #color map list - to easily assign fg color
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        
        #if cell is not flagged or exposed - expose it
        if not self.flagged and not self.exposed:
            #if its a bomb cell - game ends and player loses
            if self.isBomb:
                self.master.explode_all()
                self.master.game_lost()
            else:
            #else expose the cell and show its number of adjacent bombs
                self.updateAdjBombs()
                if self.adjBombs > 0:
                    self['text'] = self.adjBombs
                    self['fg'] = colormap[self.adjBombs]
                self['bg'] = 'grey'
                self['relief'] = SUNKEN
                self.exposed = True
                #auto expose feature
                if self.adjBombs == 0:
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if (self.coord[0]+x,self.coord[1]+y) in self.master.get_cells():
                                self.master.get_cells()[(self.coord[0]+x,self.coord[1]+y)].expose()
                                
    def toggle_flag(self,event):
        '''SweeperCell.toggle_flag(event)
        handler function for right click
        flags or unflags the cell'''
        #if game hasnt ended
        if self.master.get_game_status() == 'running':
            #if cell is not exposed
            if not self.exposed:
                #toggle the flag state
                if self.flagged:
                    self['text'] = ''
                    self.flagged = False
                    self.master.bombsLeft += 1
                else:
                    if self.master.bombsLeft > 0:
                        self['text'] = '*'
                        self.flagged = True
                        self.master.bombsLeft -= 1
                self.master.update_label()

    def become_bomb(self):
        '''SweeperCell.become_bomb()
        cell becomes a bomb'''
        self.isBomb = True
        #testing if method works
        #self['bg'] = 'red'

    def explode(self):
        '''SweeperCell.explode()
        cell explodes'''
        self['bg'] = 'red'
        self['text'] = '*'
    
    def updateAdjBombs(self):
        '''SweeperCell.updateAdjBombs()
        sets the cell adjBombs attribute
        to the amount of adjacent bombs to the cell'''
        #checking the adjacent cells for bombs 
        #x x x
        #x o x
        #x x x
        for x in range(-1,2):
            for y in range(-1,2):
                if (self.coord[0]+x,self.coord[1]+y) in self.master.get_cells():
                    if self.master.get_cells()[(self.coord[0]+x,self.coord[1]+y)].isBomb:
                        self.adjBombs += 1

    def is_exposed(self):
        '''SweeperCell.is_exposed()
        returns exposed value'''
        return self.exposed


class SweeperGrid(Frame):
    '''object for a Sweeper grid'''

    def __init__(self,master,width,height,numBombs):
        '''SweeperGrid(master)
        creates a SweeperGrid with
        width: width
        height: height
        numBombs: numBombs'''

        #set up attributes
        self.width = width
        self.height = height
        self.numBombs = numBombs
        self.bombsLeft = numBombs
        self.gameStatus = 'running'
        #initialize a new frame
        Frame.__init__(self,master)
        self.grid()
        #bombsLeft label
        self.bombsLeftLabel = Label(self,text=numBombs,font=('Arial',40))
        self.bombsLeftLabel.grid(row=height,column=0,columnspan=width)

        self.cells = {} # set up dictionary for cells
        for row in range(self.height):
            for column in range(self.width):
                coord = (row,column)
                self.cells[coord] = SweeperCell(self,coord)
                self.cells[coord].grid(row=row,column=column)
        # make list of all the cells that will be bombs
        # numBombs bombs, and picked randomly
        self.bombs = random.sample(list(self.cells.values()),numBombs)
        for bomb in self.bombs:
            bomb.become_bomb()
    
    def explode_all(self):
        '''SweeperGrid.expode_all()
        explodes all the bombs in the grid'''
        for bomb in self.bombs:
            bomb.explode()

    def update_label(self):
        '''SweeperGrid.update_label()
        updates the bombsLeftLabel'''
        self.bombsLeftLabel['text'] = self.bombsLeft

    def check_game_won(self):
        '''SweeperGrid.check_game_won()
        checks if the game has been won and updates gameStatus'''
        #count number of exposed cells
        exposeNum = 0
        for coor in self.cells:
            if self.cells[coor].is_exposed():
                exposeNum+=1
        #if all the grid's cells are exposed, game is won
        if exposeNum == (self.width * self.height) - self.numBombs:
            self.gameStatus = 'won'
    
    def game_lost(self):
        '''SweeperGrid.game_lost()
        method called when game is lost'''
        self.gameStatus = 'lost'
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
    
    def get_game_status(self):
        '''SweeperGrid.get_game_status()
        returns gameStatus'''
        return self.gameStatus
    
    def get_cells(self):
        '''SweeperGrid.get_cells()
        returns cells dictionary'''
        return self.cells

# main loop for the game
def minesweeper():
    '''minesweeper()
    plays minesweeper'''
    root = Tk()
    root.title('Mine Sweeper')
    sg = SweeperGrid(root,10,14,8)
    root.mainloop()

minesweeper()

'''My response:
My initial plan was to first find what classes I would need,
then find what basic methods and attributes I would need to get the basic
idea of the game working
After, I would add the necessary things to make the game fully function
my game logic:
SweeperCell is a label - used bind to capture left and right clicks,
used label properties to customize it properly. I made the bd larger
then in the example because I like it more :P
SweeperGrid is a grid of all the SweeperCells + the numBombs label
you lose if you expose a sweeperCell that is a bomb
when you lose, all the bombs explode, and a you lost message pops up
you win if all the sweeperCells are exposed
the program checks all the cells and if all the non-bomb cells are exposed
the autoexpose feature works recursively - 
I created 2 methods, a method to listen to the left click and a method to do the exposing
the listener method first checks if the game is running then calls the expose method on
the clicked cell
if the clicked cell is not flagged and is not yet exposed - expose it
after a cell is exposed, if it has no adjacent bombs, all adjacent cells
get the exposed method called on them, thus the cycle repeating.
once all the exposing is finished, the listener method checks if the game has been
won during the turn and does the necessary actions if so.
to check adjacent cells I find all cells that are in -1,-1 to 2,2 range of the 
initial 
I used cell.self['fg'] = colormap[self.adjBombs]to get the right fg color
if self.adjBombs > 0:
to make sure the '' color was never called.

toggling flag only works when the game is running and
it decreases/increases the numBombsLabel and makes the clicked cell unexposable/exposable 
I was also able to reuse some of the cell dictionary, cells, coordinate logic from 
the sudoku.
The minesweeper was fun to make! :)
'''