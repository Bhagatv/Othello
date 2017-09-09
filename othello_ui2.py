#Veeral Bhagat 10763937

import othello_logic

class InvalidEntry(Exception):
    'If user enters an invalid input in either first player or relational'
    def __init__(self, string):
        self._string = string
    def __str__(self):
        return 'Invalid input: '+self._string
    pass
class InvalidDimensionsInputted(Exception):
    'If user enters dimensions that are invalid'
    def __init__(self,string):
        self._string = string
    def __str__(self):
        return 'Number of row/col is not an even number between 4 and 16: '+self._string
    pass
class InvalidBoardInput(Exception):
    'If user enters a board that is of invalid syntax'
    pass
class InvalidRowColError(Exception):
    'If user inputs a row/col that is greater than or equal to the total number of rows/col in the board'
    pass


def _no_available_moves(turn: int)-> str:
    'Shortcut to return the string when no movies are available'
    return 'No available moves for '+othello_logic.number_to_letter(turn)

def _get_relational() -> str:
    'Prompts user for input of relational operator to determine the winner'
    win_determiner = input()
    if win_determiner.strip() != '>' and win_determiner.strip() != '<':
        raise InvalidEntry(win_determiner)
    else:
        return win_determiner
        
def _create_board(nrows: int, ncols: int) -> [[int]]:
    'Prompts user for rows of board and replaces the letters to numbers in the background'
    board=[]
    i=0
        #message = 'Enter '+str(i+1)+'st row with '+str(NUMBER_COLS)+' columns: '
    while i<nrows:
        inputted = input()
        if len(inputted.replace(' ','')) !=ncols:
            raise InvalidBoardInput(inputted)
        else:
            board.append(inputted.strip())
            board[i] = board[i].split(' ')
            if len(board[i]) !=ncols:
                raise InvalidBoardInput(inputted)
        i+=1
    for r in range(len(board)):
        for c in range(len(board[0])):
            board[r][c] = board[r][c].replace('.','0')
            board[r][c] = board[r][c].replace('B','1')
            board[r][c] = board[r][c].replace('W','2')
            try:
                board[r][c] = int(board[r][c])
            except ValueError:
                raise InvalidBoardInput()
        #print(board)
        #self._game_board = board
    return board
    
def _get_input()-> int:
    'Prompts user for rows & col input'
    result=0
    while True:
        result = input()
        try:
            if int(result) % 2 != 0 or int(result) < 4 or int(result) > 16:
                raise InvalidDimensionsInputted(result)
                
        except ValueError:
            raise InvalidDimensionsInputted(result)
        break
    return int(result)


def _get_turn() -> int:
    'Prompts user for who goes first in the game'
    turn=0
    while True:
        turn = input()
        number_turn = othello_logic.letter_to_number(turn)
        if number_turn == None:
            raise InvalidEntry(turn)
        break
    return number_turn

    
def run_user_interface() -> None:
    'Creates board and goes through the complex chain, prompting users for row and col each turn'
    list_of_deltas = [[-1,0],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[0,1],[-1,1]]

    game_state = othello_logic.GameState()
    
    number_of_rows = _get_input()
    number_of_cols = _get_input()

    game_state.change_turn(othello_logic.opposite(_get_turn()))
    win_determiner = _get_relational()
    loop = True
    
    game_state.update_board(_create_board(number_of_rows,number_of_cols))


    color_count = game_state.count()
    print('B:',color_count[0],'W:',color_count[1])
    othello_logic.print_board(game_state.return_board())
    
    invalid = False
    untouched=0
    while loop:
        game_state.change_turn(othello_logic.opposite(game_state.return_turn()))
        
        if game_state.return_board() == None:
            break
        if game_state.board_capacity_checker():
            print('WINNER:',othello_logic.number_to_letter(othello_logic.get_winner(win_determiner,color_count)))
            break
        if not game_state.valid_move_left(game_state.return_turn(),number_of_rows, number_of_cols, list_of_deltas):
            #print(_no_available_moves(game_state.return_turn()))
            game_state.change_turn(othello_logic.opposite(game_state.return_turn()))
            if not game_state.valid_move_left(game_state.return_turn(),number_of_rows, number_of_cols, list_of_deltas):
                #print(_no_available_moves(othello_logic.opposite(game_state.return_turn())))
                #print(_no_available_moves(game_state.return_turn()))
                print('WINNER:',othello_logic.number_to_letter(othello_logic.get_winner(win_determiner,color_count)))
                break
            else:
                print(_no_available_moves(othello_logic.opposite(game_state.return_turn())))
        if not invalid:
            print('Turn: ',othello_logic.number_to_letter(game_state.return_turn()))
        else:
            invalid=False
        row_col = input().split()
        if len(row_col) != 2:
            raise InvalidRowColError('Format incorrect for input')
        
        row,col = int(row_col[0])-1,int(row_col[1])-1

        if row >= number_of_rows or col >=number_of_cols:
            raise InvalidRowColError('Row: '+str(row+1)+'. '+'Col: '+str(col+1)+'.')
        if game_state.is_valid_move(game_state.return_turn(),row,col,number_of_rows,number_of_cols,list_of_deltas): 
    
            for deltas in list_of_deltas:
                if game_state.check_sequence(game_state.return_turn(),row,col,deltas[0],deltas[1],number_of_rows,number_of_cols):
                    
                    color_count_before = game_state.count()
                  
                    game_state.make_move(game_state.return_turn(),row,col,deltas[0],deltas[1],number_of_rows,number_of_cols)
                    color_count_after = game_state.count()
                   
                    if color_count_before != color_count_after:
                        untouched+=1
                        if untouched==1:
                            print('VALID')
                        
                        invalid = False
                        continue
            if untouched == 0:
               
                invalid = True
            elif untouched !=0:
                untouched = 0
                game_state.return_board()[row][col]=game_state.return_turn()
        else:
            invalid = True
            
        if invalid:
                
            print('INVALID')
            game_state.change_turn(othello_logic.opposite(game_state.return_turn()))
            continue
        
        color_count = game_state.count()
        print('B:',color_count[0],'W:',color_count[1])
        othello_logic.print_board(game_state.return_board())
        
        if not game_state.valid_move_left(othello_logic.opposite(game_state.return_turn()), number_of_rows, number_of_cols, list_of_deltas) \
           and not game_state.valid_move_left(game_state.return_turn(), number_of_rows, number_of_cols, list_of_deltas):
            print('WINNER:',othello_logic.number_to_letter(othello_logic.get_winner(win_determiner,color_count)))
            break
        
if __name__ == '__main__':
    print('FULL')
    run_user_interface()
    
