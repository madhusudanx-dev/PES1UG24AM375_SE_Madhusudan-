import unittest
from unittest.mock import patch

from board import Board


class BoardMergeTests(unittest.TestCase):
    def make_board(self, first_row):
        with patch.object(Board, "add_random_tile"):
            board = Board()
        board.grid = [first_row[:], [0] * 4, [0] * 4, [0] * 4]
        return board

    def test_four_equal_tiles_merge_as_two_pairs(self):
        self.assertEqual(Board.slide_line([2, 2, 2, 2]), [4, 4, 0, 0])

    def test_new_tile_cannot_merge_again_in_the_same_move(self):
        self.assertEqual(Board.slide_line([2, 2, 4, 0]), [4, 4, 0, 0])

    def test_separated_equal_tiles_compress_then_merge(self):
        self.assertEqual(Board.slide_line([2, 0, 2, 4]), [4, 4, 0, 0])

    def test_move_adds_only_the_value_of_new_tiles_to_score(self):
        board = self.make_board([2, 2, 4, 0])

        self.assertTrue(board.move_left())
        self.assertEqual(board.grid[0], [4, 4, 0, 0])
        self.assertEqual(board.score, 4)
        self.assertEqual(board.last_merge_score, 4)
        self.assertEqual(board.last_merge_count, 1)


if __name__ == "__main__":
    unittest.main()
