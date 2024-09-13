import random

# Initialize the board
def create_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

# Print the board with optional highlighting of winning discs
def print_board(board, winning_discs=None):
    for row in range(6):
        row_display = '|'
        for col in range(7):
            disc = board[row][col]
            if winning_discs and (row, col) in winning_discs:
                # Highlight winning discs (for example, using brackets)
                row_display += f'[{disc}]|'
            else:
                row_display += f' {disc} |'
        print(row_display)
    print(' ' + '-' * 15)

# Drop a disc into a column
def drop_disc(board, col, disc):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = disc
            return True
    return False

# Undo the last move
def undo_move(board, col):
    for row in board:
        if row[col] != ' ':
            row[col] = ' '
            return

# Check for a win and return the winning discs' coordinates
def check_win(board, disc):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == disc for i in range(4)):
                return [(row, col + i) for i in range(4)]

    # Check vertical
    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == disc for i in range(4)):
                return [(row + i, col) for i in range(4)]

    # Check positive diagonal (\)
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == disc for i in range(4)):
                return [(row + i, col + i) for i in range(4)]

    # Check negative diagonal (/)
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == disc for i in range(4)):
                return [(row - i, col + i) for i in range(4)]

    return []

# Check for stalemate
def check_stalemate(board):
    return all(board[0][col] != ' ' for col in range(7))

# Evaluate board state
def evaluate_board(board, disc):
    score = 0
    # Evaluate horizontal and vertical lines
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == disc for i in range(4)):
                score += 10
            if all(board[row][col + i] == ('X' if disc == 'O' else 'X') for i in range(4)):
                score -= 10

    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == disc for i in range(4)):
                score += 10
            if all(board[row + i][col] == ('X' if disc == 'O' else 'X') for i in range(4)):
                score -= 10

    return score

# MiniMax Algorithm with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win(board, 'O'):
        return 1000
    if check_win(board, 'X'):
        return -1000
    if check_stalemate(board):
        return 0
    if depth == 0:
        return evaluate_board(board, 'O')

    if is_maximizing:
        max_eval = -float('inf')
        for col in get_available_columns(board):
            drop_disc(board, col, 'O')
            eval = minimax(board, depth - 1, False, alpha, beta)
            undo_move(board, col)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for col in get_available_columns(board):
            drop_disc(board, col, 'X')
            eval = minimax(board, depth - 1, True, alpha, beta)
            undo_move(board, col)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Compute the best move for the computer
def compute_best_move(board):
    best_move = None
    best_value = -float('inf')
    for col in get_available_columns(board):
        drop_disc(board, col, 'O')
        move_value = minimax(board, 3, False, -float('inf'), float('inf'))
        undo_move(board, col)
        if move_value > best_value:
            best_value = move_value
            best_move = col
    return best_move

# Find available columns
def get_available_columns(board):
    return [col for col in range(7) if board[0][col] == ' ']

# Main game loop
def play_game():
    board = create_board()
    game_over = False

    # Ask the player if the computer should go first
    while True:
        choice = input("Do you want the computer to go first? (yes/no): ").strip().lower()
        if choice in ['yes', 'no']:
            computer_first = choice == 'yes'
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

    # Set the starting player
    current_player = 'Computer' if computer_first else 'User'

    while not game_over:
        winning_discs = None
        print_board(board, winning_discs)

        if current_player == 'User':
            while True:
                try:
                    col = int(input("Choose a column (0-6): "))
                    if 0 <= col <= 6:
                        if drop_disc(board, col, 'X'):
                            break
                        else:
                            print("Column full! Try a different column.")
                    else:
                        print("Invalid column! Choose between 0 and 6.")
                except ValueError:
                    print("Invalid input! Please enter an integer between 0 and 6.")

            if check_win(board, 'X'):
                winning_discs = check_win(board, 'X')
                print_board(board, winning_discs)
                print("Congratulations! You win!")
                game_over = True
            else:
                if check_stalemate(board):
                    print_board(board)
                    print("It's a tie!")
                    game_over = True
                else:
                    current_player = 'Computer'

        else:  # Computer's turn
            col = compute_best_move(board)
            drop_disc(board, col, 'O')

            if check_win(board, 'O'):
                winning_discs = check_win(board, 'O')
                print_board(board, winning_discs)
                print("Computer wins! Better luck next time.")
                game_over = True
            else:
                if check_stalemate(board):
                    print_board(board)
                    print("It's a tie!")
                    game_over = True
                else:
                    current_player = 'User'

if __name__ == "__main__":
    play_game()




