from Main_functions import *
from Models.Board import *

human = True  # TODO: Enable if playing against a human player (in black)

# INITIALISATION
print("---> You get three seconds to focus on the board <---")
time.sleep(3)
print("---> Start initialisation: <---")
print()

dimensionBoard = get_dimension_board()
dimensionSquare = dimensionBoard[0] / 8, dimensionBoard[1] / 8
board = [[None] * 8] * 8
for i in range(8):
    board[i] = [None] * 8
start_board = get_start_pos_board()
pyautogui.moveTo(start_board[0], start_board[1], 0.2)

# MAIN
print("---> Start main: <---")
print()

init_board(board)
check_complete_board(start_board, dimensionSquare, board)  # Make own board up to date with real board
print_own_board(board)

while True:
    if game_active():
        print("Our algorithm\'s turn: ", end="")
        print("Calculating...")
        best_move, end_game = compute_best_move(board)
        print("Best move: ", end="")
        print(best_move)
        move_piece(best_move[0], best_move[1], start_board, dimensionSquare, board)
        if end_game:
            break  # Check mate

        time.sleep(1)
        print("Their turn:")
        if check_got_promotion():
            check_complete_board(start_board, dimensionSquare, board)
        if human:
            while not check_complete_board(start_board, dimensionSquare, board):
                time.sleep(0.5)
            time.sleep(0.5)
        check_complete_board(start_board, dimensionSquare, board)
        print_own_board(board)
    else:
        time.sleep(0.5)

# While-loop has ended
print(" ____________ ")
print("|            |")
print("| GAME OVER! |")
print("|____________|")
