# Making a chess game

import tkinter as tk
root = tk.Tk()

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
    # This is a separate function from remove_piece so that it is
    # easier to track how a piece is removed
    def remove_enpassant(self, piece):
        self.remove_piece(piece)
    # add piece to the board
    def add_piece(self, piece):
        if piece.get_color() == "Black":
            self.list_black.append(piece)
        elif piece.get_color() == "White":
            self.list_white.append(piece)

    # Call this function to move pieces on the board
    def board_move(self, piece, new_x, new_y):
        color = piece.get_color()
        king = self.get_king_of_color(color)
        x = piece.get_x()
        y = piece.get_y()
        
        if piece.is_valid_move(new_x, new_y, self):
            board_empty = self.is_empty(new_x, new_y)
            if not board_empty:
                captured_piece = self.get_piece(new_x, new_y)
            piece.temp_move(new_x, new_y)
            if king.in_check(self):
                piece.temp_move(x, y)
                print("King is in check!")
            else:
                # Moving piece back to check some enpassant stuff
                piece.temp_move(x, y)
                self.unset_enpassant(piece)
                if not board_empty:
                    self.remove_piece(captured_piece)
                if isinstance(piece, Pawn):
                    possible_enpassant_piece = piece.check_enpassant(self, new_x, new_y)
                    if possible_enpassant_piece:
                        self.remove_piece(possible_enpassant_piece)
                # now moving for real
                piece.move(new_x, new_y)


    def get_king_of_color(self, color):
        for piece in self.get_all_pieces():
            if (isinstance(piece, King) and color == piece.get_color()):
                return piece

    # returns all pawns of the specified color
    def get_pawns_of_color(self, color):
        pawn_list = []
        for piece in self.get_all_pieces():
            piece_color = piece.get_color()
            if isinstance(piece, Pawn) and color == piece_color:
                pawn_list.append(piece)
        return pawn_list
          # This is how you would do it in a list comprehension.
          # List comprehensions are dumb X<
##        return [piece for piece in self.get_all_pieces()
##                if isinstance(piece, Pawn) and color == piece.get_color()]

    # Sets all pawns with the same color as the input piece to be out of
    # an enpassant state
    def unset_enpassant(self, piece):
        piece_color = piece.get_color()
        pawn_list = self.get_pawns_of_color(piece_color)
        if piece in pawn_list:
            if piece.not_yet_moved: 
                pawn_list.remove(piece)
        for pawn in pawn_list:
            pawn.enpassant = False
            

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
        self.image = None

    def __str__(self):
        return (self.get_color() + " " + str(self.__class__.__name__) +
                " (" + str(self.get_x()) + ", " + str(self.get_y()) + ")")

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_color(self):
        return self.color
    def get_image(self):
        return self.image
    def get_captured(self):
        return self.captured
    

    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y
    def set_captured(self):
        self.captured = True

    def move(self, new_x, new_y):
        self.set_x(new_x)
        self.set_y(new_y)
    # this is for checking if a move puts the king in check
    # without updating state like move does
    # this should not be overridden
    def temp_move(self, new_x, new_y):
        self.set_x(new_x)
        self.set_y(new_y)

    # checks if new location is different, on the board, and (empty or occupied by the opposite color)
    def is_valid_move(self, new_x, new_y, board):
        x_on_board = 0 <= new_x < BOARD_SIZE
        y_on_board = 0 <= new_y < BOARD_SIZE
        x = self.get_x()
        y = self.get_y()
        
        # check if new location is on the board
        if x_on_board and y_on_board:

            # check if there is a change in position
            if new_x == x and new_y == y:
                return False

            # check if new location is open
            elif board.is_empty(new_x, new_y):
                return True

            # if new location is already taken
            else:
                piece_in_new_location = board.get_piece(new_x, new_y)

                # check for opposite color in occupied spot in order to capture
                if self.get_color() != piece_in_new_location.get_color():
                    return True

                # if same color, cannot move into the same spot
                else:
                    return False
                
        # exit immediately if not on board    
        else:
            return False
           

