class Board:
    def __init__(self, size: int):
        self.size = size
        self.board_2d = [[0 for _ in range(size)] for _ in range(size)]
        self.pieces = []

    def add_piece(self, piece: 'Piece'):
        x, y = piece.position
        if self.board_2d[x][y] == 0:
            self.board_2d[x][y] = piece.type
            self.pieces.append(piece)

    def move_piece(self, piece: 'Piece', new_position: tuple[int, int]):
        x, y = piece.position
        new_x, new_y = new_position
        if self.board_2d[new_x][new_y] == 0:
            self.board_2d[x][y] = 0
            self.board_2d[new_x][new_y] = piece.type
            piece.position = new_position

    def remove_piece(self, piece: 'Piece'):
        x, y = piece.position
        self.board_2d[x][y] = 0
        self.pieces.remove(piece)

    def get_piece_at(self, position: tuple[int, int]) -> 'Piece':
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

class Piece:
    def __init__(self, type: int, position: tuple[int, int], insect_type: str, board: Board, value=5):
        """
        type
        -1 ---->black
        -2 -----> Queen Bee Black
         1 ----->white
         2 ---->Queen Bee White

        position
        -1,-1 --> outside the board
        """
        self.type = type
        self.position = position
        self.insect_type = insect_type
        self.valid_moves = None
        self.board = board
        self.value = value
        self.board.pieces.append(self)

    def check_coordinates(self, x: int, y: int):
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 == 0):
            return [(x-1, y), (x-1, y+1), (x, y+1), (x+1, y), (x, y-1), (x-1, y-1)]
        else:
            return [(x+1, y), (x+1, y-1), (x+1, y+1), (x, y-1), (x, y+1), (x-1, y)]

    def get_free_region_of_piece(self, piece: 'Piece'):
        x, y = piece.position
        neighbors = piece.check_coordinates(x, y)
        return [(nx, ny) for nx, ny in neighbors if self.board.board_2d[nx][ny] == 0]

    def get_occupied_region_of_piece(self, piece: 'Piece'):
        x, y = piece.position
        neighbors = piece.check_coordinates(x, y)
        return [(nx, ny) for nx, ny in neighbors if self.board.board_2d[nx][ny] != 0]

    def around_the_hive(self, x: int, y: int) -> list[tuple[int, int]]:
        occupied_regions = self.get_occupied_region_of_piece(self)
        free_regions = set(self.get_free_region_of_piece(self))

        free_around_neighbors = set()
        for nx, ny in occupied_regions:
            free_around_neighbors.update(self.get_free_region_of_piece(Piece(self.type, (nx, ny), self.insect_type, self.board)))

        return list(free_regions & free_around_neighbors)

    def check_free_to_slide(self, point1: tuple[int, int], point2: tuple[int, int]) -> bool:
        neighbors_point1 = set(self.check_coordinates(*point1))
        neighbors_point2 = set(self.check_coordinates(*point2))

        intersection = neighbors_point1 & neighbors_point2
        if len(intersection) < 2:
            return True

        x1, y1 = list(intersection)[0]
        x2, y2 = list(intersection)[1]
        return not (self.board.board_2d[x1][y1] != 0 and self.board.board_2d[x2][y2] != 0)

    def is_hive_connected(self):
        visited = set()
        all_pieces = [(i, j) for i in range(self.board.size) for j in range(self.board.size) if self.board.board_2d[i][j] != 0]

        if not all_pieces:
            return True

        def dfs(position):
            visited.add(position)
            for nx, ny in self.check_coordinates(*position):
                if (nx, ny) in all_pieces and (nx, ny) not in visited:
                    dfs((nx, ny))

        dfs(all_pieces[0])
        return len(visited) == len(all_pieces)

    def check_hive_connectivity_after_move(self, move):
        original_position = self.position
        x, y = original_position
        original_value = self.board.board_2d[move[0]][move[1]]

        self.board.board_2d[x][y] = 0
        self.board.board_2d[move[0]][move[1]] = self.type
        self.position = move

        hive_connected = self.is_hive_connected()

        self.board.board_2d[move[0]][move[1]] = original_value
        self.board.board_2d[x][y] = self.type
        self.position = original_position

        return hive_connected


class Ant(Piece):
    def __init__(self, type: int, position: tuple[int, int], board: Board, value=5):
        super().__init__(type, position, "Ant", board, value)

    def valid_moves_func(self):
        x, y = self.position
        valid_moves = set()
        initial_moves = self.around_the_hive(x, y)

        for move in initial_moves:
            if self.check_free_to_slide((x, y), move):
                valid_moves.add(move)

        previous_size = -1
        self.board.board_2d[x][y] = 0

        while len(valid_moves) != previous_size:
            previous_size = len(valid_moves)
            current_moves = list(valid_moves)

            for move_x, move_y in current_moves:
                additional_moves = self.around_the_hive(move_x, move_y)
                for new_move in additional_moves:
                    if self.check_free_to_slide((move_x, move_y), new_move):
                        valid_moves.add(new_move)

        self.board.board_2d[x][y] = self.type
        valid_moves.discard(self.position)
        return list(valid_moves)

