# Testing if Rook movement works
import chess
from chess import *

board = Board()

# seed data
white_rook = board.get_piece(7, 7)
# move into the middle of the board to test movement
white_rook.move(4,4)


def test_movement(piece, coord, board, expected_value):
    valid_move = piece.is_valid_move(coord[0], coord[1], board)
    if expected_value == valid_move:
        return "\tPASS"
    else:
        return "\tFAIL"

# dictionary where the spaces on the board map to whether or not my
# Rook should be able to move there
test_coords = {(0, 4): True,
               (7, 4): True,
               (4, 1): True,
               (4, 5): True,
               (5, 5): False,
               (3, 5): False,
               (1, 23): False,
               (4, 2): True
               }

for coord in test_coords:
    expected_value = test_coords[coord]
    print(str(coord) + ":", test_movement(white_rook, coord, board, expected_value))

print(board)
board.board_move(white_rook, 1, 4)
print(white_rook)
    
