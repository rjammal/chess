import chess

class ChessGame:

    def __init__(self):

        self.board = chess.Board()
        self.white_turn = True
        self.score = {'White':0, 'Black':0}

    def get_board(self):
        return self.board
    def get_turn_color(self):
        if self.white_turn:
            return "White"
        else:
            return "Black"

    def move(self, piece, new_x, new_y):
        if self.checkmate():
            color = self.get_turn_color()
            print(color + "is in checkmate!")
            if self.white_turn:
                self.score["Black"] += 1
            else:
                self.score["White"] += 1
        else: 
            board = self.get_board()
            x = piece.get_x()
            y = piece.get_y()
            if self.get_turn_color() == piece.get_color():
                board.board_move(piece, new_x, new_y)
            if (x != piece.get_x() or
                y != piece.get_y()):
                self.white_turn = not self.white_turn

    def checkmate(self):
        if self.white_turn:
            king = self.board.get_king_of_color("White")
            pieces = self.board.get_white()
        else: 
            king = self.board.get_king_of_color("Black")
            pieces = self.board.get_black()
        if king.in_check(self.board):
            for piece in pieces:
                for x in range(chess.BOARD_SIZE):
                    for y in range(chess.BOARD_SIZE):
                        current_x = piece.get_x()
                        current_y = piece.get_y()
                        if piece.is_valid_move(x, y, board): 
                            piece.temp_move(x, y)
                            if not king.in_check(self.board):
                                return False
            return True
        return False
