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
            self.list_black.append(Pawn(i, FRONT_ROW + 1, "Black"))
            self.list_white.append(Pawn(i, BACK_ROW - 1, "White"))

        # rooks
        for x in [LEFT_COLUMN, RIGHT_COLUMN]:
            self.list_black.append(Rook(x, FRONT_ROW, "Black"))
            self.list_white.append(Rook(x, BACK_ROW, "White"))

        # knights
        for x in [LEFT_COLUMN + 1, RIGHT_COLUMN - 1]:
            self.list_black.append(Knight(x, FRONT_ROW, "Black"))
            self.list_white.append(Knight(x, BACK_ROW, "White"))

        # bishops
        for x in [LEFT_COLUMN + 2, RIGHT_COLUMN - 2]:
            self.list_black.append(Bishop(x, FRONT_ROW, "Black"))
            self.list_white.append(Bishop(x, BACK_ROW, "White"))

        # queens
        self.list_black.append(Queen(RIGHT_COLUMN - 3, FRONT_ROW, "Black"))
        self.list_white.append(Queen(RIGHT_COLUMN - 3, BACK_ROW, "White"))

        # kings
        self.list_black.append(King(RIGHT_COLUMN - 4, FRONT_ROW, "Black"))
        self.list_white.append(King(RIGHT_COLUMN - 4, BACK_ROW, "White"))

    def __str__(self):
        print_string = ""
        for piece in self.get_all_pieces():
            print_string += str(piece) + '\n'
        return print_string

    def get_black(self):
        return self.list_black
    def get_white(self):
        return self.list_white
    def get_all_pieces(self):
        piece_list = []
        piece_list.extend(self.get_black())
        piece_list.extend(self.get_white())
        return piece_list
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

    def __str__(self):
        return (self.get_color() + " " + str(self.__class__.__name__) +
                " (" + str(self.get_x()) + ", " + str(self.get_y()) + ")")

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
        self.set_x(new_x)
        self.set_y(new_y)

    def is_valid_move(self, new_x, new_y, board):
        if new_x < 0 or new_x >= BOARD_SIZE:
            return False
        if new_y < 0 or new_y >= BOARD_SIZE:
            return False
        return True

    

class Pawn(ChessPiece):

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color)
        self.not_yet_moved = True

    def move(self, new_x, new_y):
        super(Pawn, self).move(new_x, new_y)
        self.not_yet_moved = False

    def is_valid_move(self, new_x, new_y, board):
        if not super(Pawn, self).is_valid_move(new_x, new_y, board):
            return False
        
        x = self.get_x()
        y = self.get_y()
        black = self.get_color() == "Black"
        white = self.get_color() == "White"

        
        if board.is_empty(new_x, new_y):
            same_x = x == new_x
            if self.not_yet_moved:
                if black:
                    valid_y = ((y + 1) == new_y or
                               (y + 2) == new_y)
                elif white:
                    valid_y = ((y - 1) == new_y or
                               (y - 2) == new_y)
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

            capture_piece = left_or_right_one and one_row_ahead and opposite_color_in_destination

            if capture_piece:
                piece_in_new_location.set_captured()

            return capture_piece

         

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


board = Board()
print(board)

# Testing if moving works

# seed data
white_pawn = Pawn(2, 2, "White")
board.get_white().append(white_pawn)
black_pawn = board.get_piece(1, 1)


def test_movement(piece, coord, board, expected_value):
    valid_move = piece.is_valid_move(coord[0], coord[1], board)
    if expected_value == valid_move:
        return "\tPASS"
    else:
        return "\tFAIL"
        
test_coords = {(1, 2): True,
               (1, 3): True,
               (1, 4): False,
               (0, 2): False,
               (2, 2): True
               }

for coord in test_coords:
    expected_value = test_coords[coord]
    print(str(coord) + ":", test_movement(black_pawn, coord, board, expected_value))
    

