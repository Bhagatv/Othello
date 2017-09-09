#Veeral Bhagat 10763937

def number_to_letter(turn: int) ->str:
    'Converts number of board to letter'
    if turn == 1:
        return 'B'
    elif turn ==2:
        return 'W'
    elif turn == 0:
        return 'NONE'
def letter_to_number(turn: str) -> int:
    'Converts letter of board to number corresponding to it'
    if turn == 'B':
        return 1
    if turn == 'W':
        return 2

def print_board(x: list) -> None:
    'Prints the board in a readable format'
    board=''
    for r in range(len(x)):
        for c in range(len(x[0])):
            if x[r][c] == 0:
                board+='. '
            if x[r][c] == 1:
                board+='B '
            if x[r][c] == 2:
                board+='W '
        board+='\n'
    print(board[:-1])

def get_winner(relational: str,count:list)-> int:
    'Returns the number associated with the winner depending on the color count'
    if relational.strip() == '>':
        if count[0] > count[1]:
            return 1 #black wins
        if count[1] > count[0]:
            return 2 #white wins
        if count[1] == count[0]:
            return 0 #no one wins
    if relational.strip() == '<':
        if count[0] < count[1]:
            return 1 #black wins
        if count[1] < count [0]:
            return 2 #white wins
        if count[1] == count[0]:
            return 0 #no one wins


def opposite(turn: int)-> int:
    'Returns opposite of the current turn'
    if turn==1:
        turn=2
    elif turn==2:
        turn=1
    return turn


class GameState:
    'Class defining a gameboard and all its contents, such as turn'
    def __init__(self)-> None:
        'Creates an empty list for the board and initializes the first turn to 0'
        self._game_board = []
        self._turn = 1
        
    def empty_board(self,nrows: int, ncols: int):
        for r in range(nrows):
            self.return_board().append([])
            for c in range(ncols):
                self.return_board()[r].append(0)
        print(self.return_board())
        
    def return_turn(self)-> int:
        'Returns current turn based on GameState'
        return self._turn
    
    def change_turn(self,turn: int)-> None:
        'Changes turn based on the parameter'
        self._turn = turn
        
    def update_board(self, main_board: [[int]])-> None:
        'Updates board based on the board included in the parameter'
        self._game_board=main_board
        
    def make_move(self,turn: int, row: int, col: int, rowdelta:int, coldelta:int, nrows: int, ncols: int) -> [[int]]:
        'Makes move depending on if the next spot in the board is of the same turn, oppsite turn, or just a period'
        k = list(self._game_board)
        
        list_of_changes=[]
        
        count=0
        for i in range(1,nrows+ncols):
            
            if self._game_board[row][col] != 0:
                break
            if (((row+rowdelta*i) < 0 or (row+rowdelta*i >= nrows)) or \
                ((col+coldelta*i) < 0 or (col+coldelta*i >= ncols))):
                continue
            elif self._game_board[row+rowdelta*i][col+coldelta*i] == turn and count==0:
                break
            elif self._game_board[row+rowdelta*i][col+coldelta*i] == opposite(turn):
                count+=1
            elif self._game_board[row+rowdelta*i][col+coldelta*i] == 0:
                break
            elif self._game_board[row+rowdelta*i][col+coldelta*i] == turn and count!=0:
                count=0
                list_of_changes.append([row+rowdelta*i,col+coldelta*i])
                
                for j in range(1,i):
                    if(((row+rowdelta*j) < 0 or (row+rowdelta*j >= nrows)) or \
                ((col+coldelta*j) < 0 or (col+coldelta*j >= ncols))):
                        continue
                    elif self._game_board[row+rowdelta*j][col+coldelta*j] == opposite(turn):
                        count+=1
                        list_of_changes.append([row+rowdelta*j,col+coldelta*j])
                    elif self._game_board[row+rowdelta*j][col+coldelta*j] == turn:
                        break
                             
            else:
                pass                 
        for change in list_of_changes:
            self._game_board[change[0]][change[1]] = turn
        return list_of_changes

    def return_board(self)-> [[int]]:
        'Returns game board'
        return self._game_board
    
    def count(self)->[int]:
        'Counts up the number of blacks and whites in the board'
        black_count = 0
        white_count = 0
        for r in range(len(self._game_board)):
            for c in range(len(self._game_board[0])):
                if self._game_board[r][c] == 1:
                    black_count+=1
                elif self._game_board[r][c] == 2:
                    white_count+=1
        return [black_count,white_count]

    def board_capacity_checker(self)-> bool:
        'Checks if the board isn\'t full and return False if it isn\'t, true if it is.'
        for r in range(len(self._game_board)):
            for c in range(len(self._game_board[0])):
                if self._game_board[r][c] == 0:
                    return False
        return True
    
    def _get_empty_spaces(self)-> list:
        '''Returns list of all the empty spots in the board. Function is not used outside of
           this module, so it is private'''
        result=[]
        for r in range(len(self._game_board)):
            for c in range(len(self._game_board[0])):
                if self._game_board[r][c] == 0:
                    result.append([r,c])
        return result
    
    def valid_move_left(self, turn: int, nrows: int, ncols: int, list_of_deltas)-> bool:
        'Checks if, given a specific turn, there is a valid move left by iterating through every direction'
        board= self._game_board
        empty_spaces = self._get_empty_spaces()
        temp_state = GameState()
        temp_board=[]
        for r in range(len(self._game_board)):
            temp_state._game_board.append(self._game_board[r][:])
            

        count = self.count()
        if turn == 1:
            if count[0] == 0:
                return False
        if turn == 2:
            if count[1] == 0:
                return False
        for ordered_pair in empty_spaces:
            if self.is_valid_move(turn,ordered_pair[0],ordered_pair[1],nrows, ncols,list_of_deltas):
            
            
                for deltas in list_of_deltas:
                    color_count_before = temp_state.count()
                    temp_board = temp_state.make_move(turn,ordered_pair[0],ordered_pair[1],deltas[0],deltas[1],nrows,ncols)
                    color_count_after = temp_state.count()
                  
                    if color_count_before != color_count_after:
                        return True
            
    
        return False
    def is_valid_move(self,turn: int, row: int, col:int,nrows: int, ncols: int,list_of_deltas: list)-> bool:
        '''Checks every direction from a specific spot in the board if there exists a valid move. Returns True if there is,
        False if there isn\'t depending on the function \'check_sequence\''''

        for delta in list_of_deltas:
            if self.check_sequence(turn,row,col,delta[0],delta[1],nrows,ncols):
                return True
        return False

    def check_sequence(self,turn: int,row:int,col: int, rowdelta:int, coldelta:int, nrows: int, ncols: int) -> bool:
        '''Given a specific direction to go in, given by the rowdelta/coldelta, iterates through everything in that direction and returns a
        bool depending on if the move is valid in that specific direction.'''
        focus = self._game_board[row][col]
        count=0
        for i in range(1,nrows+ncols):
            if (((row+rowdelta*i) < 0 or (row+rowdelta*i >= nrows)) or \
                    ((col+coldelta*i) < 0 or (col+coldelta*i >= ncols))):
                continue
            elif opposite(turn) == self._game_board[row+rowdelta*i][col+coldelta*i]:
                count+=1
                continue
            elif 0 == self._game_board[row+rowdelta*i][col+coldelta*i] and count==0:
                return False
            elif turn == self._game_board[row+rowdelta*i][col+coldelta*i] and count!=0:
                continue
            elif focus == 0 and count == 0:
                return False
        return True