class Spider(Piece):
    def __init__(self, type: int, position: tuple[int, int], board: Board, value=3):
        super().__init__(type, position, "Spider", board, value)

    def valid_moves_func(self):
        x, y = self.position
        moves = self.around_the_hive(x, y)
        moves = [m for m in moves if self.check_free_to_slide((x, y), m)]
        return moves if len(moves) <= 3 else moves[:3]

class Hopper(Piece):
    def __init__(self, type: int, position: tuple[int, int], board: Board, value=4):
        super().__init__(type, position, "Hopper", board, value)

    def valid_moves_func(self):
        x, y = self.position
        directions = self.check_coordinates(x, y)
        valid_moves = []

        for nx, ny in directions:
            while 0 <= nx < self.board.size and 0 <= ny < self.board.size and self.board.board_2d[nx][ny] != 0:
                nx += (nx - x)
                ny += (ny - y)

            if 0 <= nx < self.board.size and 0 <= ny < self.board.size and self.board.board_2d[nx][ny] == 0:
                valid_moves.append((nx, ny))

        return valid_moves

class QueenBee(Piece):
    def __init__(self, type: int, position: tuple[int, int], board: Board, value=9):
        super().__init__(type, position, "QueenBee", board, value)

    def valid_moves_func(self):
        x, y = self.position
        return [move for move in self.around_the_hive(x, y) if self.check_free_to_slide((x, y), move)]

class Beetle(Piece):
    def __init__(self, type: int, position: tuple[int, int], board: Board, value=8):
        super().__init__(type, position, "Beetle", board, value)

    def valid_moves_func(self):
        x, y = self.position
        return self.around_the_hive(x, y)



# Class Descriptions and Methods
# 1. Board
# Represents the game board for HIVE, holding the pieces and their positions.
#
# __init__(size: int): Initializes a board with a 2D grid and an empty list of pieces.
# add_piece(piece: 'Piece'): Adds a piece to the board if its position is unoccupied.
# move_piece(piece: 'Piece', new_position: tuple[int, int]): Moves a piece to a new position if the target position is empty.
# remove_piece(piece: 'Piece'): Removes a piece from the board and updates the grid.
# get_piece_at(position: tuple[int, int]): Returns the piece at the specified position or None.
# 2. Piece
# Base class for all game pieces with shared attributes and methods.
#
# __init__(type: int, position: tuple[int, int], insect_type: str, board: Board, value=5): Initializes a piece with its type, position, insect type, board reference, and value.
# check_coordinates(x: int, y: int): Returns neighboring coordinates for a given position.
# get_free_region_of_piece(piece: 'Piece'): Retrieves all empty neighboring tiles around a piece.
# get_occupied_region_of_piece(piece: 'Piece'): Retrieves all occupied neighboring tiles around a piece.
# around_the_hive(x: int, y: int): Returns valid free moves adjacent to both occupied and free regions around a piece.
# check_free_to_slide(point1: tuple[int, int], point2: tuple[int, int]): Checks if a piece can slide between two points based on neighbor states.
# is_hive_connected(): Checks if the hive remains connected.
# check_hive_connectivity_after_move(move): Verifies hive connectivity after a hypothetical move.
# 3. Ant
# A piece that can move to any reachable position around the hive.
#
# __init__(type: int, position: tuple[int, int], board: Board, value=5): Initializes an Ant piece.
# valid_moves_func(): Finds all valid moves for the Ant, allowing unrestricted sliding around the hive.
# 4. Spider
# A piece that moves exactly three spaces around the hive.
#
# __init__(type: int, position: tuple[int, int], board: Board, value=3): Initializes a Spider piece.
# valid_moves_func(): Returns valid moves, ensuring a maximum of three moves from the current position.
# 5. Hopper
# A piece that jumps in straight lines over other pieces.
#
# __init__(type: int, position: tuple[int, int], board: Board, value=4): Initializes a Hopper piece.
# valid_moves_func(): Finds valid moves by jumping in a straight line over pieces until it encounters an empty spot.
# 6. QueenBee
# The central piece, essential for determining the game state.
#
# __init__(type: int, position: tuple[int, int], board: Board, value=9): Initializes a QueenBee piece.
# valid_moves_func(): Determines valid moves for the Queen Bee by sliding one step in any direction around the hive.
# 7. Beetle
# A piece that can climb over other pieces.
#
# __init__(type: int, position: tuple[int, int], board: Board, value=8): Initializes a Beetle piece.
# valid_moves_func(): Determines valid moves, including the ability to move to occupied spaces by climbing.
#
