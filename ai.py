from piecesboard import Piece,Board
from game import Game


import copy


def evaluate_board(board_obj,player):
    #   if player is -1 then its black turn,1 is white turn
    from math import sqrt

    def count_valid_moves(piece):
        """Count valid moves for the specified piece."""
        return len(piece.valid_moves_func()) if piece else 0

    def find_piece_by_position(board_obj, position):
        """Find the piece object at the given position."""
        for piece in board_obj.pieces:
            if piece.position == position:
                return piece
        return None

    def calculate_distance(pos1, pos2):
        """Calculate Euclidean distance between two positions."""
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    # Find the positions of the queens

    white_queen_pos = board_obj.board_logic.find_piece_position(2)  # Assuming 2 represents the white queen
    black_queen_pos = board_obj.board_logic.find_piece_position(-2)  # Assuming -2 represents the black queen

    # Get the corresponding Piece objects
    white_queen = find_piece_by_position(board_obj, white_queen_pos) if white_queen_pos else None
    black_queen = find_piece_by_position(board_obj, black_queen_pos) if black_queen_pos else None

    # Calculate mobility scores
    if player == -1:
        opponent_queen_mobility = count_valid_moves(white_queen) if white_queen else 0
        own_queen_mobility = count_valid_moves(black_queen) if black_queen else 0

        # Calculate proximity of AI pieces to opponent queen
        proximity_score = 0
        if white_queen:
            for piece in board_obj.pieces:
                x, y = piece.position
                if ((x > 0) and (y > 0)) and piece.type in [-1, -2]:  # AI's pieces
                    distance = calculate_distance(piece.position, white_queen.position)
                    proximity_score += max(0, 10 - distance)  # Reward closer pieces
    else:
        opponent_queen_mobility = count_valid_moves(black_queen) if black_queen else 0
        own_queen_mobility = count_valid_moves(white_queen) if white_queen else 0

        # Calculate proximity of AI pieces to opponent queen
        proximity_score = 0
        if black_queen:
            for piece in board_obj.pieces:
                x, y = piece.position
                if ((x > 0) and (y > 0)) and piece.type in [1, 2]:  # AI's pieces
                    distance = calculate_distance(piece.position, black_queen.position)
                    proximity_score += max(0, 30 - distance)  # Reward closer pieces

    # Fallback to piece values if queens are missing
    # piece_value_score = sum(piece.value for piece in board_obj.pieces if piece.position != (-1, -1))
    piece_value_score = 0
    for piece in board_obj.pieces:
        x, y = piece.position
        if(x > 0) and (y > 0):
            piece_value_score = piece_value_score + piece.value
    # Calculate the final score
    score = 0
    if white_queen or black_queen:
        # Use mobility and proximity if queens are present
        score -= opponent_queen_mobility * 10  # Penalize opponent queen mobility
        score += own_queen_mobility * 5  # Reward AI queen mobility
        score += proximity_score  # Add proximity score
    else:
        # Fallback to piece value-based scoring
        score += piece_value_score

    return score



def get_all_possible_moves(board, piece_type):#T
    """
    Get all possible moves for a given piece type (white or black).
    
    Args:
    - board (Board): The game board object containing all pieces and their positions.
    - piece_type (int): The piece type for which to generate moves (1 for white, -1 for black).
    
    Returns:
    - list of tuples: Each tuple represents a move in the form of ((starting_position), (valid_move_position)).
    """
    all_moves = []
    for piece in board.pieces:
        if piece_type < 0:
            valid = piece.valid_moves_func()
            if(valid):
                if piece.type == -1 or piece.type == -2:
                    for valid_move in valid:
                        all_moves.append((piece.position, valid_move))
        else:
            valid = piece.valid_moves_func()
            if(valid):
                if piece.type == 1 or piece.type == 2:
                    for valid_move in valid:
                        if valid_move != piece.position:
                            all_moves.append((piece.position, valid_move)) 

    if not all_moves:
        print(f"No valid moves for pieces of type {piece_type}.")
    return all_moves


