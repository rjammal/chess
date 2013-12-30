# Testing if bishop movement works
import chess
from chess import *

board = Board()

# seed data
bishop = board.get_piece(2, 0)
bishop.move(2, 4)


def test_movement(piece, coord, board, expected_value):
    valid_move = piece.is_valid_move(coord[0], coord[1], board)
    if expected_value == valid_move:
        return "\tPASS"
    else:
        return "\tFAIL"


test_coords = {(3, 5): True,
               (4, 6): True,
               (5, 7): False,
               (0, 2): True,
               (2, 2): False,
               (17, 23): False,
               (3, 2): False,
               (3, 3): True,
               (3, 7): False,
               (5, 5): False
               }

for coord in test_coords:
    expected_value = test_coords[coord]
    print(str(coord) + ":", test_movement(bishop, coord, board, expected_value))
    
