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