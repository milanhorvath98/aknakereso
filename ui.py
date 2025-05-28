import tkinter as tk
from tkinter import messagebox # For potential future use with dialogs
from game import MinesweeperGame # Import for _reset_game

# UI Enhancement Constants
FONT_DEFAULT = ('Arial', 10)
FONT_STATUS = ('Arial', 10, 'bold')
FONT_BUTTON_SYMBOLS = ('Arial', 12) # Potentially for Mine/Flag if needed, or use text

COLOR_BACKGROUND = '#ECECEC' # Main window background
COLOR_FRAME_BG = '#ECECEC'   # Frame background
COLOR_DEFAULT_BG = '#F0F0F0' # Default button background for unrevealed
COLOR_REVEALED_EMPTY = '#DCDCDC' # Light grey for revealed empty/number (was #E0E0E0)
COLOR_FLAGGED_BG = '#FFFFE0'     # Light yellow (was lightblue)
COLOR_MINE_BG = '#FFB6C1'        # Light pink/red (was red)
COLOR_BUTTON_BORDER = '#BDBDBD'  # For flat buttons with a border
COLOR_HIGHLIGHT = '#FFFFCC'      # Light yellow for click highlight

NUMBER_COLORS = {
    1: '#0000FF',  # Blue
    2: '#008000',  # Green
    3: '#FF0000',  # Red
    4: '#00008B',  # Dark Blue
    5: '#A52A2A',  # Brown
    6: '#00FFFF',  # Cyan
    7: '#000000',  # Black
    8: '#808080'   # Grey
}

