import tkinter as tk
import chess

SQUARE_SIZE = 50
HEIGHT = SQUARE_SIZE * chess.BOARD_SIZE
WIDTH = SQUARE_SIZE * chess.BOARD_SIZE

class ChessGUI(tk.Frame):
    def __init__(self, master = None):

        tk.Frame.__init__(self, master)

        self.grid()
        self.canvas = tk.Canvas(self, height = HEIGHT, width = WIDTH)
        self.canvas.grid()
        self.draw_board()

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


chess_gui = ChessGUI()

chess_gui.master.title('Chess')

chess_gui.mainloop()
