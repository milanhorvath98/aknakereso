import tkinter as tk
from tkinter import messagebox # For potential future use with dialogs

# # UI elements for Minesweeper (Text-based)
#
# def display_board(game):
#     """Displays the Minesweeper board in the console."""
#     print("   " + " ".join([str(i) for i in range(game.width)])) # Column headers
#     print("  " + "--" * game.width)
#     for r in range(game.height):
#         row_str = f"{r}| " # Row header
#         for c in range(game.width):
#             if game.flags[r][c]:
#                 row_str += "F "
#             elif not game.revealed[r][c]:
#                 row_str += "# "
#             else:
#                 if game.board[r][c] == 'M':
#                     row_str += "M "
#                 elif game.board[r][c] == 0:
#                     row_str += "  " # Space for empty cell
#                 else:
#                     row_str += f"{game.board[r][c]} "
#         print(row_str)
#     print()
#
# def get_user_input(width, height):
#     """Prompts the user for input and validates it."""
#     while True:
#         try:
#             user_input = input(f"Enter action ('reveal R C' or 'flag R C', or 'r R C' or 'f R C'): ").strip().lower()
#             parts = user_input.split()
#            
#             action_input = parts[0]
#             row = int(parts[1])
#             col = int(parts[2])
#
#             if action_input not in ['reveal', 'r', 'flag', 'f']:
#                 raise ValueError("Invalid action. Use 'reveal'/'r' or 'flag'/'f'.")
#            
#             if not (0 <= row < height and 0 <= col < width):
#                 raise ValueError(f"Coordinates out of bounds. Row must be 0-{height-1}, Col must be 0-{width-1}.")
#
#             action_type = 'reveal' if action_input in ['reveal', 'r'] else 'flag'
#            
#             return action_type, row, col
#
#         except (ValueError, IndexError) as e:
#             print(f"Error: {e}. Please try again.")

class MinesweeperGUI:
    def __init__(self, master, game_instance):
        self.master = master
        self.game = game_instance # Renamed from game_instance for brevity
        
        master.title("Minesweeper")

        # Main frame for better organization
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=10, pady=10) # Add some padding around the frame

        self.width = self.game.width
        self.height = self.game.height
        self.game_over = False # Initialize game_over state
        
        self.buttons = [[None for _ in range(self.width)] for _ in range(self.height)]

        # Create button grid
        for r in range(self.height):
            for c in range(self.width):
                btn = tk.Button(self.main_frame, text=' ', width=2, height=1)
                # Bind left and right clicks
                btn.bind('<Button-1>', lambda event, row=r, col=c: self._handle_left_click(event, row, col))
                btn.bind('<Button-3>', lambda event, row=r, col=c: self._handle_right_click(event, row, col))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn
        
        # Status bar (Label)
        self.status_label = tk.Label(master, text=f"Mines: {self.game.num_mines}", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.sync_board_to_gui() # Initial sync

    def _handle_left_click(self, event, row, col):
        if self.game_over or self.game.flags[row][col]:
            return

        result = self.game.reveal_cell(row, col)

        if result == 'mine':
            self.game_over = True
            # Ensure the clicked mine itself is marked as revealed for sync_board_to_gui
            self.game.revealed[row][col] = True 
            self._reveal_all_unflagged_mines()
            self.status_label.config(text="Game Over! You hit a mine.")
            self._disable_all_buttons() # Disable buttons before final sync
        
        self.sync_board_to_gui() # Sync after potential game state changes

        # Check for win condition only if not a mine and game not already over by mine
        if result != 'mine' and not self.game_over:
            if self.game.check_win_condition():
                self.game_over = True
                self.status_label.config(text="Congratulations! You won!")
                self._disable_all_buttons()
                self.sync_board_to_gui() # Sync again to show final win state (e.g. all disabled)


    def _handle_right_click(self, event, row, col):
        if self.game_over or self.game.revealed[row][col]:
            return
        
        self.game.toggle_flag(row, col)
        self.sync_board_to_gui()

    def _disable_all_buttons(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.buttons[r][c]:
                    self.buttons[r][c].config(state=tk.DISABLED)

    def _reveal_all_unflagged_mines(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.game.board[r][c] == 'M' and not self.game.flags[r][c]:
                    self.game.revealed[r][c] = True
                    # No need to update button appearance here, sync_board_to_gui will do it

    def sync_board_to_gui(self):
        """Updates the GUI buttons to reflect the current game state."""
        # Define colors and characters (can be moved to class/module constants)
        COLOR_DEFAULT_BG = 'SystemButtonFace' # Default button color
        COLOR_REVEALED_EMPTY = '#d9d9d9' # Light grey for revealed empty/number
        COLOR_FLAGGED_BG = 'lightblue'
        COLOR_MINE_BG = 'red'
        CHAR_FLAG = '🚩' # Or 'F'
        CHAR_MINE = '💣' # Or 'M'

        for r in range(self.height):
            for c in range(self.width):
                button = self.buttons[r][c]
                is_revealed = self.game.revealed[r][c]
                is_flagged = self.game.flags[r][c]
                cell_value = self.game.board[r][c]

                if is_flagged:
                    button.config(text=CHAR_FLAG, state=tk.DISABLED, bg=COLOR_FLAGGED_BG)
                elif not is_revealed:
                    button.config(text=' ', state=tk.NORMAL, bg=COLOR_DEFAULT_BG)
                else: # Revealed
                    button.config(state=tk.DISABLED)
                    if cell_value == 'M':
                        button.config(text=CHAR_MINE, bg=COLOR_MINE_BG)
                    elif cell_value == 0:
                        button.config(text=' ', bg=COLOR_REVEALED_EMPTY)
                    else: # Number
                        button.config(text=str(cell_value), bg=COLOR_REVEALED_EMPTY)
        
        # Update status label
        # For now, just total mines. Could be updated to remaining non-flagged mines.
        flags_placed = sum(row.count(True) for row in self.game.flags)
        self.status_label.config(text=f"Mines: {self.game.num_mines} | Flags: {flags_placed}")


    # Additional methods for updating UI, handling game events will be added later

# Example usage (for testing purposes, will be moved to main.py)
if __name__ == '__main__':
    # This part is just for testing the GUI structure directly
    # In the actual application, main.py will instantiate MinesweeperGame and MinesweeperGUI
    class MockGame: # Mock game class for testing
        def __init__(self, width, height, num_mines):
            self.width = width
            self.height = height
            self.num_mines = num_mines
            # Minimal attributes to make the GUI init work
            self.board = [[' ' for _ in range(width)] for _ in range(height)] 
            self.revealed = [[False for _ in range(width)] for _ in range(height)]
            self.flags = [[False for _ in range(width)] for _ in range(height)]

    root = tk.Tk()
    mock_game_instance = MockGame(width=10, height=8, num_mines=12)
    gui = MinesweeperGUI(root, mock_game_instance)
    root.mainloop()
