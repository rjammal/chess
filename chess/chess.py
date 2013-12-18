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

    def remove_piece(self, piece):
        if piece.get_color() == "Black":
            self.list_black.remove(piece)
        elif piece.get_color() == "White":
            self.list_white.remove(piece)
    def add_piece(self, piece):
        if piece.get_color() == "Black":
            self.list_black.append(piece)
        elif piece.get_color() == "White":
            self.list_white.append(piece)
      
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
    
    def move(self, new_x, new_y):
        self.set_x(new_x)
        self.set_y(new_y)

    def is_valid_move(self, new_x, new_y, board):
        x_on_board = 0 <= new_x < BOARD_SIZE
        y_on_board = 0 <= new_y < BOARD_SIZE
        return x_on_board and y_on_board

    

class Pawn(ChessPiece):

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color)
        self.not_yet_moved = True
        self.enpassant = False

    def move(self, new_x, new_y):
        super(Pawn, self).move(new_x, new_y)
        self.not_yet_moved = False

    def is_valid_move(self, new_x, new_y, board):
        # if the new location isn't on the board, exit immediately
        if not super(Pawn, self).is_valid_move(new_x, new_y, board):
            return False
        
        x = self.get_x()
        y = self.get_y()
        black = self.get_color() == "Black"
        white = self.get_color() == "White"

        moving_forward = x == new_x

        if moving_forward:
            # check if spot ahead is empty
            if not board.is_empty(x, y + 1):
                return False
            if self.not_yet_moved:
                if black:
                    valid_y = ((y + 1) == new_y or
                               (y + 2) == new_y)
                elif white:
                    valid_y = ((y - 1) == new_y or
                               (y - 2) == new_y)

        
        if board.is_empty(new_x, new_y):
            same_x = x == new_x
            if self.not_yet_moved:
                if black:
##                    # check if spot ahead is empty
##                    if not board.is_empty(x, y + 1):
##                        return False
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

    def in_promotion_space(self):
        if self.get_color() == "White":
            return self.get_y() == 0
        elif self.get_color() == "Black":
            return self.get_y() == BACK_ROW

    def promote(self, board, new_type):
        if self.in_promotion_space():
            x = self.get_x()
            y = self.get_y()
            color = self.get_color()
            board.remove_piece(self)
            new_piece = new_type(x, y, color) 
            board.add_piece(new_piece)

    
            

class Knight(ChessPiece):
    pass # Cyrus

class Rook(ChessPiece):
    pass # Cyrus

class Bishop(ChessPiece):
    pass # Rosemary

class Queen(Bishop):
    pass # Rosemary

class King(ChessPiece):
    pass # Cyrus


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

# dictionary where the spaces on the board map to whether or not my
# pawn should be able to move there
test_coords = {(1, 2): True,
               (1, 3): True,
               (1, 4): False,
               (0, 2): False,
               (2, 2): True,
               (17, 23): False
               }

for coord in test_coords:
    expected_value = test_coords[coord]
    print(str(coord) + ":", test_movement(black_pawn, coord, board, expected_value))
    
black_pawn.move(0,7)
black_pawn.promote(board, Queen)
print(str(board))
