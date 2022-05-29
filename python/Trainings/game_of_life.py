import sys
import random
import os
import time


class GameOfLife:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.clear_console = "cls" if os.name == "nt" else "clear"
        self.init_grid()

    def init_grid(self):
        value = [0, 1]
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(random.choice(value))
            self.grid.append(row)

    def display(self):
        pixels = [" ", "#"]
        for row in self.grid:
            row_str = " ".join(pixels[x] for x in row)
            print(row_str)

    def kill_or_save_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                neighbor_num = self.count_neighbors(row, col)
                cell = self.grid[row][col]
                if cell:
                    if neighbor_num < 2 or neighbor_num > 3:
                        self.grid[row][col] = 0
                else:
                    if neighbor_num == 3:
                        self.grid[row][col] = 1

    def count_neighbors(self, row, col):
        neighbor_num = 0

        row_down = row + 1
        row_down = row_down if row_down <= self.rows - 1 else 0
        row_up = row - 1
        col_right = col + 1
        col_right = col_right if col_right <= self.cols - 1 else 0
        col_left = col - 1

        # upper cell
        neighbor_num += self.grid[row_up][col]
        # upper right
        neighbor_num += self.grid[row_up][col_right]
        # right
        neighbor_num += self.grid[row][col_right]
        # lower right
        neighbor_num += self.grid[row_down][col_right]
        # lower
        neighbor_num += self.grid[row_down][col]
        # lower left
        neighbor_num += self.grid[row_down][col_left]
        # left
        neighbor_num += self.grid[row][col_left]
        # upper left
        neighbor_num += self.grid[row_up][col_left]

        return neighbor_num

    def loop(self):
        self.display()
        while True:
            self.kill_or_save_cells()
            self.display()
            time.sleep(0.001)
            os.system(self.clear_console)


if __name__ == "__main__":
    rows = 70
    cols = 115
    # rows = 4
    # cols = 4
    game_of_life = GameOfLife(rows, cols)
    game_of_life.loop()
