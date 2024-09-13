import random


# Initialize the board
def create_board():
    return [[' ' for _ in range(7)] for _ in range(6)]


# Print the board
def print_board(board):
    for row in board:
        print('|' + '|'.join(row) + '|')
    print(' ' + '-' * 15)


# Drop a disc into a column
def drop_disc(board, col, disc):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = disc
            return True
    return False


# Check for a win (horizontal, vertical, and diagonal)
def check_win(board, disc):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == disc for i in range(4)):
                return True

    # Check vertical
    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == disc for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == disc for i in range(4)):
                return True

    # Check diagonal \
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == disc for i in range(4)):
                return True

    return False


# Check for stalemate
def check_stalemate(board):
    return all(board[0][col] != ' ' for col in range(7))


# Check if a move will win
def will_win(board, col, disc):
    temp_board = [row[:] for row in board]
    drop_disc(temp_board, col, disc)
    return check_win(temp_board, disc)


# Computer move
def computer_move(board):
    # Check for immediate win
    for col in range(7):
        if board[0][col] == ' ' and will_win(board, col, 'O'):
            return col

    # Block user win
    for col in range(7):
        if board[0][col] == ' ' and will_win(board, col, 'X'):
            return col

    # Random move if no immediate win or block
    available_columns = [col for col in range(7) if board[0][col] == ' ']
    return random.choice(available_columns)


# Main game loop
def play_game():
    board = create_board()
    game_over = False
    current_player = 'User'  # Start with the user

    while not game_over:
        print_board(board)

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
                print_board(board)
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
            col = computer_move(board)
            drop_disc(board, col, 'O')

            if check_win(board, 'O'):
                print_board(board)
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


