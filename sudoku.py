from __future__ import annotations

from itertools import chain
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: list[list[int]]):
        self._grid: list[list[int]] = puzzle

    def place(self, value: int, x: int, y: int) -> None:
        """Places value at x,y."""
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Removes (unplaces) a number at x,y."""
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""

        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = set()

        # get the index of the block based from x,y
        block_index: int = (y // 3) * 3 + x // 3

        row = self.row_values(y)
        column = self.column_values(x)
        block = self.block_values(block_index)

        # remove all values from the row
        for value in range(1, 10):
            if value not in row and value not in column and value not in block:
                options.add(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            for x in range(9):
                if self._grid[y][x] == 0:
                    return x, y

        return -1, -1

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""

        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for row in self._grid:
            values.append(row[i])

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self._grid[y][x])

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        # values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        if 0 in chain(*self._grid):
            return False

        return True

    def __str__(self) -> str:

        representation = ""

        for row in self._grid:
            representation += str(row).replace(",", "")[1:-1] + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[list[int]] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            num_list = line.strip().split(",")

            # convert all numbers to integers
            numbers = [int(i) for i in num_list]

            puzzle.append(numbers)

    return Sudoku(puzzle)
