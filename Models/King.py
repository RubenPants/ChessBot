from Models.Board import *

string = "KW"
points = 1000


class King:
    def __init__(self, stri="KW"):
        self.string = stri
        self.im_b = "Images/" + stri + "B.jpg"
        self.im_w = "Images/" + stri + "W.jpg"
        if "W" in stri:
            self.points = 2 * points
        else:
            self.points = -points


def possible_positions_king_white(start_pos, end_pos):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if start_pos == end_pos:
        return False
    if abs(abs(start_pos[0]) - abs(end_pos[0])) < 2 and abs(abs(start_pos[1]) - abs(end_pos[1])) < 2:
        return True
    return False


def valid_positions_king_white(start_pos, board):
    """
    A position is valid when no one of the other team can obtain the king, and there is no white piece on this position

    :return A list with all possible positions
    """
    list = []

    for row in range(start_pos[0] - 1, start_pos[0] + 2):
        for col in range(start_pos[1] - 1, start_pos[1] + 2):
            if valid_new_position((row, col), start_pos) and not white_piece_on_pos((row, col), board):
                if (king_white_not_under_threat_close((row, col), board) and
                        king_white_not_under_threat_far((row, col), board)):
                    list.append((row, col))

    return list


def king_white_not_under_threat_close(pos, board):
    """
    Consider a 5x5-cube around the king, check if there are any pawns, horses or the king of the other team in here which
    are a threat to this position. Consider each individual to improve performance. Pos will be within the board.

    :param pos: the position that must be checked
    :param board: our board
    :return True if not a threat
    """
    from Models.Horse import Horse
    from Models.Horse import possible_position_horse_black
    from Models.Pawn import Pawn

    # Pawn
    new_pos = (pos[0] + 1, pos[1] + 1)
    if black_piece_on_pos(new_pos, board):
        if type(board[new_pos[0]][new_pos[1]]) is Pawn:
            return False
    new_pos = (pos[0] + 1, pos[1] - 1)
    if black_piece_on_pos(new_pos, board):
        if type(board[new_pos[0]][new_pos[1]]) is Pawn:
            return False

    # 3x3-cube: King
    for row in range(pos[0] - 1, pos[0] + 2):
        for col in range(pos[1] - 1, pos[1] + 2):
            if black_piece_on_pos((row, col), board):
                if type(board[row][col]) is King:
                    return False

    # 5x5-cube: Horse
    for row in range(pos[0] - 2, pos[0] + 3):
        for col in range(pos[1] - 2, pos[1] + 3):
            if (row != pos[0]) and (col != pos[1]) and black_piece_on_pos((row, col), board):
                if (type(board[row][col]) is Horse) and possible_position_horse_black((row, col), pos, board):
                    return False

    return True


def king_white_not_under_threat_far(pos, board):
    """
    Consider a queen on the given position, search for all enemy-pieces a queen could take at this position. If the piece
    that this queen could obtain also could obtain us, then this piece is a threat to our king, and thus this position is
    not a valid position. Pos will be within the board.

    :param pos: the position that must be checked
    :param board: our board
    :return True if not a threat
    """
    from Models.Queen import Queen
    from Models.Tower import Tower
    from Models.Bishop import Bishop

    # Up
    end_pos = pos[0] + 1, pos[1]
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] + 1, end_pos[1]
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Down
    end_pos = pos[0] - 1, pos[1]
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] - 1, end_pos[1]
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Left
    end_pos = pos[0], pos[1] - 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0], end_pos[1] - 1
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Right
    end_pos = pos[0], pos[1] + 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0], end_pos[1] + 1
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Top-Right
    end_pos = pos[0] + 1, pos[1] + 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] + 1, end_pos[1] + 1
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    # Top-Left
    end_pos = pos[0] + 1, pos[1] - 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] + 1, end_pos[1] - 1
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    # Bottom-Right
    end_pos = pos[0] - 1, pos[1] + 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] - 1, end_pos[1] + 1
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    # Bottom-Left
    end_pos = pos[0] - 1, pos[1] - 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] - 1, end_pos[1] - 1
    if pos_within_board(end_pos) and black_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    return True


