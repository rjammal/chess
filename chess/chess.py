# Making a chess game

BOARD_SIZE = 8

FRONT_ROW = 0
BACK_ROW = 7
LEFT_COLUMN = 0
RIGHT_COLUMN = 7

class Board:

    def __init__(self):
        self.list_black = []
        self.list_white = []

        # pawns
        for i in range(BOARD_SIZE):
            self.list_black.append(Pawn(FRONT_ROW + 1, i, "Black"))
            self.list_white.append(Pawn(BACK_ROW - 1, i, "White"))

        # rooks
        for x in [LEFT_COLUMN, RIGHT COLUMN]:
            self.list_black.append(Rook(FRONT_ROW, x, "Black"))
            self.list_white.append(Rook(BACK_ROW, x, "White"))

        # knights
        for x in [LEFT_COLUMN + 1, RIGHT_COLUMN - 1]:
            self.list_black.append(Knight(FRONT_ROW, x, "Black"))
            self.list_white.append(Knight(BACK_ROW, x, "White"))

        # bishops
        for x in [LEFT_COLUMN + 2, RIGHT_COLUMN - 2]:
            self.list_black.append(Bishop(FRONT_ROW, x, "Black"))
            self.list_white.append(Bishop(BACK_ROW, x, "White"))

        # queens
        self.list_black.append(Queen(FRONT_ROW, RIGHT_COLUMN - 3, "Black"))
        self.list_white.append(Queen(BACK_ROW, RIGHT_COLUMN - 3, "White"))

        # kings
        self.list_black.append(King(FRONT_ROW, RIGHT_COLUMN - 4, "Black"))
        self.list_white.append(King(BACK_ROW, RIGHT_COLUMN - 4, "White"))

    def get_black(self):
        return self.list_black
    def get_white(self):
        return self.list_white
    def get_all_pieces(self):
        return list(self.get_black()).extend(self.get_white())
    def get_piece(self, x, y):
        for piece in self.get_all_pieces():
            if x == piece.get_x() and y == piece.get_y():
                return piece
       
    def is_empty(self, x, y):
        for piece in self.get_all_pieces():
            if x == piece.get_x() and y == piece.get_y():
                return False
        return True 

class ChessPiece:

    def __init__(self, x, y, color):
        self.captured = False
        # location on board
        # can be 0 - 7
        self.x = x
        self.y = y
        self.color = color

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_color(self):
        return self.color

    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y
    def set_captured(self):
        self.captured = True
    
    def move(self):
        pass

    def is_valid_move(self, new_x, new_y, board):
        return False

    

class Pawn(ChessPiece):

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color)
        self.not_yet_moved = True

    def move(self, new_x, new_y):
        x = self.get_x()
        y = self.get_y()
        if self.get_color() == "Black":
            space_ahead = y + 1
            if board.is_empty(x, space_ahead):
                self.set_y(y + 1)
        elif self.get_color() == "White":
            space_ahead = y - 1
            if board.is_empty(x, space_ahead):
                self.set_y(y - 1)

    def is_valid_move(self, new_x, new_y, board):
        if new_x < 0 or new_x >= BOARD_SIZE:
            return False
        if new_y < 0 or new_y >= BOARD_SIZE:
            return False
        x = chess_piece.get_x()
        y = chess_piece.get_y()
        black = self.get_color() == "Black"
        white = self.get_color() == "White"
        
        if board.is_empty(new_x, new_y):
            same_x = x == new_x
            if self.not_yet_moved:
                if black:
                    valid_y = (y + 1 == new_y) or
                              (y + 2 == new_y)
                elif white:
                    valid_y = (y - 1 == new_y) or
                              (y - 2 == new_y)
            else:
                if black:
                    valid_y = y + 1 == new_y
                elif white:
                    valid_y = y - 1 == new_y

            return same_x and valid_y

        else:
            left_or_right_one = abs(new_x - x)
            piece_in_new_location = board.get_piece(new_x, new_y)
            new_location_piece_color = piece_in_new_location.get_color()
            if black: 
                one_row_ahead = new_y - y == 1
                opposite_color_in_destination = new_location_piece_color == "White"
            elif white:
                one_row_ahead = y - new_y == 1
                opposite_color_in_destination = new_location_piece_color == "Black"

            return left_or_right_one and one_row_ahead and opposite_color_in_destination

            
                
                

class Knight(ChessPiece):
    pass

class Rook(ChessPiece):
    pass

class Bishop(ChessPiece):
    pass

class Queen(ChessPiece):
    pass

class King(ChessPiece):
    pass

