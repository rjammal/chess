# Testing if pawn movement works
import chess
from chess import *

board = Board()

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

white_pawn = board.get_piece(1,6)
test_coords_white = {(1, 5): True,
                     (1, 6): False,
                     (1, 7): False,
                     (1, 4): True,
                     (1, 3): False,
                     (2, 5): False}

for coord in test_coords_white:
    expected_value = test_coords_white[coord]
    print(str(coord) + ":", test_movement(white_pawn, coord, board, expected_value))


black_pawn.move(0,7)
black_pawn.promote(board, Queen)
print(str(board))
