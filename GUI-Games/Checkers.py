from tkinter import *
import random

class CheckerSquare(Canvas):
    '''displays a square in the checker game'''

    def __init__(self,master,x,y):
        if x > 7:
            Canvas.__init__(self,master,width=50,height=50,bg='light grey')
            self["highlightbackground"] = 'light grey'
        elif (x + y) % 2 == 0:
            Canvas.__init__(self,master,width=50,height=50,bg='blanched almond')
            self["highlightbackground"] = 'blanched almond'
    
        else:
            Canvas.__init__(self,master,width=50,height=50,bg='dark green')
            self["highlightbackground"] = 'dark green'
            self.bind('<Button>',master.cell_clicked)
        self.grid(row=x,column=y)
        self.position = (x,y)
        #makes it easier to access x and y
        self.x = x
        self.y = y
        self.isKing = False 
    
    def make_color(self,color):
        '''CheckerSquare.make_color(color)
        changes color of piece on square to specified color'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10,10,44,44,fill=color)
    
    def get_position(self):
        '''CheckerSquare.get_position() -> (int,int)
        returns (x,y) of square'''
        return self.position
    
    def remove_oval(self):
        '''removes oval from the square'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)

    def become_king(self):
        '''square becomes a king'''
        self.isKing = True

    def remove_king(self):
        '''square gets dethroned'''
        self.isKing = False

    def get_jumps(self):
        '''get all the possible jumps of the piece'''
        jumps = []
        if (self.x+2,self.y+2*self.master.flow) in self.master.squares:
            if (self.master.board[(self.x+1,self.y+self.master.flow)] == 1-self.master.playerTurn\
            and self.master.board[(self.x+2,self.y+2*self.master.flow)]==None):
                jumps.append((self.x+2,self.y+2*self.master.flow))

        if (self.x-2,self.y+2*self.master.flow) in self.master.squares:
            if (self.master.board[(self.x-1,self.y+self.master.flow)] == 1-self.master.playerTurn\
            and self.master.board[(self.x-2,self.y+2*self.master.flow)]==None):
                jumps.append((self.x-2,self.y+2*self.master.flow))
        
        if self.isKing:
            if (self.x+2,self.y-2*self.master.flow) in self.master.squares:
                if (self.master.board[(self.x+1,self.y-self.master.flow)] == 1-self.master.playerTurn\
                and self.master.board[(self.x+2,self.y-2*self.master.flow)]==None):
                    jumps.append((self.x+2,self.y-2*self.master.flow))

            if (self.x-2,self.y-2*self.master.flow) in self.master.squares:
                if (self.master.board[(self.x-1,self.y-self.master.flow)] == 1-self.master.playerTurn\
                and self.master.board[(self.x-2,self.y-2*self.master.flow)]==None):
                    jumps.append((self.x-2,self.y-2*self.master.flow))
        return jumps
    
    def get_moves(self):
        '''get all the possible moves of the piece'''
        moves = self.get_jumps()
        if (self.x+1,self.y+self.master.flow) in self.master.squares:
            if self.master.board[(self.x+1,self.y+self.master.flow)]==None:
                moves.append((self.x+1,self.y+self.master.flow))

        if (self.x-1,self.y+self.master.flow) in self.master.squares:
            if self.master.board[(self.x-1,self.y+self.master.flow)]==None:
                moves.append((self.x-1,self.y+self.master.flow))
        
        if self.isKing:
            if (self.x+1,self.y-self.master.flow) in self.master.squares:
                if self.master.board[(self.x+1,self.y-self.master.flow)]==None:
                    moves.append((self.x+1,self.y-self.master.flow))

            if (self.x-1,self.y-self.master.flow) in self.master.squares:
                if self.master.board[(self.x-1,self.y-self.master.flow)]==None:
                    moves.append((self.x-1,self.y-self.master.flow))
        return moves

