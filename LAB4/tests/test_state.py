import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from game import Game


class GameStateTests(unittest.TestCase):
    def make_game(self, rows=None):
        game = Game()
        game.board.grid = rows or [[0] * 4 for _ in range(4)]
        return game

    def test_reaching_2048_wins_and_does_not_spawn_another_tile(self):
        game = self.make_game([[1024, 1024, 0, 0], [0] * 4, [0] * 4, [0] * 4])
        with patch.object(game.board, "add_random_tile") as add_tile:
            self.assertTrue(game.move("a"))

        self.assertTrue(game.has_won())
        self.assertTrue(game.is_game_over())
        add_tile.assert_not_called()

    def test_full_board_without_adjacent_matches_is_game_over(self):
        rows = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        game = self.make_game(rows)

        self.assertFalse(game.board.can_move())
        self.assertTrue(game.is_game_over())

    def test_unchanged_move_does_not_spawn_a_tile(self):
        game = self.make_game([[2, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4])
        original = [row[:] for row in game.board.grid]
        with patch.object(game.board, "add_random_tile") as add_tile:
            self.assertFalse(game.move("a"))

        self.assertEqual(game.board.grid, original)
        add_tile.assert_not_called()

    def test_successful_nonwinning_move_spawns_one_tile(self):
        game = self.make_game([[0, 2, 0, 0], [0] * 4, [0] * 4, [0] * 4])
        with patch.object(game.board, "add_random_tile") as add_tile:
            self.assertTrue(game.move("a"))

        add_tile.assert_called_once_with()

    def test_run_stops_before_input_when_board_is_won(self):
        game = self.make_game([[2048, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4])
        output = StringIO()
        with patch("builtins.input", side_effect=AssertionError("input should not be requested")):
            with redirect_stdout(output):
                game.run()

        self.assertIn("You reached 2048!", output.getvalue())


if __name__ == "__main__":
    unittest.main()
