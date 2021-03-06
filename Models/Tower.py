from Models.Board import *

string = "TW"
points = 5


class Tower:
    def __init__(self, stri="TW"):
        self.string = stri
        self.im_b = "Images/" + stri + "B.jpg"
        self.im_w = "Images/" + stri + "W.jpg"
        if "W" in stri:
            self.points = points
        else:
            self.points = -points


def possible_position_tower_white(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if start_pos == end_pos:
        return False
    if (((start_pos[0] == end_pos[0]) | (start_pos[1] == end_pos[1])) and (not white_piece_on_pos(end_pos, board)) and
            (pos_within_board(end_pos))):
        return True
    return False


def valid_positions_tower_white(start_pos, board):
    """
    :return A list with all possible positions given a white tower
    """
    list = []

    # Up
    no_black = True
    end_pos = start_pos[0] + 1, start_pos[1]
    while possible_position_tower_white(start_pos, end_pos, board) and no_black:
        list.append(end_pos)
        if black_piece_on_pos(end_pos, board):
            no_black = False
        else:
            end_pos = end_pos[0] + 1, end_pos[1]

    # Down
    no_black = True
    end_pos = start_pos[0] - 1, start_pos[1]
    while possible_position_tower_white(start_pos, end_pos, board) and no_black:
        list.append(end_pos)
        if black_piece_on_pos(end_pos, board):
            no_black = False
        else:
            end_pos = end_pos[0] - 1, end_pos[1]

    # Left
    no_black = True
    end_pos = start_pos[0], start_pos[1] - 1
    while possible_position_tower_white(start_pos, end_pos, board) and no_black:
        list.append(end_pos)
        if black_piece_on_pos(end_pos, board):
            no_black = False
        else:
            end_pos = end_pos[0], end_pos[1] - 1

    # Right
    no_black = True
    end_pos = start_pos[0], start_pos[1] + 1
    while possible_position_tower_white(start_pos, end_pos, board) and no_black:
        list.append(end_pos)
        if black_piece_on_pos(end_pos, board):
            no_black = False
        else:
            end_pos = end_pos[0], end_pos[1] + 1

    return list


def possible_position_tower_black(start_pos, end_pos, board):
    """
    Check if new position is a valid position. No collision-detection yet
    """
    if not pos_within_board(end_pos):
        return False
    if start_pos == end_pos:
        return False
    if (((start_pos[0] == end_pos[0]) | (start_pos[1] == end_pos[1])) and (not black_piece_on_pos(end_pos, board)) and
            (pos_within_board(end_pos))):
        return True
    return False


def valid_positions_tower_black(start_pos, board):
    """
    :return A list with all possible positions given a white tower
    """
    list = []

    # Up
    no_white = True
    end_pos = start_pos[0] + 1, start_pos[1]
    while possible_position_tower_black(start_pos, end_pos, board) and no_white:
        list.append(end_pos)
        if white_piece_on_pos(end_pos, board):
            no_white = False
        else:
            end_pos = end_pos[0] + 1, end_pos[1]

    # Down
    no_white = True
    end_pos = start_pos[0] - 1, start_pos[1]
    while possible_position_tower_black(start_pos, end_pos, board) and no_white:
        list.append(end_pos)
        if white_piece_on_pos(end_pos, board):
            no_white = False
        else:
            end_pos = end_pos[0] - 1, end_pos[1]

    # Left
    no_white = True
    end_pos = start_pos[0], start_pos[1] - 1
    while possible_position_tower_black(start_pos, end_pos, board) and no_white:
        list.append(end_pos)
        if white_piece_on_pos(end_pos, board):
            no_white = False
        else:
            end_pos = end_pos[0], end_pos[1] - 1

    # Right
    no_white = True
    end_pos = start_pos[0], start_pos[1] + 1
    while possible_position_tower_black(start_pos, end_pos, board) and no_white:
        list.append(end_pos)
        if white_piece_on_pos(end_pos, board):
            no_white = False
        else:
            end_pos = end_pos[0], end_pos[1] + 1

    return list
