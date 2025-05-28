import random

class MinesweeperGame:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flags = [[False for _ in range(width)] for _ in range(height)]
        
        self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if self.board[row][col] != 'M':
                self.board[row][col] = 'M'
                mines_placed += 1

    def _calculate_adjacent_mines(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == 'M':
                    continue
                mine_count = 0
                for i in range(max(0, r - 1), min(self.height, r + 2)):
                    for j in range(max(0, c - 1), min(self.width, c + 2)):
                        if (i, j) == (r, c):
                            continue
                        if self.board[i][j] == 'M':
                            mine_count += 1
                self.board[r][c] = mine_count

    def reveal_cell(self, row, col):
        if not (0 <= row < self.height and 0 <= col < self.width):
            return None # Out of bounds
        if self.revealed[row][col] or self.flags[row][col]:
            return None

        self.revealed[row][col] = True

        if self.board[row][col] == 'M':
            return 'mine'
        
        if self.board[row][col] == 0:
            for r_offset in range(-1, 2):
                for c_offset in range(-1, 2):
                    if r_offset == 0 and c_offset == 0:
                        continue
                    self.reveal_cell(row + r_offset, col + c_offset)
            return 'safe' # Or 0, consistent return type might be better. For now, 'safe' for 0-mine cells.

        return self.board[row][col] # Number of adjacent mines

    def toggle_flag(self, row, col):
        if not (0 <= row < self.height and 0 <= col < self.width):
            return # Out of bounds
        if self.revealed[row][col]:
            return
        self.flags[row][col] = not self.flags[row][col]

    def check_win_condition(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] != 'M' and not self.revealed[r][c]:
                    return False
        return True
