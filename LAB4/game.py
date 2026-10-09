from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self._undo_state = None

    def has_won(self):
        return any(tile >= 2048 for row in self.board.grid for tile in row)

    def is_game_over(self):
        return self.has_won() or not self.board.can_move()

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves or self.is_game_over():
            return False

        previous_state = ([row[:] for row in self.board.grid], self.board.score)
        changed = moves[key]()
        if changed:
            self._undo_state = previous_state
            self.best_score = max(self.best_score, self.board.score)
            if not self.has_won():
                self.board.add_random_tile()
        return changed

    def undo(self):
        if self._undo_state is None:
            return False

        grid, score = self._undo_state
        self.board.grid = [row[:] for row in grid]
        self.board.score = score
        self.board.last_merge_score = 0
        self.board.last_merge_count = 0
        self._undo_state = None
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            if self.has_won():
                print("You reached 2048!")
                return
            if not self.board.can_move():
                print("No legal moves remain.")
                return
            key = input("> ").strip().lower()
            if key == "q":
                return
            if key == "u":
                if self.undo():
                    print("Undid the previous move.")
                else:
                    print("Nothing to undo.")
                continue
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue
            self.move(key)
