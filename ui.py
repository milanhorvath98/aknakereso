# UI elements for Minesweeper

def display_board(game):
    """Displays the Minesweeper board in the console."""
    print("   " + " ".join([str(i) for i in range(game.width)])) # Column headers
    print("  " + "--" * game.width)
    for r in range(game.height):
        row_str = f"{r}| " # Row header
        for c in range(game.width):
            if game.flags[r][c]:
                row_str += "F "
            elif not game.revealed[r][c]:
                row_str += "# "
            else:
                if game.board[r][c] == 'M':
                    row_str += "M "
                elif game.board[r][c] == 0:
                    row_str += "  " # Space for empty cell
                else:
                    row_str += f"{game.board[r][c]} "
        print(row_str)
    print()

def get_user_input(width, height):
    """Prompts the user for input and validates it."""
    while True:
        try:
            user_input = input(f"Enter action ('reveal R C' or 'flag R C', or 'r R C' or 'f R C'): ").strip().lower()
            parts = user_input.split()
            
            action_input = parts[0]
            row = int(parts[1])
            col = int(parts[2])

            if action_input not in ['reveal', 'r', 'flag', 'f']:
                raise ValueError("Invalid action. Use 'reveal'/'r' or 'flag'/'f'.")
            
            if not (0 <= row < height and 0 <= col < width):
                raise ValueError(f"Coordinates out of bounds. Row must be 0-{height-1}, Col must be 0-{width-1}.")

            action_type = 'reveal' if action_input in ['reveal', 'r'] else 'flag'
            
            return action_type, row, col

        except (ValueError, IndexError) as e:
            print(f"Error: {e}. Please try again.")