class Pawn(ChessPiece):

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color)
        self.not_yet_moved = True
        self.enpassant = False
        if color == "Black": 
            self.image = tk.PhotoImage(file = "black_pawn.gif")
        else:
            self.image = tk.PhotoImage(file = "white_pawn.gif")

    def move(self, new_x, new_y):
        if abs(self.get_y() - new_y) == 2:
            self.enpassant = True
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
        if black:
                space_ahead = y + 1
                space_two_ahead = y + 2
        elif white:
                space_ahead = y - 1
                space_two_ahead = y - 2

        if moving_forward:
            # check if spot ahead is empty
            if not board.is_empty(x, space_ahead):
                return False
            if self.not_yet_moved:
                valid_y = (new_y == space_ahead or
                           new_y == space_two_ahead)
            else:
                valid_y = space_ahead == new_y
            return valid_y
        else:
            # This is checking all capture scenarios.
            
            # Pawn cannot move more than 1 left or right
            if abs(x - new_x) > 1 or new_y != space_ahead:
                return False

            if board.is_empty(new_x, new_y):
                # check for enpassant
                # enpassant_piece may be None
                enpassant_piece = self.check_enpassant(board, new_x, new_y)
                return enpassant_piece      

            else:
                other_piece = board.get_piece(new_x, new_y)
                different_colors = other_piece.get_color() != self.get_color()
                return different_colors and new_y == space_ahead
                    
    def check_enpassant(self, board, new_x, new_y):
        y = self.get_y()
        if not board.is_empty(new_x, y): # check if there is an adjacent piece
            adjacent_piece = board.get_piece(new_x, y)
            if not isinstance(adjacent_piece, Pawn):
                return False
            if (adjacent_piece.get_color() != self.get_color() and
                adjacent_piece.enpassant):
                return adjacent_piece

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
        if color == "Black": 
            self.image = tk.PhotoImage(file = "black_knight.gif")
        else:
            self.image = tk.PhotoImage(file = "white_knight.gif")


    def move(self, new_x, new_y):
        super(Knight, self).move(new_x, new_y)

    def is_valid_move(self, new_x, new_y, board):

        # check if new location is on board, empty and/or occupied by the opposite color
        if not super(Knight, self).is_valid_move(new_x, new_y, board):
            return False

        x = self.get_x()
        y = self.get_y()

        # check for Knight 'L' move
        if ((abs(new_x - x) == 2 and abs(new_y - y) == 1) or \
           (abs(new_x - x) == 1 and abs(new_y - y) == 2)):
            return True
        else:
            return False



class Rook(ChessPiece):

    def __init__(self, x, y, color):
        super(Rook, self).__init__(x, y, color)
        self.not_yet_moved = True
        if color == "Black": 
            self.image = tk.PhotoImage(file = "black_rook.gif")
        else:
            self.image = tk.PhotoImage(file = "white_rook.gif")

    def move(self, new_x, new_y):
        super(Rook, self).move(new_x, new_y)
        self.not_yet_moved = False

    def is_valid_move(self, new_x, new_y, board):
        
        # check if new location is on board, empty and/or occupied by the opposite color
        if not super(Rook, self).is_valid_move(new_x, new_y, board):
            return False

        x = self.get_x()
        y = self.get_y()

        # check if the movement is horizontal or veritical (is_valid_move guarantees that there is a change of position)
        if abs(new_x - x) == 0 or abs(new_y - y) == 0:

            block = False

            # check vertical path
            if abs(new_x - x) == 0:
                for piece in board.get_all_pieces():
                    # check if any pieces are in the same column
                    if piece.get_x() == x:
                        # check if same-column piece is in the range of Rook movement
                        if piece.get_y() > min(y, new_y) and piece.get_y() < max(y, new_y):
                            block = True

            # check horizontal path
            elif abs(new_y - y) == 0:
                for piece in board.get_all_pieces():
                    # check if any pieces are in the same row
                    if piece.get_y() == y:
                        # check if same-row piece is in the range of Rook movement
                        if piece.get_x() > min(x, new_x) and piece.get_x() < max(x, new_x):
                            block = True

            # return True if not blocked, False if blocked
            return not block
                                                          
        # exit if not horizontal/vertical    
        else:
            return False

        
        
        

class Bishop(ChessPiece):

    def __init__(self, x, y, color):

        super(Bishop, self).__init__(x, y, color)
        if color == "Black": 
            self.image = tk.PhotoImage(file = "black_bishop.gif")
        else:
            self.image = tk.PhotoImage(file = "white_bishop.gif")


    def is_valid_move(self, new_x, new_y, board):
        # check if new location is on board, empty and/or occupied by the opposite color
        if not super(Bishop, self).is_valid_move(new_x, new_y, board):
            return False
        return (new_x, new_y) in movement_path_diagonal(self, board)

class Queen(ChessPiece):

    def __init__(self, x, y, color):
        super(Queen, self).__init__(x, y, color)
        if color == "Black": 
            self.image = tk.PhotoImage(file = "black_queen.gif")
        else:
            self.image = tk.PhotoImage(file = "white_queen.gif")


    def is_valid_move(self, new_x, new_y, board):
        # check if new location is on board, empty and/or occupied by the opposite color
        if not super(Queen, self).is_valid_move(new_x, new_y, board):
            return False
        valid_moves = movement_path_hv(self, board)
        valid_moves.extend(movement_path_diagonal(self, board))
        return (new_x, new_y) in valid_moves

