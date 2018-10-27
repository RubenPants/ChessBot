from Models.Board import *

string = "PW"
points = 1


class Pawn:
    def __init__(self, stri="PW"):
        self.string = stri
        self.im_b = "Images/" + stri + "B.jpg"
        self.im_w = "Images/" + stri + "W.jpg"
        if "W" in stri:
            self.points = points
        else:
            self.points = -points


def possible_position_pawn_white(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if (end_pos[0] == start_pos[0] + 1) and (abs(end_pos[1] - start_pos[1]) == 1) and black_piece_on_pos(end_pos,
                                                                                                         board):
        return True
    elif (end_pos[0] == start_pos[0] + 1) and (end_pos[1] == start_pos[1]) and (not piece_on_pos(end_pos, board)):
        return True
    elif (start_pos[0] == 1) and (end_pos[0] == 3) and (start_pos[1] == end_pos[1]) and (
    not piece_on_pos(end_pos, board)) \
            and (not piece_on_pos([2, end_pos[1]], board)):
        return True
    return False


def valid_positions_pawn_white(start_pos, board):
    """
    :return A list with all possible positions for a white pawn
    """
    list = []
    for row in [start_pos[0] + 1, start_pos[0] + 2]:
        for col in range(8):
            pos = row, col
            if (possible_position_pawn_white(start_pos, pos, board)) and pos_within_board(pos):
                list.append(pos)
    return list


def possible_position_pawn_black(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if (end_pos[0] == start_pos[0] - 1) and (abs(end_pos[1] - start_pos[1]) == 1) and white_piece_on_pos(end_pos,
                                                                                                         board):
        return True
    elif (end_pos[0] == start_pos[0] - 1) and (end_pos[1] == start_pos[1]) and (not piece_on_pos(end_pos, board)):
        return True
    elif (start_pos[0] == 6) and (end_pos[0] == 4) and (start_pos[1] == end_pos[1]) and (
    not piece_on_pos(end_pos, board)) \
            and (not piece_on_pos([5, end_pos[1]], board)):
        return True
    return False


def valid_positions_pawn_black(start_pos, board):
    """
    :return A list with all possible positions for a black pawn
    """
    list = []
    for row in [start_pos[0] - 1, start_pos[0] - 2]:
        for col in range(8):
            pos = row, col
            if (possible_position_pawn_black(start_pos, pos, board)) and (pos_within_board(pos)):
                list.append(pos)
    return list