def possible_positions_king_black(start_pos, end_pos):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if start_pos == end_pos:
        return False
    if abs(abs(start_pos[0]) - abs(end_pos[0])) < 2 and abs(abs(start_pos[1]) - abs(end_pos[1])) < 2:
        return True
    return False


def valid_positions_king_black(start_pos, board):
    """
    A position is valid when no one of the other team can obtain the king, and there is no white piece on this position

    :return A list with all possible positions
    """
    list = []

    for row in range(start_pos[0] - 1, start_pos[0] + 2):
        for col in range(start_pos[1] - 1, start_pos[1] + 2):
            if valid_new_position((row, col), start_pos) and not black_piece_on_pos((row, col), board):
                if (king_black_not_under_threat_close((row, col), board) and
                        king_black_not_under_threat_far((row, col), board)):
                    list.append((row, col))

    return list


def king_black_not_under_threat_close(pos, board):
    """
    Consider a 5x5-cube around the king, check if there are any pawns, horses or the king of the other team in here which
    are a threat to this position. Consider each individual to improve performance. Pos will be within the board.

    :param pos: the position that must be checked
    :param board: our board
    :return True if not a threat
    """
    from Models.Horse import Horse
    from Models.Horse import possible_position_horse_white
    from Models.Pawn import Pawn

    # Pawn
    new_pos = (pos[0] - 1, pos[1] - 1)
    if white_piece_on_pos(new_pos, board):
        if type(board[new_pos[0]][new_pos[1]]) is Pawn:
            return False
    new_pos = (pos[0] - 1, pos[1] + 1)
    if white_piece_on_pos(new_pos, board):
        if type(board[new_pos[0]][new_pos[1]]) is Pawn:
            return False

    # 3x3-cube: King
    for row in range(pos[0] - 1, pos[0] + 2):
        for col in range(pos[1] - 1, pos[1] + 2):
            if white_piece_on_pos((row, col), board):
                if type(board[row][col]) is King:
                    return False

    # 5x5-cube: Horse
    for row in range(pos[0] - 2, pos[0] + 3):
        for col in range(pos[1] - 2, pos[1] + 3):
            if (row != pos[0]) and (col != pos[1]) and white_piece_on_pos((row, col), board):
                if (type(board[row][col]) is Horse) and possible_position_horse_white((row, col), pos, board):
                    return False

    return True


def king_black_not_under_threat_far(pos, board):
    """
    Consider a queen on the given position, search for all enemy-pieces a queen could take at this position. If the piece
    that this queen could obtain also could obtain us, then this piece is a threat to our king, and thus this position is
    not a valid position. Pos will be within the board.

    :param pos: the position that must be checked
    :param board: our board
    :return True if not a threat
    """
    from Models.Queen import Queen
    from Models.Tower import Tower
    from Models.Bishop import Bishop

    # Up
    end_pos = pos[0] + 1, pos[1]
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] + 1, end_pos[1]
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Down
    end_pos = pos[0] - 1, pos[1]
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] - 1, end_pos[1]
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Left
    end_pos = pos[0], pos[1] - 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0], end_pos[1] - 1
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Right
    end_pos = pos[0], pos[1] + 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0], end_pos[1] + 1
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Tower) | (type(obj) is Queen):
            return False

    # Top-Right
    end_pos = pos[0] + 1, pos[1] + 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] + 1, end_pos[1] + 1
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    # Top-Left
    end_pos = pos[0] + 1, pos[1] - 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] + 1, end_pos[1] - 1
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    # Bottom-Right
    end_pos = pos[0] - 1, pos[1] + 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] - 1, end_pos[1] + 1
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    # Bottom-Left
    end_pos = pos[0] - 1, pos[1] - 1
    while pos_within_board(end_pos) and (not piece_on_pos(end_pos, board)):
        end_pos = end_pos[0] - 1, end_pos[1] - 1
    if pos_within_board(end_pos) and white_piece_on_pos(end_pos, board):
        obj = board[end_pos[0]][end_pos[1]]
        if (type(obj) is Bishop) | (type(obj) is Queen):
            return False

    return True
