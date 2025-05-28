import tkinter as tk
from game import MinesweeperGame
from ui import MinesweeperGUI # Changed from text-based UI functions

# Game settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 10 # Adjusted for a more standard square board for GUI
NUM_MINES = 15 # Slightly increased mine count for a 10x10 board

# def reveal_all_cells(game): # No longer needed for GUI version
#     """Helper function to reveal all cells at the end of the game."""
#     for r in range(game.height):
#         for c in range(game.width):
#             game.revealed[r][c] = True 
#             game.flags[r][c] = False

def main():
    root = tk.Tk()
    
    # Create game instance
    game = MinesweeperGame(BOARD_WIDTH, BOARD_HEIGHT, NUM_MINES)
    
    # Create GUI instance, passing the root window and game instance
    # The MinesweeperGUI class itself handles setting the window title and other setup.
    gui = MinesweeperGUI(root, game) 
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
