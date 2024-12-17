from enum import Enum
import copy


class HexMoveCaseEvenEven(Enum):
    TOP = (-1, 0)
    DOWN = (1, 0)
    TOP_RIGHT = (-1, 1)
    TOP_LEFT = (-1, -1)
    LOWER_LEFT = (0, -1)
    LOWER_RIGHT = (0, 1)


class HexMoveCaseOddOdd(Enum):
    TOP = (-1, 0)
    DOWN = (1, 0)
    TOP_RIGHT = (0, 1)
    TOP_LEFT = (0, -1)
    LOWER_LEFT = (1, -1)
    LOWER_RIGHT = (1, 1)


class Board:
    def __init__(self, size: int):
        """
        Initialize the Board object with a 2D list representing the game board.
        
        Args:
            size (int): The size of the board (number of rows and columns).
        
        Attributes:
            board_2d (list): A 2D list of size x size initialized with zeros to represent empty spaces.
            size (int): Size of the board.
            pieces (list): A list to store all pieces placed on the board.
            black_piece (list): A list to store black pieces (-1 or -2).
            white_piece (list): A list to store white pieces (1 or 2).
        """
        self.board_2d = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.pieces = []  # list to store Piece objects
        self.black_piece = []  # list of black pieces
        self.white_piece = []  # list of white pieces

    def check_empty_board(self) -> bool:
        """
        Check if the board is completely empty (all cells contain zero).

        Returns:
            bool: True if all cells are empty, otherwise False.
        """
        return all(all(element == 0 for element in row) for row in self.board_2d)

    def get_piece_at(self, position):
        """
        Retrieve the piece type at a given position on the board.
        
        Args:
            position (tuple[int, int]): Coordinates of the position (x, y).
        
        Returns:
            int: The type of the piece at the position, or 0 if the cell is empty.
        """
        x, y = position
        return self.board_2d[x][y]

    def place_piece(self, piece: 'Piece', position: tuple[int, int]):
        """
        Place a piece on the board at a given position and update its internal state.
        
        Args:
            piece (Piece): The piece object to be placed on the board.
            position (tuple[int, int]): Coordinates where the piece should be placed (x, y).
        """
        x, y = position
        self.board_2d[x][y] = piece.type
        piece.position = position
        self.pieces.append(piece)
        if piece.type == -1 or piece.type == -2:
            self.black_piece.append(piece)

        elif piece.type == 1 or piece.type == 2:
            self.white_piece.append(piece)

    def make_move(self, move):
        """
        Move a piece from a start position to an end position if the move is valid.

        Args:
            move (tuple): A tuple of two positions: start and end.
                          Example: ((start_x, start_y), (end_x, end_y))
        
        Returns:
            Board: The updated board after making the move. If the move is invalid, the board remains unchanged.
        """
        start_pos, end_pos = move
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        type = self.get_piece_at(start_pos)

        if type is None or self.board_2d[end_x][end_y] != 0:
            return self  # Invalid move

        self.board_2d[start_x][start_y] = 0
        self.board_2d[end_x][end_y] = type

        for piece in self.pieces:
            if piece.position == start_pos:
                piece.position = end_pos
                break

        return self

    def find_piece_position(self, type):
        """
        Find the position of a piece based on its type.

        Args:
            type (int): The type of the piece to locate on the board.

        Returns:
            tuple[int, int] or None: The position of the piece if found, otherwise None.
        """        
        for piece in self.pieces:
            if piece.type == type:
                return piece.position
        return None

    def display(self):
        """
        Display the current state of the board in a formatted way.
        - Empty cells are represented by '.'.
        - Other cells display the piece type.
        """
        for row in self.board_2d:
            print(" | ".join(str(cell) if cell else "." for cell in row))
            print("-" * (self.size * 4 - 1))


