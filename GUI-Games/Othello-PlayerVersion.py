from tkinter import *
 
class ReversiBoard:
    '''represents a board of Reversi'''
 
    def __init__(self):
        '''ReversiBoard()
        creates a ReversiBoard in starting position'''
        self.board = {}  # dict to store position
        # create opening position
        for row in range(8):
            for column in range(8):
                coords = (row,column)
                if coords in [(3,3),(4,4)]:
                    self.board[coords] = 1  # player 1
                elif coords in [(3,4),(4,3)]:
                    self.board[coords] = 0  # player 0
                else:
                    self.board[coords] = None  # empty
        self.currentPlayer = 0  # player 0 starts
        self.endgame = None  # replace with string when game ends
 
    def get_piece(self,coords):
        '''ReversiBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]
 
    def get_endgame(self):
        '''ReversiBoard.get_endgame() -> None or str
        returns endgame state'''
        return self.endgame
 
    def get_player(self):
        '''ReversiBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer
 
    def next_player(self):
        '''ReversiBoard.next_player()
        advances to next player'''
        self.currentPlayer = 1 - self.currentPlayer
 
    def get_scores(self):
        '''ReversiBoard.get_scores() -> tuple
        returns a tuple containing player 0's and player 1's scores'''
        pieces = list( self.board.values() )  # list of all the pieces
        # count the number of pieces belonging to both players
        return pieces.count(0), pieces.count(1)
 
    def flip_pieces(self,coords,checkingOnly=False):
        '''ReversiBoard.flip_pieces(coords[checkingOnly]) -> int
        returns number of pieces flipped when a piece is played at coords
          checkingOnly True just computes, doesn't actually flip
          checkingOnly False also flips the pieces'''
        # get player colors
        thisPlayer = self.currentPlayer
        otherPlayer = 1 - thisPlayer
        flipped = 0  # counts flipped pieces
        # loop over the 8 possible directions
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0:  # non-direction
                    continue
                # look at the first square in the given direction
                (row,col) = (coords[0]+dr,coords[1]+dc)
                counter = 0  # keep track of how many squares have a
                             # piece of the opposite color
                # keep looking as long as we have pieces of the opposite
                #   color and we're still on the board
                while (0 <= row < 8) and (0 <= col < 8) and \
                      self.board[(row,col)] == otherPlayer:
                    (row,col) = (row+dr,col+dc) # continue moving in this direction
                    counter += 1  # increment the count of number of stones flipped
                # the next stone must be of the current player's color
                #  (and still on the board)
                if (0 <= row < 8) and (0 <= col < 8) and \
                   self.board[(row,col)] == thisPlayer:
                    # this direction will get flipped
                    flipped += counter  # update the overall flipped counter
                    if not checkingOnly:  # if not just checking, flip them!
                        for i in range(1,counter+1):
                            self.board[(coords[0]+i*dr,coords[1]+i*dc)] = thisPlayer
        return flipped
 
    def get_legal_moves(self):
        '''ReversiBoard.get_legal_moves() -> list
        returns a list of the current player's legal moves'''
        moves = []  # place legal moves here
        for row in range(8):  # check each square
            for column in range(8):
                coords = (row,column)
                # if space is empty and would flip pieces
                if self.board[coords] is None and \
                   self.flip_pieces(coords,checkingOnly=True) > 0:
                    moves.append(coords)  # add to list
        return moves
 
    def try_move(self,coords):
        '''ReversiBoard.try_move(coords)
        places the current player's piece in the given square if the
          square is empty and the move is legal
        also flips necessary pieces and goes to other player's turn'''
        if self.board[coords] is not None:  # if square occupied
            return  # do nothing
        # flip any pieces and check how many got flipped
        numFlipped = self.flip_pieces(coords)
        if numFlipped > 0:  # if any pieces flipped
            # set the target square to the current player's color
            self.board[coords] = self.currentPlayer
            self.next_player()  # next player's turn
            self.check_endgame()  # check if game over
 
    def check_endgame(self):
        '''ReversiBoard.check_endgame()
        checks if game is over
        updates endgameMessage if over'''
        # if current player has no legal move
        if len(self.get_legal_moves()) == 0:
            self.next_player()  # temporarily switch to next player
            # if other player has no legal move, game is over
            if len(self.get_legal_moves()) == 0:
                scores = self.get_scores()
                if scores[0] > scores[1]:
                    self.endgame = 0
                elif scores[0] < scores[1]:
                    self.endgame = 1
                else:
                    endgame = 'draw'
            self.next_player()  # return to original player

