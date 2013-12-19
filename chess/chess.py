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

    # return list of black pieces
    def get_black(self):
        return self.list_black
    # return list of white pieces
    def get_white(self):
        return self.list_white
    # return all pieces on the board
    def get_all_pieces(self):
        piece_list = []
        piece_list.extend(self.get_black())
        piece_list.extend(self.get_white())
        return piece_list
    # return the piece at a specified location
    def get_piece(self, x, y):  
        for piece in self.get_all_pieces():
            if x == piece.get_x() and y == piece.get_y():
                return piece
    # remove piece from the board
    def remove_piece(self, piece):
        if piece.get_color() == "Black":
            self.list_black.remove(piece)
        elif piece.get_color() == "White":
            self.list_white.remove(piece)
    # add piece to the board
    def add_piece(self, piece):
        if piece.get_color() == "Black":
            self.list_black.append(piece)
        elif piece.get_color() == "White":
            self.list_white.append(piece)
    # returns True if a spot is empty, False if occupied  
    def is_empty(self, x, y):
        for piece in self.get_all_pieces():
            if x == piece.get_x() and y == piece.get_y():
                return False
        return True 

class ChessPiece():

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

    def __init__(self, x, y, color):
        super(Knight, self).__init__(x, y, color)

    def move(self, new_x, new_y):
        super(Knight, self).move(new_x, new_y)

    def is_valid_move(self, new_x, new_y, board):

        # check if new location is on board
        if not super(Knight, self).is_valid_move(new_x, new_y, board):
            print('a')
            return False

        x = self.get_x()
        y = self.get_y()

        # check for Knight 'L' move
        if not ((abs(new_x - x) == 2 and abs(new_y - y) == 1) or \
           (abs(new_x - x) == 1 and abs(new_y - y) == 2)):
            print('b')
            return False
        # check if new location is open                   
        elif board.is_empty(new_x, new_y):
            print('c')
            return True
        # if new location is already taken
        else:
            piece_in_new_location = board.get_piece(new_x, new_y)

            # check for opposite color in occupied spot in order to capture
            if self.get_color() != piece_in_new_location.get_color():
                print('d')
                piece_in_new_location.set_captured()
                return True
            # if same color, cannot move into the same spot
            else:
                print('e')
                return False


class Rook(ChessPiece):
    pass # Cyrus

class Bishop(ChessPiece):
    pass # Rosemary

class Queen(Bishop):
    pass # Rosemary

class King(ChessPiece):
    pass # Cyrus

