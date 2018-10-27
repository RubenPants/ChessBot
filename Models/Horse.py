from Models.Board import *

string = "HW"
points = 3


class Horse:
    def __init__(self, stri="HW"):
        self.string = stri
        self.im_b = "Images/" + stri + "B.jpg"
        self.im_w = "Images/" + stri + "W.jpg"
        if "W" in stri:
            self.points = points
        else:
            self.points = -points


def possible_position_horse_white(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if end_pos[0] < 0 | end_pos[1] < 0 | end_pos[0] > 7 | end_pos[1] > 7:
        return False
    if ((abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1]) == 3) and
            ((start_pos[0] != end_pos[0]) and (start_pos[1] != end_pos[1])) and
            not white_piece_on_pos(end_pos, board)):
        return True
    return False


def valid_positions_horse_white(start_pos, board):
    """
    :return A list with all possible positions given a white horse
    """
    list = []
    for row in range(8):
        for col in range(8):
            pos = row, col
            if (possible_position_horse_white(start_pos, pos, board)) and (pos_within_board(pos)):
                list.append(pos)
    return list


def possible_position_horse_black(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if ((abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1]) == 3) and
            ((start_pos[0] != end_pos[0]) and (start_pos[1] != end_pos[1])) and (
            not black_piece_on_pos(end_pos, board))):
        return True
    return False


def valid_positions_horse_black(start_pos, board):
    """
    :return A list with all possible positions given a black horse
    """
    list = []
    for row in range(8):
        for col in range(8):
            pos = row, col
            if (possible_position_horse_black(start_pos, pos, board)) and (pos_within_board(pos)):
                list.append(pos)
    return list