class Piece:
    def __init__(self, type: int, position: tuple[int, int], insect_type: str, board: Board, player: int = 0,
                 color: tuple[int, int, int] = (0, 0, 0), pos_gui: tuple[int, int] = (0, 0), value=5):
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
        self.player = player
        self.color = color
        self.pos_gui = pos_gui
        

    def check_coordinates(self, x: int, y: int):
        # Check if (x is even and y is even) or (x is odd and y is even)
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 == 0):
            return [(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y - 1)]
        else:
            return [(x + 1, y), (x + 1, y - 1), (x + 1, y + 1), (x, y - 1), (x, y + 1), (x - 1, y)]

    def get_free_region_of_piece(self, piece: 'Piece'):
        x, y = piece.position
        list = piece.check_coordinates(x, y)
        returnList = []
        for i in range(6):
            x, y = list[i]
            if self.board.board_2d[x][y] == 0:
                returnList.append((x, y))

        return returnList

    def get_occupied_region_of_piece(self, piece: 'Piece'):
        x, y = piece.position
        list = piece.check_coordinates(x, y)
        returnList = []
        for i in range(6):
            x, y = list[i]
            if self.board.board_2d[x][y] != 0:
                returnList.append((x, y))

        return returnList

    def around_the_hive(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Determines the intersection of free regions around the hive based on occupied regions.

        Args:
            x (int): The x-coordinate of the piece.
            y (int): The y-coordinate of the piece.

        Returns:
            list[tuple[int, int]]: A list of coordinates representing valid moves around the hive.
        """
        # Get the occupied regions around the given coordinates
        occupied_regions = self.get_occupied_region_of_piece(Piece(self.type, (x, y), self.insect_type, self.board))

        # Get the free regions of the given coordinates
        free_regions = set(self.get_free_region_of_piece(Piece(self.type, (x, y), self.insect_type, self.board)))

        # Calculate the free regions of all occupied neighbors
        free_around_neighbors = set()
        for neighbor_x, neighbor_y in occupied_regions:
            free_around_neighbors.update(
                self.get_free_region_of_piece(Piece(self.type, (neighbor_x, neighbor_y), self.insect_type, self.board)))

        # Return the intersection of the free regions
        return list(free_regions & free_around_neighbors)

    def check_free_to_slide(self, point1: tuple[int, int], point2: tuple[int, int]) -> bool:

        x1, y1 = point1
        x2, y2 = point2

        # Get the surrounding coordinates for both points
        neighbors_point1 = set(self.check_coordinates(x1, y1))
        neighbors_point2 = set(self.check_coordinates(x2, y2))

        # Find the intersection of the neighbors
        intersection = neighbors_point1 & neighbors_point2
        if len(list(intersection)) < 2:
            return True
        x1, y1 = list(intersection)[0]
        x2, y2 = list(intersection)[1]

        # Check if both points on the board are occupied
        if self.board.board_2d[x1][y1] != 0 and self.board.board_2d[x2][y2] != 0:
            return False
        else:
            return True

    def hopper_get_valid_pos_of_direction(self, direction: tuple[int, int], piece_position: tuple[int, int]):
        x, y = piece_position
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 == 0):
            if direction == HexMoveCaseEvenEven.TOP.value:
                x, y = piece_position
                while (self.board.board_2d[x][y] != 0):
                    x = x - 1

                return (x, y)

            elif direction == HexMoveCaseEvenEven.DOWN.value:
                x, y = piece_position
                while (self.board.board_2d[x][y] != 0):
                    x = x + 1

                return (x, y)

            elif direction == HexMoveCaseEvenEven.TOP_LEFT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y - 1
                    if counter % 2 == 0:
                        x = x - 1
                    counter = counter + 1

                return (x, y)

            elif direction == HexMoveCaseEvenEven.TOP_RIGHT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y + 1
                    if counter % 2 == 0:
                        x = x - 1
                    counter = counter + 1

                return (x, y)

            elif direction == HexMoveCaseEvenEven.LOWER_LEFT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y - 1
                    if counter % 2 != 0:
                        x = x + 1
                    counter = counter + 1

                return (x, y)

            elif direction == HexMoveCaseEvenEven.LOWER_RIGHT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y + 1
                    if counter % 2 != 0:
                        x = x + 1
                    counter = counter + 1

                return (x, y)

        else:
            if direction == HexMoveCaseOddOdd.TOP.value:
                x, y = piece_position
                while (self.board.board_2d[x][y] != 0):
                    x = x - 1

                return (x, y)

            elif direction == HexMoveCaseOddOdd.DOWN.value:
                x, y = piece_position
                while (self.board.board_2d[x][y] != 0):
                    x = x + 1

                return (x, y)

            elif direction == HexMoveCaseOddOdd.TOP_LEFT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y - 1
                    if counter % 2 != 0:
                        x = x - 1
                    counter = counter + 1

                return (x, y)

            elif direction == HexMoveCaseOddOdd.TOP_RIGHT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y + 1
                    if counter % 2 != 0:
                        x = x - 1
                    counter = counter + 1
                return (x, y)

            elif direction == HexMoveCaseOddOdd.LOWER_LEFT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y - 1
                    if counter % 2 == 0:
                        x = x + 1
                    counter = counter + 1

                return (x, y)

            elif direction == HexMoveCaseOddOdd.LOWER_RIGHT.value:
                counter = 0
                x, y = piece_position

                while (self.board.board_2d[x][y] != 0):
                    y = y + 1
                    if counter % 2 == 0:
                        x = x + 1
                    counter = counter + 1

                return (x, y)
