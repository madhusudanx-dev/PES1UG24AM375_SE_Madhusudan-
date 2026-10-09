import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from board import Board
from game import Game


class MoveFeedbackTests(unittest.TestCase):
    def make_game(self, first_row):
        game = Game()
        game.board.grid = [first_row[:], [0] * 4, [0] * 4, [0] * 4]
        return game

    def test_successful_move_reports_direction_once(self):
        game = self.make_game([0, 2, 0, 0])
        with patch.object(game.board, "add_random_tile"):
            self.assertTrue(game.move("a"))

        self.assertEqual(game.last_feedback, "Moved left.")

    def test_merge_feedback_is_action_level_and_printed_once(self):
        game = self.make_game([2, 2, 0, 0])
        output = StringIO()
        with patch.object(game.board, "add_random_tile"):
            with patch("builtins.input", side_effect=["a", "q"]):
                with redirect_stdout(output):
                    game.run()

        message = "Moved left. Merged 1 pair (+4)."
        self.assertEqual(game.last_feedback, message)
        self.assertEqual(output.getvalue().count(message), 1)

    def test_unchanged_move_does_not_claim_a_move_or_spawn_a_tile(self):
        game = self.make_game([2, 0, 0, 0])
        original_grid = [row[:] for row in game.board.grid]
        with patch.object(game.board, "add_random_tile") as add_tile:
            self.assertFalse(game.move("a"))

        self.assertEqual(game.last_feedback, "No tiles moved left.")
        self.assertEqual(game.board.grid, original_grid)
        add_tile.assert_not_called()

    def test_invalid_and_empty_commands_are_rejected(self):
        game = self.make_game([0, 2, 0, 0])
        original_grid = [row[:] for row in game.board.grid]
        with patch.object(game.board, "add_random_tile") as add_tile:
            self.assertFalse(game.move("x"))
            self.assertFalse(game.move(""))

        self.assertEqual(
            game.last_feedback,
            "Use W/A/S/D to move, U to undo, or Q to quit.",
        )
        self.assertEqual(game.board.grid, original_grid)
        add_tile.assert_not_called()

    def test_board_scans_do_not_print_action_feedback(self):
        board = Board()
        output = StringIO()
        with redirect_stdout(output):
            board.move_left()
            board.can_move()

        self.assertEqual(output.getvalue(), "")

    def test_undo_feedback_is_set_by_the_action(self):
        game = self.make_game([0, 2, 0, 0])
        with patch.object(game.board, "add_random_tile"):
            game.move("a")
        self.assertTrue(game.undo())

        self.assertEqual(game.last_feedback, "Undid the previous move.")


if __name__ == "__main__":
    unittest.main()
