import unittest
from game import MinesweeperGame
import random

class TestMinesweeperGame(unittest.TestCase):

    def test_board_initialization(self):
        game = MinesweeperGame(width=5, height=8, num_mines=10)
        self.assertEqual(game.width, 5)
        self.assertEqual(game.height, 8)
        self.assertEqual(len(game.board), 8) # Height
        self.assertEqual(len(game.board[0]), 5) # Width

        # Check number of mines
        mine_count = 0
        for r in range(game.height):
            for c in range(game.width):
                if game.board[r][c] == 'M':
                    mine_count += 1
        self.assertEqual(mine_count, 10)

        # Check revealed and flags arrays
        for r in range(game.height):
            for c in range(game.width):
                self.assertFalse(game.revealed[r][c])
                self.assertFalse(game.flags[r][c])

    def test_adjacent_mine_calculation(self):
        # Override random mine placement for this test
        game = MinesweeperGame(width=3, height=3, num_mines=2)
        # Manually place mines
        game.board = [
            ['M', 0, 0],
            [0, 'M', 0],
            [0, 0, 0]
        ]
        # Ensure revealed and flags are reset as __init__ would do
        game.revealed = [[False for _ in range(3)] for _ in range(3)]
        game.flags = [[False for _ in range(3)] for _ in range(3)]
        
        game._calculate_adjacent_mines()

        expected_board_values = [
            ['M', 2, 1],
            [2, 'M', 1],
            [1, 1, 1]
        ]
        for r in range(game.height):
            for c in range(game.width):
                self.assertEqual(game.board[r][c], expected_board_values[r][c])

    def test_reveal_cell_mine(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        # Manually place a mine
        game.board[0][0] = 'M'
        # Ensure other cells are not mines for simplicity of this test case
        for r in range(game.height):
            for c in range(game.width):
                if r == 0 and c == 0:
                    continue
                if game.board[r][c] == 'M': # if random placement also put a mine elsewhere
                    game.board[r][c] = 0 
        game._calculate_adjacent_mines() # Recalculate based on manual placement

        result = game.reveal_cell(0, 0)
        self.assertEqual(result, 'mine')
        self.assertTrue(game.revealed[0][0])

    def test_reveal_cell_empty_flood_fill(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        # Place a mine such that (0,0) is empty and triggers flood fill
        game.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 'M'] 
        ]
        game.revealed = [[False for _ in range(3)] for _ in range(3)]
        game.flags = [[False for _ in range(3)] for _ in range(3)]
        game._calculate_adjacent_mines()
        
        # (0,0) should be 0 after _calculate_adjacent_mines
        self.assertEqual(game.board[0][0], 0) 

        result = game.reveal_cell(0, 0)
        self.assertEqual(result, 'safe') # or 0, depending on implementation detail

        # Check that (0,0) and its non-mine neighbors are revealed
        # (0,0) is empty, (0,1) is 1, (1,0) is 1, (1,1) is 1
        # (2,2) is M, (1,2) is 1, (2,1) is 1, (0,2) is 0, (2,0) is 0
        # Flood fill should reveal (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)
        # because (0,2) and (2,0) are also 0.
        
        # Expected revealed state after flood fill from (0,0)
        # Board after calc:
        # 0  1  1
        # 1  2  M
        # 1  M  M  <- Mistake in original manual board, let's fix mine for clarity
        
        # Corrected setup for flood fill
        game = MinesweeperGame(width=4, height=4, num_mines=1)
        game.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,1,'M'], # Mine at (2,3)
            [0,0,1,1]
        ]
        game.revealed = [[False for _ in range(4)] for _ in range(4)]
        game.flags = [[False for _ in range(4)] for _ in range(4)]
        game._calculate_adjacent_mines()
        # Expected board after calculation:
        # 0  0  0  0
        # 0  0  1  1
        # 0  0  1  M
        # 0  0  1  1
        self.assertEqual(game.board[0][0], 0)
        
        game.reveal_cell(0,0)

        # All cells in the top-left 2x2 block should be revealed
        # And (0,2), (1,2)
        # And (0,3), (1,3)
        # And (2,0), (2,1)
        # And (3,0), (3,1)
        expected_revealed_pattern = [
            [True, True, True, True],
            [True, True, True, True],
            [True, True, False, False], # (2,2) is 1, (2,3) is M
            [True, True, False, False]  # (3,2) is 1, (3,3) is 1
        ]
        # Actually, the flood fill logic is simpler: reveal all 0s and their 1-degree neighbors
        # The current recursive reveal_cell will reveal all 0-cells and their immediate non-mine neighbors.
        # If a neighbor is also 0, it will continue from there.
        # For the given board:
        # 0  0  0  0
        # 0  0  1  1
        # 0  0  1  M
        # 0  0  1  1
        # Revealing (0,0) should reveal:
        # (0,0),(0,1),(0,2),(0,3)
        # (1,0),(1,1)
        # (2,0),(2,1)
        # (3,0),(3,1)
        # And also the '1' cells adjacent to these 0s:
        # (1,2), (2,2), (3,2)
        # (1,3) -> this is adjacent to (0,3) which is 0.

        self.assertTrue(game.revealed[0][0])
        self.assertTrue(game.revealed[0][1])
        self.assertTrue(game.revealed[0][2]) # adjacent to (0,1) which is 0
        self.assertTrue(game.revealed[0][3]) # adjacent to (0,2) which is 0
        self.assertTrue(game.revealed[1][0]) 
        self.assertTrue(game.revealed[1][1])
        self.assertTrue(game.revealed[1][2]) # This is 1, adjacent to (0,2), (1,1), (2,2)
        self.assertTrue(game.revealed[1][3]) # This is 1, adjacent to (0,3), (2,3)M
        self.assertTrue(game.revealed[2][0])
        self.assertTrue(game.revealed[2][1])
        self.assertTrue(game.revealed[2][2]) # This is 1
        self.assertFalse(game.revealed[2][3]) # Mine
        self.assertTrue(game.revealed[3][0])
        self.assertTrue(game.revealed[3][1])
        self.assertTrue(game.revealed[3][2]) # This is 1

    def test_reveal_cell_numbered(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        # Manually place a mine and setup board
        game.board = [
            ['M', 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        game.revealed = [[False for _ in range(3)] for _ in range(3)]
        game.flags = [[False for _ in range(3)] for _ in range(3)]
        game._calculate_adjacent_mines() # (0,1) will be 1

        result = game.reveal_cell(0, 1)
        self.assertEqual(result, 1) # Number of adjacent mines
        self.assertTrue(game.revealed[0][1])
        # Ensure only that cell is revealed
        self.assertFalse(game.revealed[0][0]) 
        self.assertFalse(game.revealed[0][2])
        self.assertFalse(game.revealed[1][1])

    def test_reveal_already_revealed_cell(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        game.board[0][1] = 1 # Assume it's a numbered cell
        game.revealed[0][1] = True
        
        result = game.reveal_cell(0, 1)
        self.assertIsNone(result) # Should do nothing
        self.assertTrue(game.revealed[0][1]) # Remains revealed

    def test_reveal_flagged_cell(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        game.flags[0][1] = True
        
        result = game.reveal_cell(0, 1)
        self.assertIsNone(result) # Should do nothing
        self.assertFalse(game.revealed[0][1]) # Remains unrevealed
        self.assertTrue(game.flags[0][1]) # Remains flagged

    def test_toggle_flag(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        
        # Flag an unrevealed cell
        game.toggle_flag(0, 0)
        self.assertTrue(game.flags[0][0])

        # Unflag a flagged cell
        game.toggle_flag(0, 0)
        self.assertFalse(game.flags[0][0])

    def test_toggle_flag_on_revealed_cell(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        game.board[0][0] = 1 # Some non-mine value
        game.revealed[0][0] = True
        
        game.toggle_flag(0, 0)
        self.assertFalse(game.flags[0][0]) # Should not be able to flag

    def test_check_win_condition_win(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        # Manually set up a win state
        game.board = [
            ['M', 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        # Reveal all non-mine cells
        game.revealed = [
            [False, True, True],
            [True, True, True],
            [True, True, True]
        ]
        self.assertTrue(game.check_win_condition())

    def test_check_win_condition_not_win(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        game.board = [ # Assume this is post _calculate_adjacent_mines
            ['M', 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        # Not all non-mine cells are revealed
        game.revealed = [
            [False, True, False], # (0,2) is not revealed
            [True, True, True],
            [True, True, True]
        ]
        self.assertFalse(game.check_win_condition())

    def test_check_win_condition_with_flags(self):
        game = MinesweeperGame(width=3, height=3, num_mines=1)
        game.board = [
            ['M', 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        game.revealed = [
            [False, True, True],
            [True, True, True],
            [True, True, True]
        ]
        game.flags[0][0] = True # Flag the mine
        self.assertTrue(game.check_win_condition()) # Win condition only depends on revealed non-mines

        # Scenario: A non-mine is flagged but not revealed -> not a win
        game.revealed[1][1] = False
        game.flags[1][1] = True
        self.assertFalse(game.check_win_condition())

if __name__ == '__main__':
    unittest.main()