class ReversiSquare(Canvas):
    '''displays a square in the Reversi game'''
 
    def __init__(self,master,r,c):
        '''ReversiSquare(master,r,c)
        creates a new blank Reversi square at coordinate (r,c)'''
        # create and place the widget
        Canvas.__init__(self,master,width=50,height=50,bg='medium sea green')
        self.grid(row=r,column=c)
        # set the attributes
        self.position = (r,c)
        # bind button click to placing a piece
        self.bind('<Button>',master.get_click)
 
    def get_position(self):
        '''ReversiSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

 
    def make_color(self,color):
        '''ReversiSquare.make_color(color)
        changes color of piece on square to specified color'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10,10,44,44,fill=color)
 
class ReversiGame(Frame):
    '''represents a game of Reversi'''
 
    def __init__(self,master):
        '''ReversiGame(master,[computerPlayer])
        creates a new Reversi game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # set up game data
        self.colors = ('black','white')  # players' colors
        # create board in starting position, player 0 going first
        self.board = ReversiBoard() 
        self.squares = {}  # stores ReversiSquares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                self.squares[rc] = ReversiSquare(self,row,column)
        # set up scoreboard and status markers
        self.rowconfigure(8,minsize=3)  # leave a little space
        self.turnSquares = []  # to store the turn indicator squares
        self.scoreLabels = []  # to store the score labels
        # create indicator squares and score labels
        for i in range(2):  
            self.turnSquares.append(ReversiSquare(self,9,7*i))
            self.turnSquares[i].make_color(self.colors[i])
            self.turnSquares[i].unbind('<Button>')
            self.scoreLabels.append(Label(self,text='2',font=('Arial',18) ) )
            self.scoreLabels[i].grid(row=9,column=1+5*i)
        self.passButton = Button(self,text='Pass',command=self.pass_move)
        self.passButton.grid(row=9,column=3,columnspan=2)
        self.update_display()
 
    def get_click(self,event):
        '''ReversiGame.get_click(event)
        event handler for mouse click
        gets click data and tries to make the move'''
        coords = event.widget.get_position()
        # try_move will do the move if valid
        # it will do nothing if not
        self.board.try_move(coords)
        self.update_display()  # update the display
 
    def pass_move(self):
        '''ReversiGame.pass_move()
        event handler for Pass button
        passes for the player's turn'''
        self.board.next_player()  # move onto next player
        self.update_display()
 
    def update_display(self):
        '''ReversiGame.update_display()
        updates squares to match board
        also updates scoreboard'''
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                piece = self.board.get_piece(rc)
                if piece is not None:
                    self.squares[rc].make_color(self.colors[piece])
        # update the turn indicator
        newPlayer = self.board.get_player()
        oldPlayer = 1 - newPlayer
        self.turnSquares[newPlayer]['highlightbackground'] = 'blue'
        self.turnSquares[oldPlayer]['highlightbackground'] = 'white'
        # update the score displays
        scores = self.board.get_scores()
        for i in range(2):
            self.scoreLabels[i]['text'] = scores[i]
        # enable or disable the Pass button
        if len(self.board.get_legal_moves()) == 0:  # if no legal moves
            self.passButton.config(state=NORMAL)  # enable button
        else:  # if there are legal moves
            self.passButton.config(state=DISABLED)
        # if game over, show endgame message
        endgame = self.board.get_endgame()
        if endgame is not None:  # if game is over
            # remove the turn indicator
            self.turnSquares[newPlayer]['highlightbackground'] = 'white'
            if isinstance(endgame,int):  # if a player won
                winner = self.colors[endgame]  # color of winner
                endgameMessage = '{} wins!'.format(winner.title())
            else:
                endgameMessage = "It's a tie!"
            Label(self,text=endgameMessage,font=('Arial',18)).grid(row=9,column=2,columnspan=4)
 
def play_reversi():
    '''play_reversi()
    starts a new game of Reversi'''
    root = Tk()
    root.title('Reversi')
    RG = ReversiGame(root)
    RG.mainloop()
 
play_reversi()