CHAR_FLAG = 'F' # Using 'F' for Flag for better font compatibility (was 🚩)
CHAR_MINE = 'M' # Using 'M' for Mine for better font compatibility (was 💣)


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
        self.game = game_instance
        
        master.title("Minesweeper")
        master.config(bg=COLOR_BACKGROUND) # Set main window background

        # Store fonts and colors
        self.default_font = FONT_DEFAULT
        self.status_font = FONT_STATUS
        self.number_colors = NUMBER_COLORS

        # Main frame for better organization
        self.main_frame = tk.Frame(master, bg=COLOR_FRAME_BG)
        self.main_frame.pack(padx=10, pady=10)

        self.width = self.game.width
        self.height = self.game.height
        self.initial_num_mines = self.game.num_mines
        self.game_over = False
        
        self.buttons = [[None for _ in range(self.width)] for _ in range(self.height)]

        # Create button grid
        for r in range(self.height):
            for c in range(self.width):
                btn = tk.Button(
                    self.main_frame, 
                    text=' ', 
                    width=2, 
                    height=1,
                    font=self.default_font,
                    relief=tk.FLAT, # Modern look
                    borderwidth=1,
                    # highlightthickness=1, # Use if borders are too subtle or for focus
                    # highlightbackground=COLOR_BUTTON_BORDER 
                )
                btn.bind('<Button-1>', lambda event, row=r, col=c: self._handle_left_click(event, row, col))
                btn.bind('<Button-3>', lambda event, row=r, col=c: self._handle_right_click(event, row, col))
                btn.grid(row=r, column=c) # No extra padding here, let frame handle it
                self.buttons[r][c] = btn
        
        # Reset Button
        self.reset_button = tk.Button(
            master, 
            text="Reset Game", 
            command=self._reset_game,
            font=self.status_font,
            relief=tk.RAISED, # Standard look for a button
            bg=COLOR_DEFAULT_BG, # Give it a slight background
            padx=5, pady=2
        )
        self.reset_button.pack(pady=(0, 10)) # Padding top 0, bottom 10

        # Status bar (Label)
        self.status_label = tk.Label(
            master, 
            text=f"Mines: {self.game.num_mines}", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=self.status_font,
            bg=COLOR_DEFAULT_BG, # Match reset button or a neutral status color
            padx=5
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0)) # pady was implicitly added via pack

        self.sync_board_to_gui()

    def _reset_game(self):
        """Resets the game to its initial state."""
        self.game = MinesweeperGame(self.width, self.height, self.initial_num_mines)
        self.game_over = False
        # No need to manually enable all buttons here, sync_board_to_gui will handle it.
        # It sets unrevealed, unflagged cells to NORMAL state.
        self.sync_board_to_gui()
        # The status label is also updated by sync_board_to_gui to show correct mine/flag counts.

    def _handle_left_click(self, event, row, col):
        if self.game_over or self.game.flags[row][col]:
            return

        # Store original clicked coordinates, as row/col might be used elsewhere if we had complex logic
        clicked_r, clicked_c = row, col
        
        result = self.game.reveal_cell(clicked_r, clicked_c)

        # Subtle highlight for single, non-mine, non-flood-triggering reveals
        if isinstance(result, int) and result > 0: # result is the number of adjacent mines
            # This means a numbered cell was revealed, not a mine, and not an empty cell that starts flood fill
            button = self.buttons[clicked_r][clicked_c]
            button.config(bg=COLOR_HIGHLIGHT) # Apply highlight
            self.master.after(150, self.sync_board_to_gui) # Schedule full sync
        else:
            # For mines, flood-fills ('safe'), or no change (None), sync immediately
            self.sync_board_to_gui()
        
        # Game Over / Win Condition Logic (largely unchanged)
        if result == 'mine':
            self.game_over = True
            # self.game.revealed[clicked_r][clicked_c] is already True from reveal_cell
            self._reveal_all_unflagged_mines() 
            # Status label will be updated by sync_board_to_gui based on game_over state
            self._disable_all_buttons()
            # If highlight was applied, it will be brief. Game over state takes precedence.
            # A final sync might be needed if the `after` call is too slow for game over.
            # However, sync_board_to_gui is already called or scheduled.
            # Let's ensure one runs after game_over state is fully set.
            if not isinstance(result, int) or result <= 0: # if sync wasn't scheduled by highlight
                 self.sync_board_to_gui()


        if not self.game_over: # Only check for win if game is not over by a mine
            if self.game.check_win_condition():
                self.game_over = True
                # Status label will be updated by sync_board_to_gui
                self._disable_all_buttons()
                if not isinstance(result, int) or result <= 0: # if sync wasn't scheduled by highlight
                    self.sync_board_to_gui()
        
        # Note: The status label update logic in sync_board_to_gui already handles
        # "Game Over! You hit a mine." and "Congratulations! You won!" messages
        # when self.game_over is True.

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
        # Colors and characters are now defined as class/module constants
        
        for r in range(self.height):
            for c in range(self.width):
                button = self.buttons[r][c]
                is_revealed = self.game.revealed[r][c]
                is_flagged = self.game.flags[r][c]
                cell_value = self.game.board[r][c] # This is int or 'M'

                button_config = {
                    'font': self.default_font,
                    'relief': tk.FLAT, # Keep flat style consistent
                    'borderwidth': 1
                }

                if is_flagged:
                    button_config.update({
                        'text': CHAR_FLAG,
                        'state': tk.DISABLED, # Keep flagged cells disabled for left click
                        'bg': COLOR_FLAGGED_BG,
                        'fg': 'black' # Ensure flag char is visible
                    })
                elif not is_revealed:
                    button_config.update({
                        'text': ' ',
                        'state': tk.NORMAL,
                        'bg': COLOR_DEFAULT_BG 
                    })
                else: # Revealed
                    button_config['state'] = tk.DISABLED
                    button_config['bg'] = COLOR_REVEALED_EMPTY # Default for revealed

                    if cell_value == 'M':
                        button_config.update({
                            'text': CHAR_MINE,
                            'bg': COLOR_MINE_BG, # Specific color for mine
                            'fg': 'black' # Ensure mine char is visible
                        })
                    elif cell_value == 0:
                        button_config['text'] = ' '
                        # bg is already COLOR_REVEALED_EMPTY
                    else: # Number
                        num_val = int(cell_value) # Make sure it's int for dict key
                        button_config.update({
                            'text': str(num_val),
                            'fg': self.number_colors.get(num_val, 'black') # Default to black if number not in map
                        })
                
                button.config(**button_config)
        
        self._update_status_label()

    def _update_status_label(self):
        """Updates the status label based on the current game state."""
        flags_placed = sum(row.count(True) for row in self.game.flags)
        
        if self.game_over:
            # Check if the game_over was due to a win or loss
            # The game.check_win_condition() is true if all non-mines are revealed.
            # If game_over is true AND check_win_condition is true, it's a win.
            # Otherwise, if game_over is true and check_win_condition is false, it was a loss (hit a mine).
            if self.game.check_win_condition():
                 status_text = "Congratulations! You won!"
            else: 
                 status_text = "Game Over! You hit a mine."
        else:
            mines_remaining_to_find = self.game.num_mines - flags_placed
            status_text = f"Mines: {mines_remaining_to_find} | Flags: {flags_placed}"
            
        self.status_label.config(text=status_text)

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
