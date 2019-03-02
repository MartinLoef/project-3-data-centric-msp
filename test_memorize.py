import unittest
import memorize

class TestMemorize(unittest.TestCase):
    
    def test_can_create_an_4_by_4_board(self):
        board = memorize.make_board(4)
        self.assertEqual(len(board),4)
    
    def test_can_create_an_6_by_6_board(self):
        board = memorize.make_board(6)
        self.assertEqual(len(board),6)
    
    def test_determine_if_board_is_square(self):
        board = memorize.make_board(4)
        self.assertEqual(len(board),len(board[0]))
    
    def test_determine_if_max_value_is_size4_times_2_divided_by_2_minus_1(self):
        board = memorize.make_board(4)
        self.assertEqual(max(map(max, board)),7)
    
    def test_determine_if_max_value_is_size6_times_2_divided_by_2_minus_1(self):
        board = memorize.make_board(6)
        self.assertEqual(max(map(max, board)),17)
    