class CheckerBoard(Frame):
    '''represents a board of Checkers'''

    def __init__(self,master,computer):

        Frame.__init__(self,master,bg='white')
        self.grid()
        Label(self,text=' Turn:',font=('Arial',18)).grid(row=8,column=1)
        self.turnDisplay = CheckerSquare(self,8,2)
        self.statusLabel = Label(self,text='',font=('Arial',18))
        self.statusLabel.grid(row=8,column=4,columnspan=4)
        self.colors = ('white','red')
        self.firstCell = None
        self.secondCell = None
        self.playerTurn = 0
        self.flow = -1
        self.jumpInProgress = False
        self.computer = computer

        self.squares = {}  # stores Checkers squares
        for x in range(8):
            for y in range(8):
                position = (x,y)
                self.squares[position] = CheckerSquare(self,x,y)
        
        self.board = {}  # dict to store position
        # create opening position
        for x in range(8):
            for y in range(8):
                coords = (x,y)
                if y in [0,1,2] and (x + y) % 2 == 1:
                    self.board[coords] = 1  # player 1
                elif y in [5,6,7] and (x + y) % 2 == 1:
                    self.board[coords] = 0  # player 0
                else:
                    self.board[coords] = None  # empty
        self.update_display()
        
    def nextTurn(self):
        self.playerTurn = 1 - self.playerTurn
        self.flow = 0 - self.flow

        if self.playerTurn == self.computer:
            self.computerMove()

        if self.check_game_over():
            self.statusLabel['text'] = self.colors[self.playerTurn]+' loses!'
            for x in range(8):
                for y in range(8):
                    self.squares[(x,y)].unbind('<Button>')


    def update_display(self):
        '''CheckerGame.update_display()
        updates squares to match board
        also updates scoreboard'''
        # update squares
        for x in range(8):
            for y in range(8):
                rc = (x,y)
                piece = self.board[rc]
                if piece is not None:
                    self.squares[rc].make_color(self.colors[piece])
                    if self.squares[rc].isKing:
                        self.squares[rc].create_text(28,38,font=('Arial',60),
                        text="*")
                else:
                    self.squares[rc].remove_oval()

        # update turn display
        self.turnDisplay.create_oval(10,10,44,44,fill=self.colors[self.playerTurn])

    def cell_clicked(self,event):
        #listener function for a cell click
        coords = event.widget.get_position()
    
        if self.board[coords] == self.playerTurn and self.jumpInProgress == False:
            self.statusLabel['text'] = ''
            self.firstClick(coords)
        
        elif self.board[coords] == None and not self.firstCell == None:
            self.statusLabel['text'] = ''
            self.secondClick(coords)
        else:
            self.statusLabel['text']='Unallowed Move'
        self.update_display()

    def firstClick(self,coords):
        #does the action for the player's 'first click'
        self.clear_highlights()
        self.firstCell = coords
        self.squares[coords]['highlightbackground'] = 'black'
    
    def secondClick(self,coords):
        #does the action for the player's 'second click'
        self.secondCell = coords
        piece = self.squares[self.firstCell]

        if self.secondCell in piece.get_moves() and self.is_jump_available()==False:
        #if no jumps are available and a piece does a regular move, do so
            
            self.move_piece()
            #move the king attribute
            if piece.isKing:
                self.squares[self.secondCell].become_king()
                piece.remove_king()
            self.nextTurn()
            self.clear_highlights()
            self.squares[coords]['highlightbackground'] = 'black'
            
            
        elif self.secondCell in piece.get_jumps():
        #elif the player wants a jump, do so

            self.clear_highlights()
            self.squares[self.secondCell]['highlightbackground'] = 'black'
            self.jump_piece()
            #move the king attribute
            if self.squares[self.firstCell].isKing:
                    self.squares[self.secondCell].become_king()
                    piece.remove_king()
            #if the piece that just jumped can still jump, it must do so
            if len(self.squares[self.secondCell].get_jumps()) > 0:
                self.jumpInProgress = True
                self.firstCell = self.secondCell
                self.statusLabel['text'] = 'Must continue jump!'
            else:
                self.jumpInProgress = False
                
                self.nextTurn()
        
        else:
        #else it is not a valid move
            self.statusLabel['text']=('Unallowed Move')

        #if the piece is at the opposite end, make it a king
        if self.squares[self.secondCell].y == int(3.5 - 3.5*self.flow):
            print('King')
            self.squares[self.secondCell].become_king()

    def move_piece(self):
        '''move the piece'''
        self.board[self.firstCell] = None
        self.board[self.secondCell] = self.playerTurn

    def jump_piece(self):
        '''jump the piece'''
        self.board[self.firstCell] = None
        eaten_piece = ((self.firstCell[0] + self.secondCell[0])/2,\
                        (self.firstCell[1] + self.secondCell[1])/2)
        self.board[eaten_piece] = None
        self.squares[eaten_piece].isKing = False
        self.board[self.secondCell] = self.playerTurn
    
    def clear_highlights(self):
        '''clear all highlights'''
        for coord in self.squares:
            if self.squares[coord]['highlightbackground'] == 'black':
                self.squares[coord]['highlightbackground'] = 'dark green'
    
    def is_jump_available(self):
        '''check if a jump is available'''
        for coord in self.squares:
            if self.board[coord] == self.playerTurn and\
                len(self.squares[coord].get_jumps())>0:
                return True
        return False
    
    def check_game_over(self):
        '''check if the game is over'''
        pieces = 0
        for coord in self.board:
            if self.board[coord] == self.playerTurn:
                pieces+=1
        if pieces == 0:
            return True
        for coord in self.squares:
            if self.board[coord] == self.playerTurn and \
                len(self.squares[coord].get_moves())>0:
                return False
        return True
    
    def computerMove(self):
        '''take the move for a computer'''
        playables = []
        if self.is_jump_available():
            for x in range(8):
                for y in range(8):
                    if self.board[(x,y)] == self.computer\
                        and len(self.squares[(x,y)].get_jumps()) > 0:
                            playables.append((x,y))
        else:
            for x in range(8):
                for y in range(8):
                    if self.board[(x,y)] == self.computer and\
                        len(self.squares[(x,y)].get_moves()) > 0:
                        playables.append((x,y))
        
        self.firstCell = random.choice(playables)
        self.firstClick(self.firstCell)
        
        
        if len(self.squares[self.firstCell].get_jumps()) > 0:
            self.secondCell = random.choice(self.squares[self.firstCell].get_jumps())
        else:
            self.secondCell = random.choice(self.squares[self.firstCell].get_moves())
       
        self.secondClick(self.secondCell)
        self.update_display()
        while len(self.firstCell.get_jumps()) > 0:
            self.update_display()
            self.secondCell =  random.choice(self.squares[self.firstCell].get_jumps())
            self.secondClick(self.secondCell)


def play_checkers(computer=None):
    '''play_checkers()
    starts a new game of checkers'''
    root = Tk()
    root.title('Checkers')
    Ckr = CheckerBoard(root,computer)
    Ckr.mainloop()
play_checkers()