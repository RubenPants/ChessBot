from Models.Tower import *
from Models.Bishop import *

string = "QW"
points = 9


class Queen:
    def __init__(self, stri="QW"):
        self.string = stri
        self.im_b = "Images/" + stri + "B.jpg"
        self.im_w = "Images/" + stri + "W.jpg"
        if "W" in stri:
            self.points = points
        else:
            self.points = -points


def possible_position_queen_white(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if start_pos == end_pos:
        return False
    if (((abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1])) |  # Bishop
         ((start_pos[0] == end_pos[0]) | (start_pos[1] == end_pos[1]))) and  # Tower
            (not white_piece_on_pos(end_pos, board))):
        return True
    return False


def valid_positions_queen_white(start_pos, board):
    """
    :return A list with all possible positions given a white queen
    """
    list = []

    # Tower
    tower_list = valid_positions_tower_white(start_pos, board)
    if len(tower_list) > 0:
        for pos in tower_list:
            list.append(pos)

    # Bishop
    bishop_list = valid_positions_bishop_white(start_pos, board)
    if len(bishop_list) > 0:
        for pos in bishop_list:
            list.append(pos)

    return list


def possible_position_queen_black(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if start_pos == end_pos:
        return False
    if (((abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1])) |  # Bishop
         ((start_pos[0] == end_pos[0]) | (start_pos[1] == end_pos[1]))) and  # Tower
            (not black_piece_on_pos(end_pos, board))):
        return True
    return False


def valid_positions_queen_black(start_pos, board):
    """
    :return A list with all possible positions given a black queen
    """
    list = []

    # Tower
    tower_list = valid_positions_tower_black(start_pos, board)
    if len(tower_list) > 0:
        for pos in tower_list:
            list.append(pos)

    # Bishop
    bishop_list = valid_positions_bishop_black(start_pos, board)
    if len(bishop_list) > 0:
        for pos in bishop_list:
            list.append(pos)

    return list
