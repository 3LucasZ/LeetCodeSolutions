class Solution:
    def isValidList(self, group) -> bool:
        groupCopy = group.copy()
        
        #checks if the group has any duplicates
        while "." in groupCopy:
            groupCopy.remove(".")
         
        if (len(groupCopy) != len(set(groupCopy))):
            return False
        
        #checks if the group has any number not in [1,9]
        for digit in groupCopy:
            if digit not in [str(num) for num in list(range(1,10))]:
                return False
            
        return True
        
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        #check all rows
        for row in board:
            if not self.isValidList(row):
                return False
            
        #create list of all columns
        column_board = []
        for row_index in range(9):
            selected_column = []
            for row in board:
                selected_column.append(row[row_index])
            column_board.append(selected_column)
        
        #check all columns
        for column in column_board:
            if not self.isValidList(column):
                return False
            
        #create list of all mini 3x3 grids
        grid_board = []
        for i in range(3):
            for j in range(3):
                grid = []
                for selected_row in board[3*i:3*i+3]:
                    for num in selected_row[3*j:3*j+3]:
                        grid.append(num)
                grid_board.append(grid)
        
        #check all grids
        for grid in grid_board:
            if not self.isValidList(grid):
                return False
            
        #print (board)
        #print(column_board)
        #print(grid_board)
        
        return True
