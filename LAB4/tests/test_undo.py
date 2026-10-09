import unittest
from unittest.mock import patch

from game import Game


class UndoTests(unittest.TestCase):
    def make_game(self, first_row, score=0):
        game = Game()
        game.board.grid = [first_row[:], [0] * 4, [0] * 4, [0] * 4]
        game.board.score = score
        return game

    def test_undo_restores_grid_and_score_without_spawning_a_tile(self):
        game = self.make_game([2, 2, 0, 0], score=10)
        original_grid = [row[:] for row in game.board.grid]
        with patch.object(game.board, "add_random_tile") as add_tile:
            self.assertTrue(game.move("a"))
            self.assertEqual(game.board.score, 14)
            self.assertEqual(game.best_score, 14)
            self.assertTrue(game.undo())

        self.assertEqual(game.board.grid, original_grid)
        self.assertEqual(game.board.score, 10)
        self.assertEqual(game.best_score, 14)
        self.assertEqual(game.board.last_merge_score, 0)
        self.assertEqual(game.board.last_merge_count, 0)
        add_tile.assert_called_once_with()

    def test_undo_is_available_for_only_one_successful_move(self):
        game = self.make_game([0, 2, 0, 0])
        with patch.object(game.board, "add_random_tile"):
            self.assertTrue(game.move("a"))
            state_after_first_move = [row[:] for row in game.board.grid]
            self.assertTrue(game.move("d"))

        self.assertTrue(game.undo())
        self.assertEqual(game.board.grid, state_after_first_move)
        self.assertFalse(game.undo())

    def test_unchanged_move_keeps_the_previous_undo_available(self):
        game = self.make_game([0, 2, 0, 0])
        original_grid = [row[:] for row in game.board.grid]
        with patch.object(game.board, "add_random_tile"):
            self.assertTrue(game.move("a"))
            self.assertFalse(game.move("a"))

        self.assertTrue(game.undo())
        self.assertEqual(game.board.grid, original_grid)

    def test_undo_without_a_successful_move_returns_false(self):
        game = self.make_game([2, 0, 0, 0])

        self.assertFalse(game.undo())


if __name__ == "__main__":
    unittest.main()