def game_over(board):
    def is_surrounded(position):
        """Check if a piece at the given position is completely surrounded."""
        x, y = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if any adjacent cell is empty
            if 0 <= nx < board.board_logic.size and 0 <= ny < board.board_logic.size and board.board_logic.board_2d[nx][ny] == 0:
                return False  # Found an empty adjacent cell
        return True  # All adjacent cells are occupied

    def find_piece_position(board, piece_value):
        """Find the position of a specific piece on the board."""
        for x in range(board.board_logic.size):
            for y in range(board.board_logic.size):
                if board.board_logic.board_2d[x][y] == piece_value:
                    return (x, y)
        return None

    # Find the queens' positions
    black_queen_pos = find_piece_position(board, -2)
    white_queen_pos = find_piece_position(board, 2)

    # Determine if the queens are surrounded
    black_queen_surrounded = black_queen_pos and is_surrounded(black_queen_pos)
    white_queen_surrounded = white_queen_pos and is_surrounded(white_queen_pos)

    # Decide the winner based on the game state
    if black_queen_surrounded and white_queen_surrounded:
        return 3  # Both queens are surrounded
    elif black_queen_surrounded:
        return 1  # Black queen is surrounded
    elif white_queen_surrounded:
        return 2  # White queen is surrounded
    else:
        return 0  # Game is not over


def minimax(board, depth, is_maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    if is_maximizing_player:  # AI's turn (Black)
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, -1):  # -1 is Black
            new_board =board.custom_copy()
            new_board.board_logic.make_move(move)
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:  # Opponent's turn (White)
        min_eval = float('inf')
        for move in get_all_possible_moves(board, 1):  # 1 is White
            new_board =board.custom_copy()
            new_board.board_logic.make_move(move)
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval
    

def minimax_with_alpha_beta(board,player,depth, alpha, beta, is_maximizing_player):
    """
    Minimax function with alpha-beta pruning.
    """
    if depth == 0 or game_over(board):
        if not board:
            return 0
        else:
            return evaluate_board(board,player)

    if is_maximizing_player:  # AI's turn (Black)
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, player):  # -1 is Black
            new_board = board.custom_copy()
            start, end = move
            piece = find_piece_by_position(new_board, start)
            x, y = start
            if (x < 0) and (y < 0):
                new_board.board_logic.place_piece(piece, end)
            else:
                new_board.board_logic.make_move(move)

            evall = minimax_with_alpha_beta(new_board,(-1*player) ,depth - 1, alpha, beta, False)
            max_eval = max(max_eval, evall)
            alpha = max(alpha, evall)
            if beta <= alpha:  # Prune
                break
        return max_eval
    else:  # Opponent's turn (White)
        min_eval = float('inf')
        for move in get_all_possible_moves(board, player):  # 1 is White
            new_board = board.custom_copy()
            start, end = move
            piece = find_piece_by_position(new_board, start)
            x, y = start
            if (x < 0) and (y < 0):
                new_board.board_logic.place_piece(piece, end)
            else:
                new_board.board_logic.make_move(move)
            evall = minimax_with_alpha_beta(new_board,(-1*player) ,depth - 1, alpha, beta, True)
            min_eval = min(min_eval, evall)
            beta = min(beta, evall)
            if beta <= alpha:  # Prune
                break
        return min_eval



def find_best_move(board, depth):
    best_move = None
    best_value = float('-inf')
    all_moves = get_all_possible_moves(board, -1)  # -1 is Black (AI)
    
    print("\nAll Moves:")
    print(all_moves)

    if not all_moves:
        print("No possible moves for the AI.")
        return None  # No moves available
    
    for move in all_moves:
        new_board =board.custom_copy()
        new_board.board_logic.make_move(move)
        move_value = minimax(new_board, depth-1, False)
        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

