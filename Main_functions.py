from random import randrange
from Models.King import *
from Models.Queen import *
from Models.Tower import *
from Models.Bishop import *
from Models.Horse import *
from Models.Pawn import *

"""
The depth of the searching-tree (alpha-beta-pruning)
"""
depth_tree = 3  # TODO: Change the depth of the search tree here


def game_active():
    """
    Determine based on the title in the top left corner if the game is active.

    :return: True if the game is active
    """
    im = region_grabber((0, 0, 110, 30))
    pos = imagesearcharea("Images/title.jpg", 0, 0, 0, 0, 0.9, im)  # Black background
    return pos != [-1, -1]


def compute_best_move(board):
    """
    Calculate the best next-move possible given a certain board.

    :param board: Our own board
    :return: (from-position, to-position)
    """
    best_node = alphabeta([0, []], depth_tree, float("-inf"), float("inf"), True, board)

    if (best_node[0] == float("inf")) and (len(best_node[1]) == 1):
        return best_node[1][0], True
    return best_node[1][0], False


def alphabeta(node, depth, alpha, beta, maximizingPlayer, board):
    """
    Implementation of the minimax algorithm with alpha-beta pruning.

    :initialization: Initialize this algorithm with a starting node of: [0, []]
    :param node: A node represents a board state with the transactions needed to become this state, and the
        corresponding score --> node = [score, [(from_pos, to_pos), ..., (from_pos, to_pos)]]
    :param depth: The depth the tree will descend after this stage
    :param alpha, beta: Algorithm specific
    :param maximizingPlayer: A boolean determining if the max or min part of the algorihm should run
    :param board: Own board
    :return: The optimal path to maximize the total score: [max_score, [path_to_max_score]]
    """
    if depth == 0:
        return node

    if maximizingPlayer:  # This is us
        best_node = float("-inf"), []

        # Get child nodes and put them in the proper form
        possible_moves = get_possible_moves_white(node, board)
        child_nodes = []
        for set_moves in possible_moves:
            child_nodes.append([get_total_score(set_moves, board), set_moves])

        if len(child_nodes) == 0:
            return [float("-inf"), node[1]]  # We get put check mate (crash if node[1] == [])

        best_nodes_list = []
        i = randrange(len(child_nodes))
        for child in child_nodes[i:] + child_nodes[:i]:
            rec_child = alphabeta(child, depth - 1, alpha, beta, False, board)
            if best_node[0] < rec_child[0]:
                best_nodes_list = [rec_child]
                best_node = rec_child
                alpha = max(alpha, best_node[0])
                if alpha >= beta:
                    if alpha == float("inf"):
                        return best_node
                    return [float("inf"), []]  # Pruning
            elif best_node[0] == rec_child[0]:
                best_nodes_list.append(rec_child)
        return random.choice(best_nodes_list)
    else:  # minimizingPlayer
        worst_node = float("inf"), []

        # Get child nodes and put them in the proper form
        possible_moves = get_possible_moves_black(node, board)
        child_nodes = []
        for set_moves in possible_moves:
            child_nodes.append([get_total_score(set_moves, board), set_moves])

        if len(child_nodes) == 0:
            if is_checkmate(node[1], board):
                return [float("inf"), node[1]]  # Check-mate
            else:
                return [float("-inf"), node[1]]  # Draw

        worst_nodes_list = []
        for child in child_nodes:
            rec_child = alphabeta(child, depth - 1, alpha, beta, True, board)
            if worst_node[0] > rec_child[0]:
                worst_nodes_list = [rec_child]
                worst_node = rec_child
                beta = min(beta, worst_node[0])
                if alpha >= beta:
                    return [float("-inf"), []]  # Pruning
            elif worst_node[0] == rec_child[0]:
                worst_nodes_list.append(rec_child)
        return random.choice(worst_nodes_list)


