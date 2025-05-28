from game import MinesweeperGame
from ui import display_board, get_user_input

# Game settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 10
NUM_MINES = 10

def reveal_all_cells(game):
    """Helper function to reveal all cells at the end of the game."""
    for r in range(game.height):
        for c in range(game.width):
            game.revealed[r][c] = True # Directly reveal, bypassing game logic for display purposes
            game.flags[r][c] = False # Clear flags for final display

if __name__ == "__main__":
    game = MinesweeperGame(BOARD_WIDTH, BOARD_HEIGHT, NUM_MINES)
    game_over = False
    win = False

    print("Welcome to Minesweeper!")

    while not game_over:
        display_board(game)
        action_type, row, col = get_user_input(game.width, game.height)

        if action_type == 'reveal':
            result = game.reveal_cell(row, col)
            if result == 'mine':
                print("BOOM! You hit a mine!")
                game_over = True
                win = False
            elif result is None: # Cell was already revealed or flagged
                print("Cell already revealed or flagged. Try another.")
                continue
        elif action_type == 'flag':
            game.toggle_flag(row, col)

        if not game_over and game.check_win_condition():
            print("Congratulations! You've cleared all the mines!")
            game_over = True
            win = True
    
    # Game ended, reveal all cells and display final board
    reveal_all_cells(game)
    print("\nFinal Board:")
    display_board(game)

    if win:
        print("You won!")
    else:
        print("Game Over!")
