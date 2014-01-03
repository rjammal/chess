import tkinter as tk
import chess

SQUARE_SIZE = 110
HEIGHT = SQUARE_SIZE * chess.BOARD_SIZE
WIDTH = SQUARE_SIZE * chess.BOARD_SIZE

class ChessGUI(tk.Frame):
    def __init__(self, master = None):

        tk.Frame.__init__(self, master)

        self.grid()
        self.canvas = tk.Canvas(self, height = HEIGHT, width = WIDTH)
        self.canvas.grid()
        self.board = chess.Board()
        self.draw_board()
        self.draw_pieces()
        self.canvas.bind('<Button-1>', self.click_move)

        self.active_piece = None
        self.white_turn = True

    def get_board(self):
        return self.board

    def draw_board(self):

        for row in range(chess.BOARD_SIZE):
            for column in range(chess.BOARD_SIZE):
                if ((row + column) % 2) == 0:
                    color = "White"
                else:
                    color = "Black"
                self.canvas.create_polygon(column * SQUARE_SIZE, row * SQUARE_SIZE,
                                           (column + 1) * SQUARE_SIZE, row * SQUARE_SIZE,
                                           (column + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                                           column * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                                           outline = color,
                                           fill = color)

    def draw_pieces(self):

        board = self.get_board()
     
        for piece in board.get_all_pieces():
            gif = piece.get_image()
            x = int((piece.get_x() + .5) * SQUARE_SIZE)
            y = int((piece.get_y() + .5) * SQUARE_SIZE)
 
            self.canvas.create_image(x, HEIGHT - y, image = gif)

    def click_move(self, event):
        board = self.get_board()
        x_coord = event.x // SQUARE_SIZE
        y_coord = (HEIGHT - event.y) // SQUARE_SIZE

        if self.active_piece == None:
            print(x_coord, y_coord)
            if not board.is_empty(x_coord, y_coord):
                self.active_piece = board.get_piece(x_coord, y_coord)
        else:
            print(self.active_piece)
            x = self.active_piece.get_x()
            y = self.active_piece.get_y()
            board.board_move(self.active_piece, x_coord, y_coord)
            if (x != self.active_piece.get_x() or
                y != self.active_piece.get_y):
                self.active_piece = None
                self.white_turn = not self.white_turn
                self.draw_board()
                self.draw_pieces()
                
            
                


chess_gui = ChessGUI()

chess_gui.master.title('Chess')

chess_gui.mainloop()