def is_checkmate(path, board):
    """
    Check if the black king is checkmate.

    :param path: The path needed to get board to check-state
    :param board: Own board
    :return: True if black king is under checkmate, False otherwise (black king not under checkmate, and when black king
        simply has no where to go and not under checkmate)
    """
    checkmate = False
    obj_list = []

    # Get board to end-state
    for pos_tuple in path:
        obj_list.append(board[pos_tuple[1][0]][pos_tuple[1][1]])
        move_on_own_board(pos_tuple[0], pos_tuple[1], board)

    # Get position black king
    pos_king = [-1, -1]
    for row in range(8):
        for col in range(8):
            if piece_on_pos((row, col), board):
                if board[row][col].string == "KB":
                    pos_king = [row, col]

    # Go through every possible checkmate (white) piece
    if pos_king != [-1, -1]:
        for row in range(8):
            for col in range(8):
                if piece_on_pos((row, col), board) and (not checkmate):
                    obj = board[row][col]
                    if (obj.string == "QW") and possible_position_queen_white((row, col), pos_king, board):
                        checkmate = True
                    elif (obj.string == "TW") and possible_position_tower_white((row, col), pos_king, board):
                        checkmate = True
                    elif (obj.string == "BW") and possible_position_bishop_white((row, col), pos_king, board):
                        checkmate = True
                    elif (obj.string == "HW") and possible_position_horse_white((row, col), pos_king, board):
                        checkmate = True

    # Get board back to init-state
    for i in reversed(range(len(path))):
        move_on_own_board(path[i][1], path[i][0], board)
        board[path[i][1][0]][path[i][1][1]] = obj_list[i]  # Listception

    return checkmate


def get_total_score(list, board):
    """
    Calculate the score of a board in a given state.

    :param list: A list of nodes given position switches
        list: [node0, node1, ...]
        node: [(from_pos), (to_pos)]
    :param board: Own board
    :return: The score, the higher the better
    """
    obj_list = []

    # Get board to end-state
    for pos_tuple in list:
        obj_list.append(board[pos_tuple[1][0]][pos_tuple[1][1]])
        move_on_own_board(pos_tuple[0], pos_tuple[1], board)

    # Calculate the score
    tot_score = 0
    for row in range(8):
        for col in range(8):
            if piece_on_pos((row, col), board):
                obj = board[row][col]
                tot_score += obj.points

                # Improve score calculation
                if obj.string == "PW":
                    if row == 7:
                        tot_score += 5  # Pawn becomes queen
                    else:
                        tot_score += 0.01 * (row * row)
                elif obj.string == "PB":
                    if row == 0:
                        tot_score -= 5  # Pawn becomes queen
                    else:
                        tot_score -= 0.01 * ((7 - row) * (7 - row))
                elif (obj.string == "HW") | (obj.string == "BW") | (obj.string == "QW"):
                    if row > 0:
                        tot_score += 0.1

    # Get board back to init-state
    for i in reversed(range(len(list))):
        move_on_own_board(list[i][1], list[i][0], board)
        board[list[i][1][0]][list[i][1][1]] = obj_list[i]  # Listception

    return tot_score


def get_possible_moves_white(item, board):
    """
    Give all the possible moves given a certain situation.

    :param item:
        item[0] the score of the node
        item[1] the path leading to this score
    :param board: The initial board on which the minimax algorithm has been called
    """
    obj_list = []

    # Get board to end-state
    for pos_tuple in item[1]:
        obj_list.append(board[pos_tuple[1][0]][pos_tuple[1][1]])
        move_on_own_board(pos_tuple[0], pos_tuple[1], board)

    new_positions = get_all_positions(board, True)
    for i in range(len(new_positions)):
        new_positions[i] = item[1] + [new_positions[i]]

    # Get board back to init-state
    for i in reversed(range(len(item[1]))):
        move_on_own_board(item[1][i][1], item[1][i][0], board)
        board[item[1][i][1][0]][item[1][i][1][1]] = obj_list[i]

    return new_positions


def get_possible_moves_black(item, board):
    """
    Give all the possible moves given a certain situation.

    :param item:
        item[0] the score of the node
        item[1] the path leading to this score
    :param board: The initial board on which the minimax algorithm has been called
    """
    obj_list = []

    # Get board to end-state
    for pos_tuple in item[1]:
        obj_list.append(board[pos_tuple[1][0]][pos_tuple[1][1]])
        move_on_own_board(pos_tuple[0], pos_tuple[1], board)

    new_positions = get_all_positions(board, False)
    for i in range(len(new_positions)):
        new_positions[i] = item[1] + [new_positions[i]]

    # Get board back to init-state
    for i in reversed(range(len(item[1]))):
        move_on_own_board(item[1][i][1], item[1][i][0], board)
        board[item[1][i][1][0]][item[1][i][1][1]] = obj_list[i]

    return new_positions


