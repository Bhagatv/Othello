import tkinter
import math
import othello_logic2
import othello_ui2
import coordinate

class Board:
    'Creates board that represents the graphical paralell to the 2D list in the game logic'
    
    def __init__(self,row: int,col: int,first_player: int,win_determiner: str) -> None:
        '''Initializes various elements of the game, including graphical components and components necessary
        to go back and forth between logic and GUI'''
        self._game_state = othello_logic2.GameState()
        self._game_state.change_turn(1)
        self._game_state._first_player=first_player
        
        self._dictionary = {}
        self._dictionary_rect = {}
        self._window=tkinter.Tk()
        self._window.title('Othello FULL')
       
        self._win_determiner=win_determiner  #move

        
        self._change_color = False    
        
        self._canvas = tkinter.Canvas(
            master=self._window,
            width=400,height=400,
            background='#000080',highlightthickness=0)

        
        self._canvas_width= self._canvas.winfo_width()
        self._canvas_height= self._canvas.winfo_height()
        self._list_of_ovals = []
        self._rows = row
        self._cols = col
        self._turn = 1
        self._first_player = first_player
        
        self._game_state.empty_board(self._rows,self._cols)
       
        self._list_of_orig = []
        self._canvas.grid(
            row = 0, column = 0, padx = 30, pady = 30,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        
       
        
        self._window.rowconfigure(0, weight = 1)
        self._window.columnconfigure(0, weight = 1)
        
        self._canvas.bind('<Configure>',self.draw_grid)
        
        self._turn_label = tkinter.Label(master=self._window,text=othello_logic2.number_to_letter(self._game_state.return_turn())+' choose spots for discs then press Done',font=('Comic Sans MS',12))
        self._turn_label.grid(row=5,column=0, padx=10,pady=10,sticky=tkinter.N+tkinter.W+tkinter.E+tkinter.S)
        
        self._done_button = tkinter.Button(master=self._window,text='Done')
        self._done_button.bind('<Button-1>',self.setup)
        self._done_button.grid(row=5,column=2,padx=10,pady=10,sticky=tkinter.N+tkinter.W+tkinter.E+tkinter.S)

        self._list_of_rect=[]
            
        self._done_int = 0

        self._color_count = tkinter.Label(master=self._window,text='')
        
       
    def quit(self,d: 'Dialog') -> None:
        'On cancel of the main window, closes all dialogs so the program terminates'
        
        self._window.destroy()
        #d._dialog.destroy()
        d._error.destroy()
    def run(self) -> None:
        'Runs the mainloop to give control to tkinter'
        self._window.mainloop()
        
    def setup(self,event: tkinter.Event) -> None:
        'Sets up main board before the user makes any moves'
        self._done_int+=1
        if self._done_int == 2:
            self._done_button.grid_remove()
            self._turn_label.configure(text='Turn: '+othello_logic2.number_to_letter(self._game_state._first_player))
            self._game_state.change_turn(self._game_state._first_player)
            self._change_color = True
            self._canvas.bind('<Button-1>',self.run_othello)
            if self._change_color:
                list_of_deltas = [[-1,0],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[0,1],[-1,1]]
                #print('xxxx')
                #print(self._game_state.valid_move_left(self._game_state.return_turn(), self._rows, self._cols, list_of_deltas))
                #othello_logic2.print_board(self._game_state.return_board())
                if not self._game_state.valid_move_left(self._game_state.return_turn(), self._rows, self._cols, list_of_deltas) \
                    and self._game_state.valid_move_left(othello_logic2.opposite(self._game_state.return_turn()), self._rows, self._cols, list_of_deltas):
                    #print('lolx')
                    self._game_state.change_turn(othello_logic2.opposite(self._game_state.return_turn()))
                    self._turn_label.configure(text = 'No turn available for '+othello_logic2.number_to_letter(othello_logic2.opposite(self._game_state.return_turn()))+' so, Turn: ' +othello_logic2.number_to_letter(self._game_state.return_turn()))
                if not self._game_state.valid_move_left(self._game_state.return_turn(),self._rows,self._cols,list_of_deltas) \
                   and not self._game_state.valid_move_left(othello_logic2.opposite(self._game_state.return_turn()), self._rows, self._cols, list_of_deltas):
                    #print('ok')
                    text= str('WINNER: '+othello_logic2.number_to_letter(othello_logic2.get_winner(self._win_determiner,self._game_state.count())))
                    self._turn_label.configure(text=text)
                    return
            return self._change_color
        self._game_state.change_turn(othello_logic2.opposite(self._game_state.return_turn()))
        self._turn_label.configure(text=othello_logic2.number_to_letter(self._game_state.return_turn())+' choose spots for discs then press Done',font=('Comic Sans MS',12))

        return False
    
        
    def draw_grid(self,event:tkinter.Event) -> None:
        'Draws rectangles cooresponding to the width and height of the canvas at the specific event'
        self._canvas.delete('r')
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()
        for r in range(0,self._rows):
            for c in range(0,self._cols):
                coor = coordinate.Coordinate(self._canvas_width,self._canvas_height,self._rows,self._cols) #change into coordinate class
                l=self._canvas.create_rectangle(coor.return_scaled_coords(r,c), tag='r')
                self._list_of_rect.append(l)
                self._dictionary_rect[r,c] = l

        #print(self._canvas.coords(l))
        #print('LOL',self._canvas_width)
        self._canvas.highlightthickness=0
        if self._change_color != True:
            self._canvas.bind('<Button-1>',self.on_click) #MOVE THIS
        else:
            self._canvas.bind('<Button-1>',self.run_othello)
        self.if_changed(event)
        
    def run_othello(self, event:tkinter.Event) -> None:
        'Main othello code that handles the clicking of each turn on the canvas'
        if self._done_int == 2:
            self._game_state.change_turn(self._game_state._first_player)
            self._turn_label.configure(text='Turn: '+othello_logic2.number_to_letter(self._game_state.return_turn()))
            self._done_int +=1
        continues=False
        list_of_changes=[]
        list_of_deltas = [[-1,0],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[0,1],[-1,1]]

        count = self._game_state.count()
        self._color_count.configure(text='B: '+str(count[0])+' W: '+str(count[1]))
        self._color_count.grid(row=5, column=0, padx=10,pady=10,sticky=tkinter.W)
        
         
        if self._game_state.board_capacity_checker():
            text= str('WINNER: '+othello_logic2.number_to_letter(othello_logic2.get_winner(self._win_determiner,count)))
            self._turn_label.configure(text=text)                                                  #KEEPS SAYING WINNER WHEN NO WINNER
            return
        if not self._game_state.valid_move_left(self._game_state.return_turn(),self._rows, self._cols, list_of_deltas):
        
            self._game_state.change_turn(othello_logic2.opposite(self._game_state.return_turn()))
          
            #print('yo')
            if not self._game_state.valid_move_left(self._game_state.return_turn(),self._rows, self._cols, list_of_deltas):
                #print('oyo')
                text= str('WINNER: '+othello_logic2.number_to_letter(othello_logic2.get_winner(self._win_determiner,count)))
                self._turn_label.configure(text=text)
                self._canvas.bind('<Button-1>',print)
                return
            else:
               
                self._turn_label.configure(text = 'No turn available for '+othello_logic2.number_to_letter(othello_logic2.opposite(self._game_state.return_turn()))+ 
                                           ' so, Turn: ' +othello_logic2.number_to_letter(self._game_state.return_turn()))
        
        x=event.x
        y=event.y
        
        coor = coordinate.Coordinate(self._canvas.winfo_width(),self._canvas.winfo_height(),self._rows, self._cols)
        
        x_coor = coor.return_grid_x(x)
        y_coor = coor.return_grid_y(y)

        if self._game_state.return_board()[y_coor][x_coor] != 0:
            return
        untouched=0
        if self._game_state.is_valid_move(self._game_state.return_turn(),y_coor,x_coor,self._rows,self._cols,list_of_deltas):

            for deltas in list_of_deltas:
                if self._game_state.check_sequence(self._game_state.return_turn(),y_coor,x_coor,deltas[0],deltas[1],self._rows,self._cols):
                    color_count_before = self._game_state.count()
                    #othello_logic2.print_board(self._game_state.return_board())
                    test=self._game_state.make_move(self._game_state.return_turn(),y_coor,x_coor,deltas[0],deltas[1], self._rows, self._cols)
                    #print('next')
                    #othello_logic2.print_board(self._game_state.return_board())
                    color_count_after = self._game_state.count()
                    
                            
                    if color_count_before != color_count_after:
                        untouched+=1                                  #doesnt work, i tihnk its somewhere in the code above that it doesnt change
                        list_of_changes.append(test)                                              #game_state board and doesnt accept any click as valid
                       # print(list_of_changes)   
                        continues=True
       # print('u',untouched)
        if untouched !=0:
            untouched = 0# something wrong here
            self._game_state.return_board()[y_coor][x_coor]=self._game_state.return_turn()
            list_of_changes[0].append([y_coor,x_coor])
            #print(list_of_changes)
            x,y = coor.return_coords_given_grid([x_coor,y_coor])
            #print('RUN OTHELLO',x,y)
            self._canvas_width = self._canvas.winfo_width()
            self._canvas_height = self._canvas.winfo_height()
            #temp = self._canvas.create_oval(x,y,x+int(self._canvas_width/self._cols),y+int(self._canvas_height/self._rows),fill=self.color_filled()) change back
            temp = self._canvas.create_oval(self._canvas.coords(self._dictionary_rect[y_coor,x_coor]), fill=self.color_filled())
            self._dictionary[x_coor,y_coor] = temp
            self._list_of_ovals.append(temp)
            self._list_of_orig.append((x,y,self._canvas_width,self._canvas_height))
            for l in list_of_changes:
                        for coor in l:
                            
                            fill=self.color_filled()
                            self._canvas.itemconfig(self._dictionary[coor[1],coor[0]],fill=fill)
           
        self._covered_spaces= []
        
        self._game_state.change_turn( othello_logic2.opposite(self._game_state.return_turn()))
        if continues:
            self.on_click(event)
           
        self._game_state.change_turn(othello_logic2.opposite(self._game_state.return_turn()))        
        self._turn_label.configure(text = 'Turn: ' +othello_logic2.number_to_letter(self._game_state.return_turn()))
        count = self._game_state.count()
        self._color_count.configure(text='B: '+str(count[0])+' W: '+str(count[1]))
        #print('herereree')
        if not self._game_state.valid_move_left(self._game_state.return_turn(), self._rows, self._cols, list_of_deltas) \
            and self._game_state.valid_move_left(othello_logic2.opposite(self._game_state.return_turn()), self._rows, self._cols, list_of_deltas):
            self._game_state.change_turn(othello_logic2.opposite(self._game_state.return_turn()))
            self._turn_label.configure(text = 'No turn available for '+othello_logic2.number_to_letter(othello_logic2.opposite(self._game_state.return_turn())) \
                                       +' so, Turn: ' +othello_logic2.number_to_letter(self._game_state.return_turn()))
        if not self._game_state.valid_move_left(othello_logic2.opposite(self._game_state.return_turn()), self._rows, self._cols, list_of_deltas) \
           and not self._game_state.valid_move_left(self._game_state.return_turn(), self._rows, self._cols, list_of_deltas):
            text= str('WINNER: '+othello_logic2.number_to_letter(othello_logic2.get_winner(self._win_determiner,count)))
            self._turn_label.configure(text=text)
            
    

    def color_filled(self) -> str:
        'Returns string corresponding to the color to be filled into the disc'
        if self._game_state.return_turn() == 1:
            return 'black'
        if self._game_state.return_turn() == 2:
            return 'white'
        
    def on_click(self,event: tkinter.Event) -> None:
        'Handles changing of the label, creation of ovals before & after game starts where black and white input the original board'
        
        self._color_count.grid(row=5, column=0, padx=10,pady=10,sticky=tkinter.W)

        
        if self._change_color:
            if self._done_int == 2:
                self._game_state.change_turn(self._first_player)
                self._done_int+=1
               
                self._turn_label.configure(text='Turn: '+othello_logic2.number_to_letter(self._game_state.return_turn()))
            else:
                self._game_state.change_turn(othello_logic2.opposite(self._game_state.return_turn()))

                self._turn_label.configure(text='Turn: '+othello_logic2.number_to_letter(self._game_state.return_turn()))
        
        fill=self.color_filled()
        x = event.x
        y =event.y
        

        
        coor = coordinate.Coordinate(self._canvas.winfo_width(),self._canvas.winfo_height(),self._rows, self._cols)
        
        x_coor = coor.return_grid_x(x)
        y_coor = coor.return_grid_y(y)

        x,y = coor.return_coords_given_grid([x_coor,y_coor])
        
        #print('xcoor',x,'ycoor',y)
        if self._game_state.return_board()[y_coor][x_coor] != 0:
            return
            
        self._game_state.return_board()[y_coor][x_coor] = self._game_state.return_turn()
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()
        #temp = self._canvas.create_oval(x,y,x+int(self._canvas_width/self._cols),y+int(self._canvas_height/self._rows),fill=fill) change back
        temp = self._canvas.create_oval(self._canvas.coords(self._dictionary_rect[y_coor,x_coor]),fill=fill)
        self._dictionary[x_coor,y_coor] = temp
        self._list_of_ovals.append(temp)
        self._list_of_orig.append((x,y,self._canvas_width,self._canvas_height,temp,x_coor,y_coor))
       
        self._canvas.bind('<Configure>',self.if_changed, add='+')
        
       
        count = self._game_state.count()
        self._color_count.configure(text='B: '+str(count[0])+' W: '+str(count[1]))
        
    def if_changed(self, event: tkinter.Event)-> None:
        'If the canvas size is changed changes the size of the ovals and rectangles'
        #print('k',self._list_of_ovals)
       
        for l in range(len(self._list_of_ovals)):

            x=self._list_of_orig[l][0]
            y=self._list_of_orig[l][1]
            current_width=self._list_of_orig[l][2]
            current_height=self._list_of_orig[l][3]
            coor = coordinate.Coordinate(current_width, current_height, self._rows,self._cols)
            
            
            new_x=(1/self._cols)*coor.return_grid_x(x)*round(self._canvas_width,-1)
            new_y=(1/self._rows)*coor.return_grid_y(y)*round(self._canvas_height,-1)
        
            self._canvas.coords(self._list_of_ovals[l],new_x,new_y,new_x+int(self._canvas_width/self._cols),new_y+int(self._canvas_height/self._rows))
        count = self._game_state.count()
        self._color_count.configure(text='B: '+str(count[0])+' W: '+str(count[1]))
        
class Dialog:
    'Dialog before the board appears that asks user for the inputs needed to play game'
    
    def __init__(self) -> None:
        'Initializes all the labels, buttons, error dialogs, and entry fields in the window'
        self._error = tkinter.Tk()
        self._error.title('Error!')
        self._error.withdraw()
        self._error.protocol('WM_DELETE_WINDOW', self.hide)
        
        self._first_player=0
        self._win_determiner=0
        self._dialog = tkinter.Tk()
        self._dialog.protocol('WM_DELETE_WINDOW',self.quit)
        
        self._is_destroyed=False
        
        self._dialog.rowconfigure(3, weight = 1)
        self._dialog.columnconfigure(2, weight = 1)

        self.row_label = tkinter.Label(master=self._dialog, text='Rows:')
        self.row_label.grid(row=1,column=0,padx=10,pady=10, sticky = tkinter.E+tkinter.S+tkinter.N+tkinter.W)
        
        self.col_label = tkinter.Label(master=self._dialog, text='Cols:')
        self.col_label.grid(row=2,column=0,padx=10,pady=10, sticky = tkinter.E+tkinter.S+tkinter.N+tkinter.W)
        
        self.row_entry = tkinter.Entry(
            master = self._dialog, text = 'Rows')
        self.row_entry.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = tkinter.E+tkinter.S+tkinter.N+tkinter.W)
        
        self.col_entry = tkinter.Entry(
            master = self._dialog, text = 'Cols')
        self.col_entry.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = tkinter.E+tkinter.S+tkinter.N+tkinter.W)

        first = tkinter.Label(master=self._dialog, text='Which player goes first:')
        first.grid(row=3,column=0,padx=10,pady=10, sticky = tkinter.E+tkinter.S+tkinter.N+tkinter.W)

        button_frame = tkinter.Frame(master=self._dialog)
        button_frame.grid(row=3,column=1,padx=10,pady=10,sticky=tkinter.W+tkinter.E)
        
        black_button = tkinter.Button(master=button_frame,text='B',command=lambda: self.first_player_tog(1, self._buttons))
        self._orig_color = black_button.cget("background")
        #black_button.bind('<Button-1>',lambda: self.change_color(black_button))
        black_button.grid(
            row = 3, column = 1, padx = 10, pady = 10,sticky=tkinter.W)
        
        white_button = tkinter.Button(master=button_frame,text='W',command=lambda: self.first_player_tog(2, self._buttons))
        white_button.grid(
            row = 3, column = 2, padx = 10, pady = 10, sticky=tkinter.W)

        self._buttons = [black_button,white_button]
        
        button_frame1 = tkinter.Frame(master=self._dialog)
        button_frame1.grid(row=4,column=0,padx=10,pady=10,sticky=tkinter.W+tkinter.E)

        relational_label = tkinter.Label(master=button_frame1,text='Who wins:')
        relational_label.grid(row = 4, column = 0, padx=10,pady=10, sticky=tkinter.W)
        
        rel_button1 = tkinter.Button(master=button_frame1,text='Player with most dics', command=lambda: self.who_wins_tog(1,self._rel_buttons))
        rel_button1.grid(row=4,column=1,padx=10,pady=10,sticky=tkinter.W)

        rel_button2 = tkinter.Button(master=button_frame1,text='Player with least discs', command=lambda: self.who_wins_tog(2,self._rel_buttons))
        rel_button2.grid(row=4,column=2,padx=10,pady=10,sticky=tkinter.W)

        self._rel_buttons=[rel_button1, rel_button2]

        ok_buttonf = tkinter.Frame(master=self._dialog)
        ok_buttonf.grid(row=5,column=0,padx=10,pady=10)
        
        ok_button = tkinter.Button(master=ok_buttonf,text='OK', command=self.finalize)
        ok_button.grid(row=5,column=3,padx=50,pady=10,sticky=tkinter.S)
        
        
        
    def quit(self) -> None:
        'Destroys main dialog and sets a boolean so that it destroys tkinter objects that are hidden so program terminates'
        self._dialog.destroy()
        self._is_destroyed = True

    def first_player_tog(self,index: int, buttons) -> None:
        '''If player clicks on a certain button, the value of the associated button is stored in index, and changes color of the
        button to indicate that it was clicked'''
        self._first_player=index
        self.change_color(index,buttons)
        
    def who_wins_tog(self,index: int, buttons) -> None:
        '''If player clicks on a certain button, the value of the associated button is stored in index, and changes color of the
        button to indicate that it was clicked'''
        if index == 1:
            self._win_determiner='>'
        if index == 2:
            self._win_determiner='<'
        self.change_color(index,buttons)
        
    def change_color(self,index: int,buttons)-> None:
        'Actually does the changing of the color for the buttons when the chosen, and removes color off the non clicked button'
        buttons[index-1].configure(bg='blue')
        buttons[othello_logic2.opposite(index)-1].configure(bg=self._orig_color)
        #self._first_player = index
        #print(self._first_player)

        
    def finalize(self) -> None:
        'When the OK button is pressed, finalizes and gets input from entry, prompting errors if they exist'
        #print('First player:',self._first_player)
        #print('Win Determiner:',self._win_determiner)
        if self._first_player == 0 or self._win_determiner == 0:
            self._error.deiconify()
            error_label = tkinter.Label(master=self._error,text='ERROR: Must select \'first player\' and \'who wins\' options')
            error_label.grid(row=2,column=2,sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
        else:
            try:
                self._rows=int(self.row_entry.get())
                self._cols=int(self.col_entry.get())
                if ((self._rows < 4 or self._rows > 16) or (self._cols < 4 or self._rows > 16) or self._rows % 2 !=0 or self._cols % 2 != 0):
                    error_label = tkinter.Label(master=self._error,text='Error in input for row/col. Must be an even integer between 4 and 16 inclusive.')
                    error_label.grid(row=2,column=2,sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
                    self._error.deiconify()
                else:
                    self._dialog.destroy()
            except ValueError:
                self._error.deiconify()
                error_label = tkinter.Label(master=self._error,text='Error in input for row/col. Must be an even integer between 4 and 16 inclusive.')
                error_label.grid(row=2,column=2,sticky=tkinter.N+tkinter.S+ tkinter.E+ tkinter.W)

    def hide(self) -> None:
        'Hides the error screen when someone presses the X'
        self._error.withdraw() 
                        
def run_user_interface() -> None:
    'Runs main GUI and goes to board if the dialog isn\'t closed in the middle so the values can be processed'
    d = Dialog()
    d._dialog.grab_set()
    d._dialog.wait_window()
    if not d._is_destroyed:
        x=Board(d._rows,d._cols,d._first_player,d._win_determiner)
        x._window.protocol('WM_DELETE_WINDOW',lambda: x.quit(d))
        x.run()
   # x._window.protocol('WM_DELETE_WINDOW',lambda: self.quit(d))
    

if __name__ == '__main__':
    run_user_interface()