def find_best_move_alpha_beta(board, depth):
    """
    Finds the best move for the AI using minimax with alpha-beta pruning.
    """
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    all_moves = get_all_possible_moves(board, -1)  # -1 is Black (AI)

    print("\nAll Moves:")
    print(all_moves)

    if not all_moves:
        print("No possible moves for the AI.")
        return None  # No moves available

    for move in all_moves:
        new_board = board.custom_copy()
        new_board.board_logic.make_move(move)
            
        move_value = minimax_with_alpha_beta(new_board, depth - 1, alpha, beta, False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
        alpha = max(alpha, best_value)

    return best_move

def find_piece_by_position(board_obj, position):
    """Find the piece object at the given position."""
    for piece in board_obj.pieces:
        if piece.position == position:
            return piece
    return None

def find_best_move_with_iterative_deepening(board,player,max_depth,time_limit=5):
    """
    Finds the best move using iterative deepening with alpha-beta pruning.
    player: -1 for Black (AI), 1 for White.
    max_depth: Maximum depth to search to.
    time_limit: Optional time limit (in seconds) to stop the search.
    """
    import time

    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    start_time = time.time()
    
    for depth in range(1, max_depth + 1):  # Iteratively deepen the search
        print(f"Searching at depth {depth}...")
        current_best_move = None
        current_best_value = float('-inf')

        for move in get_all_possible_moves(board, player):  # -1 is Black (AI)
            new_board = board.custom_copy()
            start, end = move
            piece = find_piece_by_position(new_board, start)
            x, y = start
            if (x < 0) and (y < 0):
                new_board.board_logic.place_piece(piece, end)
            else:
                new_board.board_logic.make_move(move)
            move_value = minimax_with_alpha_beta(new_board,(-1*player) ,depth - 1, alpha, beta, False)

            if move_value > current_best_value:
                current_best_value = move_value
                current_best_move = move

            alpha = max(alpha, current_best_value)

            # Check time limit
            if time_limit and time.time() - start_time > time_limit:
                print("Time limit reached during depth", depth)
                return best_move

        # Update the best move found at the current depth
        if current_best_move is not None:
            best_move = current_best_move

        # Check time limit
        if time_limit and time.time() - start_time > time_limit:
            print("Time limit reached.")
            break

    return best_move




#
#
#
# # Create a board with size 3x3
# board = Board(10)
#     # board.board_2d[5][5] = -1
#     # board.board_2d[6][5] = -1
#     # board.board_2d[6][3] =  1
#     # board.board_2d[7][4] =  1
#
#
#
#
# piece1 =Piece(-1,(-1,-1),"beetle",board)
# piece2 =Piece(1,(-1,-1),"beetle",board)
# piece3 =Piece(1,(-1,-1),"hopper",board)
# piece4 =Piece(1,(-1,-1),"hopper",board)
# piece5 =Piece(1,(-1,-1),"hopper",board)
# piece6 =Piece(1,(-1,-1),"hopper",board)
# piece7 =Piece(1,(-1,-1),"hopper",board)
# piece8 =Piece(1,(-1,-1),"hopper",board)
# piece9 =Piece(1,(-1,-1),"hopper",board)
# piece10 =Piece(1,(-1,-1),"hopper",board)
# piece11 =Piece(1,(-1,-1),"hopper",board)
#
# print("\nBefore Place\n")
# board.display()
#
#
#
#
#
#
# # test of the add piece
#     # board.place_piece(piece1,(5,5))
#
#     # board.place_piece(piece2,(6,6))
#
#     # x = []
#     # x = piece3.valid_moves_func()
#
#     # print(x)
#
#
# board.place_piece(piece1,(5,3))
#
# board.place_piece(piece2,(6,4))
#
# board.place_piece(piece3,(5,2))
# board.place_piece(piece4,(4,3))
# board.place_piece(piece5,(5,4))
# board.place_piece(piece6,(5,5))
# board.place_piece(piece7,(6,5))
# board.place_piece(piece8,(7,4))
#     # board.place_piece(piece9,(4,2))
#     # board.place_piece(piece10,(3,2))
#     # board.place_piece(piece11,(2,3))
# print("\nAfter Place\n")
# board.display()
#
#
# best_move = find_best_move_with_iterative_deepening(board,-1 ,5, 5)
#
#
# # # Test finding the best move
# # best_move = find_best_move_alpha_beta(board, depth=4)
# if best_move:
#     print("Best Move:", best_move)
#     board = board.make_move(best_move)
#     print("Board after Best Move:")
#     board.display()
# else:
#     print("No valid moves found. Game may be over.")
#
#
#