def get_all_positions(board, white_turn):
    """
    Get all the possible positions given a board-situation.

    :param board: The given board (own, up-to-date)
    :param white_turn: True if it is white its turn, False if its black's
    :return: A list containing all the possible positions
    """
    list = []
    for row in range(8):
        for col in range(8):
            # White
            if white_turn and white_piece_on_pos((row, col), board):
                obj = board[row][col]
                if type(obj) is Pawn:
                    for valid_pos in valid_positions_pawn_white((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Tower:
                    for valid_pos in valid_positions_tower_white((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Bishop:
                    for valid_pos in valid_positions_bishop_white((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Horse:
                    for valid_pos in valid_positions_horse_white((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Queen:
                    for valid_pos in valid_positions_queen_white((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is King:
                    for valid_pos in valid_positions_king_white((row, col), board):
                        list.append(((row, col), valid_pos))
            # Black
            elif (not white_turn) and black_piece_on_pos((row, col), board):
                obj = board[row][col]
                if type(obj) is Pawn:
                    for valid_pos in valid_positions_pawn_black((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Tower:
                    for valid_pos in valid_positions_tower_black((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Bishop:
                    for valid_pos in valid_positions_bishop_black((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Horse:
                    for valid_pos in valid_positions_horse_black((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is Queen:
                    for valid_pos in valid_positions_queen_black((row, col), board):
                        list.append(((row, col), valid_pos))
                elif type(obj) is King:
                    for valid_pos in valid_positions_king_black((row, col), board):
                        list.append(((row, col), valid_pos))
    return list


def get_score_pos(pos, board):
    """
    Return the score of the piece on the given position (color is irrelevant).
    """
    if piece_on_pos(pos, board):
        return board[pos[0]][pos[1]].points
    else:
        return 0


def move_piece(from_pos, to_pos, start_board, dim_square, board):
    """
    Move a white piece from the given location to a given location.

    :param from_pos: Initial position of the piece
    :param to_pos: The end-position of the given piece
    :param start_board: The bottom left corner of the real board
    :param dim_square: The dimension of a square on the real board
    :param board: Our own board
    """
    # From
    pyautogui.moveTo(start_board[0] + (from_pos[1] + 0.5) * dim_square[0],
                     start_board[1] - (from_pos[0] + 0.5) * dim_square[1],
                     0.2)
    pyautogui.click()

    # To
    pyautogui.moveTo(start_board[0] + (to_pos[1] + 0.5) * dim_square[0],
                     start_board[1] - (to_pos[0] + 0.5) * dim_square[1],
                     0.2)
    pyautogui.click()

    # Update on own board
    move_on_own_board(from_pos, to_pos, board)


def move_on_own_board(from_pos, to_pos, board):
    """
    Move a piece on our own board from a given position to a given position.

    :param from_pos: Initial position of the piece
    :param to_pos: The end-position of the given piece
    :param board: Our own board
    """
    obj = board[from_pos[0]][from_pos[1]]
    board[from_pos[0]][from_pos[1]] = None
    board[to_pos[0]][to_pos[1]] = obj


def check_complete_board(start_pos, dim_square, board):
    """
    Go through every position of the board and update our own board with the real board.

    :param start_pos: Starting position on the real board
    :param dim_square: The dimension of one square on the real board
    :param board: Own board
    :return: True if a piece has moved, False otherwise
    """
    change = False
    for row in range(8):
        for col in range(8):
            # Grab image on real board
            im = region_grabber((start_pos[0] + col * dim_square[0],
                                 start_pos[1] - (row + 1.0) * dim_square[1],
                                 start_pos[0] + (col + 1.0) * dim_square[0],
                                 start_pos[1] - row * dim_square[1]))

            # Check if piece corresponds with piece on board if there is a piece
            if piece_on_pos((row, col), board):
                obj = board[row][col]
                if (row + col) % 2 == 0:  # Black background
                    pos = imagesearcharea(obj.im_b, 0, 0, 0, 0, 0.9, im)
                    if pos != [-1, -1]:
                        continue
                else:  # White background
                    pos = imagesearcharea(obj.im_w, 0, 0, 0, 0, 0.9, im)
                    if pos != [-1, -1]:
                        continue

            # Else --> Go through every possible image
            if (row + col) % 2 == 0:  # Black background
                # Pawn
                pos = imagesearcharea("Images/PWB.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Pawn("PW")
                    continue
                pos = imagesearcharea("Images/PBB.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Pawn("PB")
                    continue
                # Tower
                pos = imagesearcharea("Images/TWB.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Tower("TW")
                    continue
                pos = imagesearcharea("Images/TBB.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Tower("TB")
                    continue
                # Horse
                pos = imagesearcharea("Images/HWB.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Horse("HW")
                    continue
                pos = imagesearcharea("Images/HBB.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Horse("HB")
                    continue
                # Bishop
                pos = imagesearcharea("Images/BWB.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Bishop("BW")
                    continue
                pos = imagesearcharea("Images/BBB.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Bishop("BB")
                    continue
                # King
                pos = imagesearcharea("Images/KWB.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = King("KW")
                    continue
                pos = imagesearcharea("Images/KBB.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = King("KB")
                    continue
                # Queen
                pos = imagesearcharea("Images/QWB.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Queen("QW")
                    continue
                pos = imagesearcharea("Images/QBB.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Queen("QB")
                    continue
                board[row][col] = None
            else:  # White background
                # Pawn
                pos = imagesearcharea("Images/PWW.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Pawn("PW")
                    continue
                pos = imagesearcharea("Images/PBW.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Pawn("PB")
                    continue
                # Tower
                pos = imagesearcharea("Images/TWW.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Tower("TW")
                    continue
                pos = imagesearcharea("Images/TBW.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Tower("TB")
                    continue
                # Horse
                pos = imagesearcharea("Images/HWW.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Horse("HW")
                    continue
                pos = imagesearcharea("Images/HBW.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Horse("HB")
                    continue
                # Bishop
                pos = imagesearcharea("Images/BWW.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Bishop("BW")
                    continue
                pos = imagesearcharea("Images/BBW.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Bishop("BB")
                    continue
                # King
                pos = imagesearcharea("Images/KWW.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = King("KW")
                    continue
                pos = imagesearcharea("Images/KBW.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = King("KB")
                    continue
                # Queen
                pos = imagesearcharea("Images/QWW.jpg", 0, 0, 0, 0, 0.9, im)  # White
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Queen("QW")
                    continue
                pos = imagesearcharea("Images/QBW.jpg", 0, 0, 0, 0, 0.9, im)  # Black
                if pos != [-1, -1]:
                    change = True
                    board[row][col] = Queen("QB")
                    continue
                board[row][col] = None

    if change:
        pyautogui.moveTo(start_pos[0] + 4 * dim_square[0],
                         start_pos[1] - 4 * dim_square[1], 0.2)

    return change


def is_image(pos, image, start_pos, dim_square):
    """
    Check if image in real board. Only for testing purposes.
    """
    # Grab image on real board
    im = region_grabber((start_pos[0] + pos[1] * dim_square[0],
                         start_pos[1] - (pos[0] + 1.0) * dim_square[1],
                         start_pos[0] + (pos[1] + 1.0) * dim_square[0],
                         start_pos[1] - pos[0] * dim_square[1]))

    pos_image = imagesearcharea(image, 0, 0, 0, 0, 0.9, im)
    return pos_image != [-1, -1]


def check_got_promotion():
    """
    Check if pawn got promotion to become a queen. If so, make pawn queen and wait a half a second.
    """
    im = region_grabber((550, 250, 815, 320))  # Hardcoded
    pos = imagesearcharea("Images/promotion_queen.jpg", 0, 0, 0, 0, 0.9, im)
    if pos != [-1, -1]:
        print("Got promotion")
        pos_image = [550 + pos[0], 250 + pos[1]]
        click_image("Images/promotion_queen.jpg", pos_image, "left", 0.2)
        time.sleep(0.5)
        return True
    return False
