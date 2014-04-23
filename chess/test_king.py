# testing if king works
import unittest
import chess
from chess import *


#seed_data
#black_king = board.get_piece(3, 0)
#black_king.move(2, 5)

class KingTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.black_king = self.board.get_piece(3, 0)

    def test_in_check(self):
        self.assertFalse(self.black_king.in_check(self.board))
        self.black_king.move(2, 5)
        self.assertTrue(self.black_king.in_check(self.board))
        self.black_king.move(5, 3)
        bishop = self.board.get_piece(2, 7)
        bishop.move(4, 4)
        self.assertTrue(self.black_king.in_check(self.board))
        self.black_king.move(6, 2)
        self.assertTrue(self.black_king.in_check(self.board))
        self.black_king.move(6, 3)
        self.assertFalse(self.black_king.in_check(self.board))


if __name__ == '__main__':
    unittest.main()
