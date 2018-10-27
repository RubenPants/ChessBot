from imagesearch import *


def get_dimension_board():
    """
    :return The width and the height (tuple) of a given image.
    """
    img = cv2.imread("Images/init_board.jpg")
    height, width, channels = img.shape
    return width, height


def get_start_pos_board():
    """
    Return the left-top position of the board
    """
    pos = imagesearch("Images/init_board.jpg")
    print(pos[0], pos[1] + get_dimension_board()[1])
    return pos[0], pos[1] + get_dimension_board()[1]


def print_real_board(board):
    """
    Display the real board in matrix form
    """
    for row in range(7, -1, -1):
        print(row + 1, end="  ")
        for col in range(8):
            print(get_string((row, col), board), end=", ")
        print()
    print("    A   B   C   D   E   F   G   H")
    print()


def print_own_board(board):
    """
    Display our own board in matrix form
    """
    for row in range(7, -1, -1):
        print(row, end="  ")
        for col in range(8):
            print(get_string((row, col), board), end=", ")
        print()
    print("    0   1   2   3   4   5   6   7")
    print()


def set_string(pos, string, board):
    """
    Put string on a requested place on the board
    """
    board[pos[0]][pos[1]] = string


def get_string(pos, board):
    """
    Get the string of the requested place on the board
    """
    if piece_on_pos(pos, board):
        return board[pos[0]][pos[1]].string
    return "  "


def init_board(board):
    """
    Initialize the board-matrix
    """
    from Models.King import King
    from Models.Queen import Queen
    from Models.Tower import Tower
    from Models.Bishop import Bishop
    from Models.Horse import Horse
    from Models.Pawn import Pawn

    # Black
    board[7][0] = Tower("TB")
    board[7][1] = Horse("HB")
    board[7][2] = Bishop("BB")
    board[7][3] = Queen("QB")
    board[7][4] = King("KB")
    board[7][5] = Bishop("BB")
    board[7][6] = Horse("HB")
    board[7][7] = Tower("TB")
    for i in range(8):
        board[6][i] = Pawn("PB")

    # White
    board[0][0] = Tower("TW")
    board[0][1] = Horse("HW")
    board[0][2] = Bishop("BW")
    board[0][3] = Queen("QW")
    board[0][4] = King("KW")
    board[0][5] = Bishop("BW")
    board[0][6] = Horse("HW")
    board[0][7] = Tower("TW")
    for i in range(8):
        board[1][i] = Pawn("PW")


def piece_on_pos(pos, board):
    """
    :return True if the given position has a piece on our board
    """
    if pos_within_board(pos):
        return not (not board[pos[0]][pos[1]])


def black_piece_on_pos(pos, board):
    """
    :return True if there is a black piece on the given position on the board
    """
    if pos_within_board(pos):
        obj = board[pos[0]][pos[1]]
        if piece_on_pos(pos, board):
            return "W" not in obj.string
    return False


def white_piece_on_pos(pos, board):
    """
    :return True if there is a white piece on the given position on the board
    """
    if pos_within_board(pos):
        obj = board[pos[0]][pos[1]]
        if piece_on_pos(pos, board):
            return "W" in obj.string
    return False


def pos_within_board(pos):
    """
    Check if the given positions are within the board
    """
    return (pos[0] >= 0) and (pos[1] >= 0) and (pos[0] <= 7) and (pos[1] <= 7)


def valid_new_position(new_pos, start_pos):
    return new_pos != start_pos and pos_within_board(new_pos)
