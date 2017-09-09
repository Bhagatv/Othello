class Coordinate:
    'Class that deals with the coordinate systems so the resizing of the canvas can be dealt with'
    def __init__(self,total_width,total_height,rows,cols) -> None:
        'Initializes the total width into variables to be used into fractional coordinates'
        self._canvas_width = total_width
        self._canvas_height = total_height
        self._rows = rows
        self._cols = cols

    def return_scaled_coords(self,scale_row, scale_col: int) -> tuple:
        'Returns tuple of the scaled coordinates with respect to the index in the 2D list'
        result = (int((1/self._cols)*scale_col*round(self._canvas_width,-1)),int((1/self._rows)*scale_row*round(self._canvas_height,-1)),
                  int((1/self._cols)*(1+scale_col)*round(self._canvas_width,-1)),\
                  int((1/self._rows)*(scale_row+1)*round(self._canvas_height,-1)))
        return result

    def return_grid_x(self, clicked_pos: int) -> int:
        'Returns the x index if the board were a GUI representative of a 2D list'
        return int(clicked_pos/(self._canvas_width/self._cols))

    def return_grid_y(self,clicked_pos: int) -> int:
        'Returns the y index if the board were a GUI representative of a 2D list'
        return int(clicked_pos/(self._canvas_height/self._rows))

    def return_coords_given_grid(self, grid_coors: [int]) -> [float]:
        'Returns the actual coordinates in the canvas given the index representatives (grid coords)'
        return [grid_coors[0]*(self._canvas_width/self._cols),grid_coors[1]*(self._canvas_height/self._rows)]
    
    
        
