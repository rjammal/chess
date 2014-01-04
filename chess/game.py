import chess

class ChessGame:

    def __init__(self):

        self.board = chess.Board()
        self.white_turn = True
        self.score = {'Player1':0, 'Player2':0}

    def get_board(self):
        return self.board
    def get_turn_color(self):
        if self.white_turn:
            return "White"
        else:
            return "Black"

    def move(self, piece, new_x, new_y):
        board = self.get_board()
        x = piece.get_x()
        y = piece.get_y()
        if self.get_turn_color() == piece.get_color():
            board.board_move(piece, new_x, new_y)
        if (x != piece.get_x() or
            y != piece.get_y()):
            self.white_turn = not self.white_turn
