import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.last_merge_score = 0
        self.last_merge_count = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        return Board._slide_line_with_score(line)[0]

    @staticmethod
    def _slide_line_with_score(line):
        values = [x for x in line if x]
        result = []
        score_gained = 0
        merge_count = 0
        index = 0

        while index < len(values):
            value = values[index]
            if index + 1 < len(values) and value == values[index + 1]:
                merged_value = value * 2
                result.append(merged_value)
                score_gained += merged_value
                merge_count += 1
                index += 2
            else:
                result.append(value)
                index += 1

        result.extend([0] * (SIZE - len(result)))
        return result, score_gained, merge_count

    def _record_merges(self, score_gained, merge_count):
        self.score += score_gained
        self.last_merge_score += score_gained
        self.last_merge_count += merge_count

    def _begin_move(self):
        self.last_merge_score = 0
        self.last_merge_count = 0

    def move_left(self):
        self._begin_move()
        changed = False
        for r in range(SIZE):
            old = self.grid[r][:]
            self.grid[r], score_gained, merge_count = self._slide_line_with_score(old)
            self._record_merges(score_gained, merge_count)
            changed |= old != self.grid[r]
        return changed

    def move_right(self):
        self._begin_move()
        changed = False
        for r in range(SIZE):
            old = self.grid[r][:]
            reversed_line = list(reversed(old))
            moved_line, score_gained, merge_count = self._slide_line_with_score(reversed_line)
            self.grid[r] = list(reversed(moved_line))
            self._record_merges(score_gained, merge_count)
            changed |= old != self.grid[r]
        return changed

    def move_up(self):
        self._begin_move()
        changed = False
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, score_gained, merge_count = self._slide_line_with_score(old)
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            self._record_merges(score_gained, merge_count)
            changed |= old != new
        return changed

    def move_down(self):
        self._begin_move()
        changed = False
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            reversed_line = list(reversed(old))
            moved_line, score_gained, merge_count = self._slide_line_with_score(reversed_line)
            new = list(reversed(moved_line))
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            self._record_merges(score_gained, merge_count)
            changed |= old != new
        return changed

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False