class King(ChessPiece):

    def __init__(self, x, y, color):

        super(King, self).__init__(x, y, color)
        if color == "Black": 
            self.image = tk.PhotoImage(file = "black_king.gif")
        else:
            self.image = tk.PhotoImage(file = "white_king.gif")

    def in_check(self, board):
        opponent_list = []
        if self.color == "White":
            opponent_list = board.get_white()
        elif self.color == "Black":
            opponent_list = board.get_black()
        for piece in opponent_list:
            if piece.is_valid_move(self.x, self.y, board):
                return True
        return False

    def is_valid_move(self, new_x, new_y, board):
        if not super(King, self).is_valid_move(new_x, new_y, board):
            return False
        x = self.get_x()
        y = self.get_y()
        return abs(new_x - x) <= 1 and abs(new_y - y) <= 1
    
    


# helper function to determine distance moved horizontally or vertically
# useful for queen and rook
def movement_path_hv(piece, board):
    x = piece.get_x()
    y = piece.get_y()

    # list containing tuples of all valid squares
    valid_squares = []

    # did you know you can define a function within a function? Crazy! 
    def add_spots_horizontal(y, list_of_x_coords):
        new_spots = []
        for pos in list_of_x_coords:
            if board.is_empty(pos, y):
                new_spots.append((pos, y))
            elif board.get_piece(pos, y).get_color() != piece.get_color():
                new_spots.append((pos, y))
                break
            else:
                break
        return new_spots

    def add_spots_vertical(x, list_of_y_coords):
        new_spots = []
        for pos in list_of_y_coords:
            if board.is_empty(x, pos):
                new_spots.append((x, pos))
            elif board.get_piece(x, pos).get_color() != piece.get_color():
                new_spots.append((x, pos))
                break
            else:
                break
        return new_spots

    def spaces_above_or_right(x_or_y):
        return range(x_or_y + 1, BOARD_SIZE)
    def spaces_below_or_left(x_or_y):
        return range(x_or_y - 1, -1, -1)

    x_values_right = spaces_above_or_right(x)
    x_values_left = spaces_below_or_left(x)
    y_values_above = spaces_above_or_right(y)
    y_values_below = spaces_below_or_left(y)
    
    # need to call this twice for each dimension since I break out
    # of the function upon hitting another piece
    # horizontally - to right
    valid_squares.extend(add_spots_horizontal(y, x_values_right))
    # horizontally - to left
    valid_squares.extend(add_spots_horizontal(y, x_values_left))
    # vertically - up
    valid_squares.extend(add_spots_vertical(x, y_values_above))
    # vertically - down
    valid_squares.extend(add_spots_vertical(x, y_values_below))

    return valid_squares
    

# helper function to determine distance moved diagonally
# useful for queen and bishop
def movement_path_diagonal(piece, board):
    x = piece.get_x()
    y = piece.get_y()

    # list containing tuples of all valid squares
    valid_squares = []
        

    # top right
    x_right = x + 1
    y_above = y + 1
    while x_right < BOARD_SIZE and y_above < BOARD_SIZE:
        if board.is_empty(x_right, y_above):
            valid_squares.append((x_right, y_above))
            x_right += 1
            y_above += 1
        elif board.get_piece(x_right, y_above).get_color() != piece.get_color():
            valid_squares.append((x_right, y_above))
            break
        else:
            break

    # bottom right
    x_right = x + 1
    y_below = y - 1
    while x_right < BOARD_SIZE and y_below >= FRONT_ROW:
        if board.is_empty(x_right, y_below):
            valid_squares.append((x_right, y_below))
            x_right += 1
            y_below -= 1
        elif board.get_piece(x_right, y_below).get_color() != piece.get_color():
            valid_squares.append((x_right, y_below))
            break
        else:
            break

    # top left
    x_left = x - 1
    y_above = y + 1
    while x_left >= LEFT_COLUMN and y_above < BOARD_SIZE:
        if board.is_empty(x_left, y_above):
            valid_squares.append((x_left, y_above))
            x_left -= 1
            y_above += 1
        elif board.get_piece(x_left, y_above).get_color() != piece.get_color():
            valid_squares.append((x_left, y_above))
            break
        else:
            break

    # bottom left
    x_left = x - 1
    y_below = y - 1
    while x_left >= LEFT_COLUMN and y_below >= FRONT_ROW:
        if board.is_empty(x_left, y_below):
            valid_squares.append((x_left, y_below))
            x_left -= 1
            y_below -= 1
        elif board.get_piece(x_left, y_below).get_color() != piece.get_color():
            valid_squares.append((x_left, y_below))
            break
        else:
            break


    return valid_squares        




def make_photo(filename):
    return tk.PhotoImage(file = filename)


    
    
