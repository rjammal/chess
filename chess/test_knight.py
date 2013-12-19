import chess
from chess import *



black_knight = board.get_piece(1,0)


def test_movement(piece, coord, board, expected_value):
    valid_move = piece.is_valid_move(coord[0], coord[1], board)
    if expected_value == valid_move:
        return "\tPASS"
    else:
        return "\tFAIL"

# dictionary where the spaces on the board map to whether or not my
# knight should be able to move there
test_coords = {(2, 2): True,
               (3, 1): False,
               (0, 2): True,
               (2, 1): False,
               (-1, 1): False,
               (1, 1): False,
               (17, 23): False,
               (2, 2): True
               }

for coord in test_coords:
    expected_value = test_coords[coord]
    print(str(coord) + ":", test_movement(black_knight, coord, board, expected_value))


print(board)

    
