import copy

import pygame
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow , QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QImage
import math
from piecesboard import Board, Piece  # Importing the logic from the provided file
import ai
import config
from config import config

def update_scores(black, white):
    """Update the black and white scores."""
    config.blackscore = black  # This will trigger the blackscore_changed signal
    config.whitescore = white  # This will trigger the whitescore_changed signal

def set_black_won():
    """Set the black player as the winner and emit the signal."""
    config.black_won = True  # This triggers the signal for black winning
    print("Black has won!")

def set_white_won():
    """Set the white player as the winner and emit the signal."""
    config.white_won = True  # This triggers the signal for white winning
    print("White has won!")

class pygame_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize Pygame
        pygame.init()
        # self.screen = pygame.Surface((900, 800))  # Offscreen surface for rendering
        self.display = pygame.display.set_mode((900, 800))  # Main Pygame window
        self.screen = pygame.Surface((900, 800))  # Offscreen surface for rendering
        pygame.display.set_caption("Hive AI Game")
        # Game variables
        self.hex_radius = 25* math.sqrt(3)
        self.grid_rows = 10
        self.grid_cols = 9
        self.x_offset = 60  # Starting x offset for the grid
        self.y_offset = 80  # Starting y offset for the grid
        self.board = self.create_hex_grid(self.grid_rows, self.grid_cols)  # 10x10 hex grid
        self.board_logic = Board(50)  # Use the imported Board class
        self.piece_counts = {
            1: {"Ant": 3, "Beetle": 3, "Hopper": 3, "Qbee": 1, "Spider": 2},
            2: {"Ant": 3, "Beetle": 3, "Hopper": 3, "Qbee": 1, "Spider": 2},
        }
        # Initialize game pieces

        # Initialize game pieces as instances of the Piece class
        self.pieces = [
            Piece(type=-1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=1, color=(139, 69, 19), pos_gui=(750, 50),value= 10),
            Piece(type=-1, position=(-2, -2), insect_type="Ant", board=self.board_logic, player=1, color=(139, 69, 19), pos_gui=(800, 50),value= 10),
            Piece(type=-1, position=(-3, -3), insect_type="Ant", board=self.board_logic, player=1, color=(139, 69, 19), pos_gui=(850, 50),value= 10),
            Piece(type=-1, position=(-4, -4), insect_type="Beetle", board=self.board_logic, player=1, color=(0, 0, 255), pos_gui=(750, 100),value= 15),
            Piece(type=-1, position=(-5, -5), insect_type="Beetle", board=self.board_logic, player=1, color=(0, 0, 255), pos_gui=(800, 100),value= 15),
            Piece(type=-1, position=(-6, -6), insect_type="Hopper", board=self.board_logic, player=1, color=(0, 255, 0), pos_gui=(750, 150),value= 20),
            Piece(type=-1, position=(-7, -7), insect_type="Hopper", board=self.board_logic, player=1, color=(0, 255, 0), pos_gui=(800, 150),value= 20),
            Piece(type=-1, position=(-8, -8), insect_type="Hopper", board=self.board_logic, player=1, color=(0, 255, 0), pos_gui=(850, 150),value= 20),
            Piece(type=-2, position=(-9, -9), insect_type="Qbee", board=self.board_logic, player=1, color=(255, 255, 0), pos_gui=(750, 200),value= 5),
            Piece(type=-1, position=(-10, -10), insect_type="Spider", board=self.board_logic, player=1, color=(255, 0, 0), pos_gui=(750, 250),value= 5),
            Piece(type=-1, position=(-11, -11), insect_type="Spider", board=self.board_logic, player=1, color=(255, 0, 0), pos_gui=(800, 250),value= 5),
            Piece(type=1, position=(-12, -12), insect_type="Ant", board=self.board_logic, player=2, color=(139, 69, 19), pos_gui=(750, 450),value= 5),
            Piece(type=1, position=(-13, -13), insect_type="Ant", board=self.board_logic, player=2, color=(139, 69, 19), pos_gui=(800, 450),value= 5),
            Piece(type=1, position=(-14, -14), insect_type="Ant", board=self.board_logic, player=2, color=(139, 69, 19), pos_gui=(850, 450),value= 5),
            Piece(type=1, position=(-15, -15), insect_type="Beetle", board=self.board_logic, player=2, color=(0, 0, 255), pos_gui=(750, 500),value= 5),
            Piece(type=1, position=(-16, -16), insect_type="Beetle", board=self.board_logic, player=2, color=(0, 0, 255), pos_gui=(800, 500),value= 5),
            Piece(type=1, position=(-17, -17), insect_type="Hopper", board=self.board_logic, player=2, color=(0, 255, 0), pos_gui=(750, 550),value= 5),
            Piece(type=1, position=(-18, -18), insect_type="Hopper", board=self.board_logic, player=2, color=(0, 255, 0), pos_gui=(800, 550),value= 5),
            Piece(type=1, position=(-19, -19), insect_type="Hopper", board=self.board_logic, player=2, color=(0, 255, 0), pos_gui=(850, 550),value= 5),
            Piece(type=2, position=(-20, -20), insect_type="Qbee", board=self.board_logic, player=2, color=(255, 255, 0), pos_gui=(750, 600),value= 5),
            Piece(type=1, position=(-21, -21), insect_type="Spider", board=self.board_logic, player=2, color=(255, 0, 0), pos_gui=(750, 650),value= 5),
            Piece(type=1, position=(-22, -22), insect_type="Spider", board=self.board_logic, player=2, color=(255, 0, 0), pos_gui=(800, 650),value= 5),
            # Add other pieces similarly...
        ]

        # Board pieces
        self.board_pieces = []
        self.valid_moves = []
        # Currently selected piece and its offset
        self.selected_piece = None
        self.drag_offset = (0, 0)

        # Track if the first move has been made
        self.first_move = True

        # Pygame loop timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_pygame)
        self.timer.start(150)  # ~60 FPS

        # Set the size of the QWidget
        self.setFixedSize(900, 800)
        # Button to centralize pieces
        self.centralize_button = QPushButton("Centralize Pieces", self)
        # self.centralize_button.clicked.connect(self.centralize_pieces)
        self.centralize_button.move(10, 10)
        self.turn = 1

    def custom_copy(self):
        # Create a new instance of the class
        new_instance = pygame_widget()

        # Deep copy the board logic
        if self.board_logic:
            new_instance.board_logic = copy.deepcopy(self.board_logic)

        # Deep copy the pieces
        new_instance.pieces = copy.deepcopy(self.pieces)

        return new_instance

    def grid_to_pixel(self, row, col):
        """Convert grid (row, col) to pixel (x, y)."""
        x = self.hex_radius * 1.5 * col + self.x_offset
        y = self.hex_radius * math.sqrt(3) * (row + 0.5 * (col % 2)) + self.y_offset
        return x, y

    def pixel_to_grid(self, x, y):
        """Convert pixel (x, y) to grid (row, col) using precomputed centers."""
        closest_hex = None
        min_distance = float('inf')

        # Iterate through all hexagon centers
        for (row, col), center in self.hex_centers.items():
            # Calculate Euclidean distance to the center
            distance = ((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_hex = (row, col)

        return closest_hex

    # ------------------------------- Hex Grid Creation -------------------------------

    def create_hex_grid(self, rows, cols):
        """Create a hexagonal grid of given dimensions and save centers."""
        self.hex_centers = {}  # Dictionary to store hexagon centers by (row, col)
        hex_grid = []

        for row in range(rows):
            row_list = []
            for col in range(cols):
                # Calculate the center of the hexagon
                x = self.hex_radius * 3 / 2 * col
                y = self.hex_radius * (3 ** 0.5) * (row + 0.5 * (col % 2))
                center = (x + 60, y + 80)  # Offset for center alignment

                # Save center in the dictionary
                self.hex_centers[(row, col)] = center
                row_list.append(center)

            hex_grid.append(row_list)

        return hex_grid

    # ------------------------------- Pygame Drawing Functions -------------------------------

    def draw_hex_grid(self):
        """Draw the hexagonal grid."""
        for row in self.board:
            for center in row:
                pygame.draw.polygon(
                    self.screen,
                    (200, 200, 200),  # Gray color for grid lines
                    [self.hex_corner(center, i) for i in range(6)],
                    5,  # Border width
                )

        # Highlight valid moves
        for move in self.valid_moves:
            highlight_center = self.grid_to_pixel(*move)
            pygame.draw.polygon(
                self.screen,
                (0, 255, 0),  # Green highlight for valid moves
                [self.hex_corner(highlight_center, i) for i in range(6)],
                0,  # Fill the hexagon
            )

    def hex_corner(self, center, i):
        """Calculate the corner of a hexagon."""
        angle = 2 * math.pi / 6 * i  # Angle for each corner
        x = center[0] + self.hex_radius * math.cos(angle)
        y = center[1] + self.hex_radius * math.sin(angle)
        return x, y

    def draw_pieces(self):
        """Draw the game pieces for both players."""
        for piece in self.pieces:
            pygame.draw.polygon(
                self.screen,
                piece.color,
                [self.hex_corner(piece.pos_gui, i) for i in range(6)],
            )

            # Draw border around the piece
            border_color = (0, 0, 0) if piece.player == 1 else (255, 255, 255)
            pygame.draw.polygon(
                self.screen,
                border_color,
                [self.hex_corner(piece.pos_gui, i) for i in range(6)],
                2,  # Border width
            )

            # Draw the piece type (e.g., "Ant", "Beetle") on the piece
            font = pygame.font.SysFont(None, 24)
            text = font.render(piece.insect_type, True, (0, 0, 0))
            self.screen.blit(text, (piece.pos_gui[0] - 20, piece.pos_gui[1] - 10))

    # ----------------------------- Pygame Event Handling -----------------------------

    def run_pygame(self):
        """Run the Pygame game loop."""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Pygame Mouse clicked at {event.pos}")

        # Clear screen and redraw everything
        self.screen.fill((240, 240, 240))
        self.draw_hex_grid()
        self.draw_pieces()

        # Repaint QWidget
        self.update()

    def paintEvent(self, event):
        """Override the QWidget's paintEvent to draw the Pygame screen."""
        painter = QPainter(self)
        surface = pygame.image.tostring(self.screen, 'RGB')
        img = QImage(surface, self.screen.get_width(), self.screen.get_height(), QImage.Format_RGB888)
        painter.drawImage(0, 0, img)

    # ----------------------------- Mouse Event Handling -----------------------------

    def is_odd(number):
        return number % 2 != 0

    def mousePressEvent(self, event):
        if (config.player1 == "Human") and (config.player2 == "Human"):
            if self.turn % 2 != 0:
                if self.turn == 7:
                    for piece in self.pieces:
                        pos = (event.x(), event.y())
                        row, col = self.pixel_to_grid(*pos)  # Unpack the tuple `pos` into x and y
                        print(f"Mouse pressed at pixel: {pos}, grid: ({row}, {col})")
                        if piece.type in [ 2]:
                            if self.is_point_in_hex(pos, piece.pos_gui):
                                self.selected_piece = piece
                                self.drag_offset = (pos[0] - piece.pos_gui[0], pos[1] - piece.pos_gui[1])
                                self.start_gui_position = piece.pos_gui  # Save the starting GUI position
                                self.start_grid_position = piece.position  # Save the starting grid position
                                print(f"Selected piece: {piece.insect_type} at {piece.pos_gui}")

                                # Get valid moves for the selected piece
                                self.valid_moves = self.selected_piece.valid_moves_func()
                                print(f"Valid moves: {self.valid_moves}")
                                return
                else:
                    """Handle mouse press events to select a piece."""
                    pos = (event.x(), event.y())
                    row, col = self.pixel_to_grid(*pos)  # Unpack the tuple `pos` into x and y
                    print(f"Mouse pressed at pixel: {pos}, grid: ({row}, {col})")
                    for piece in self.pieces:
                        if piece.type in [1 ,2]:
                            if self.is_point_in_hex(pos, piece.pos_gui):
                                self.selected_piece = piece
                                self.drag_offset = (pos[0] - piece.pos_gui[0], pos[1] - piece.pos_gui[1])
                                self.start_gui_position = piece.pos_gui  # Save the starting GUI position
                                self.start_grid_position = piece.position  # Save the starting grid position
                                print(f"Selected piece: {piece.insect_type} at {piece.pos_gui}")

                                # Get valid moves for the selected piece
                                self.valid_moves = self.selected_piece.valid_moves_func()
                                print(f"Valid moves: {self.valid_moves}")
                                return
            else:
                if self.turn == 8:
                    """Handle mouse press events to select a piece."""
                    pos = (event.x(), event.y())
                    row, col = self.pixel_to_grid(*pos)  # Unpack the tuple `pos` into x and y
                    print(f"Mouse pressed at pixel: {pos}, grid: ({row}, {col})")
                    for piece in self.pieces:
                        if piece.type in [-2]:
                            if self.is_point_in_hex(pos, piece.pos_gui):
                                self.selected_piece = piece
                                self.drag_offset = (pos[0] - piece.pos_gui[0], pos[1] - piece.pos_gui[1])
                                self.start_gui_position = piece.pos_gui  # Save the starting GUI position
                                self.start_grid_position = piece.position  # Save the starting grid position
                                print(f"Selected piece: {piece.insect_type} at {piece.pos_gui}")

                                # Get valid moves for the selected piece
                                self.valid_moves = self.selected_piece.valid_moves_func()
                                print(f"Valid moves: {self.valid_moves}")
                                return
                else:
                    """Handle mouse press events to select a piece."""
                    pos = (event.x(), event.y())
                    row, col = self.pixel_to_grid(*pos)  # Unpack the tuple `pos` into x and y
                    print(f"Mouse pressed at pixel: {pos}, grid: ({row}, {col})")
                    for piece in self.pieces:
                        if piece.type in [-1, -2]:
                            if self.is_point_in_hex(pos, piece.pos_gui):
                                self.selected_piece = piece
                                self.drag_offset = (pos[0] - piece.pos_gui[0], pos[1] - piece.pos_gui[1])
                                self.start_gui_position = piece.pos_gui  # Save the starting GUI position
                                self.start_grid_position = piece.position  # Save the starting grid position
                                print(f"Selected piece: {piece.insect_type} at {piece.pos_gui}")

                                # Get valid moves for the selected piece
                                self.valid_moves = self.selected_piece.valid_moves_func()
                                print(f"Valid moves: {self.valid_moves}")
                                return

        else:
            """Handle mouse press events to select a piece."""
            pos = (event.x(), event.y())
            row, col = self.pixel_to_grid(*pos)  # Unpack the tuple `pos` into x and y
            print(f"Mouse pressed at pixel: {pos}, grid: ({row}, {col})")
            for piece in self.pieces:
                if self.is_point_in_hex(pos, piece.pos_gui):
                    self.selected_piece = piece
                    self.drag_offset = (pos[0] - piece.pos_gui[0], pos[1] - piece.pos_gui[1])
                    self.start_gui_position = piece.pos_gui  # Save the starting GUI position
                    self.start_grid_position = piece.position  # Save the starting grid position
                    print(f"Selected piece: {piece.insect_type} at {piece.pos_gui}")

                    # Get valid moves for the selected piece
                    self.valid_moves = self.selected_piece.valid_moves_func()
                    print(f"Valid moves: {self.valid_moves}")
                    return


    def mouseMoveEvent(self, event):
        """Handle mouse move events to drag the selected piece."""
        if self.selected_piece:
            pos = (event.x(), event.y())
            # Update GUI position for dragging
            self.selected_piece.pos_gui = (pos[0] - self.drag_offset[0], pos[1] - self.drag_offset[1])

    def mouseReleaseEvent(self, event):
        """Handle mouse release events to place a piece."""
        if not self.selected_piece:
            return

        pos = (event.x(), event.y())
        row, col = self.pixel_to_grid(*pos)

        # Validate if the release is within valid moves
        if (row, col) in self.valid_moves:
            self.selected_piece.position = (row, col)  # Update grid position
            self.selected_piece.pos_gui = self.grid_to_pixel(row, col)  # Update GUI position
            print(f"Piece placed at grid: ({row}, {col})")
            self.board_logic.place_piece(self.selected_piece, (row, col))  # Update board logic
            self.board_logic.display()
            #print(f"This board: {self.board_logic.board_2d} ")
            for piece in self.pieces:
                piece.board = self.board_logic
            #self.selected_piece.board = self.board_logic
            self.turn = self.turn + 1
            if (config.player1 == "Human") and (config.player2 == "Human"):
                a = ai.game_over(self)
                if a == 1:
                    self.set_white_won()
                elif a == 2:
                    self.set_black_won()
            elif (config.player1 == "Human") and (config.player2 == "Computer"):
                QTimer.singleShot(30, self.execute_ai_move)
        else:
            # Invalid move, return piece to its start position
            self.selected_piece.pos_gui = self.start_gui_position
            self.selected_piece.position = self.start_grid_position
            print(f"Invalid move. Returning piece to {self.start_gui_position}")


        self.selected_piece = None  # Deselect the piece









    def execute_ai_move(self):
        """Execute AI's move after player's turn."""
        if (config.player1 == "Human") and (config.player2 == "Computer"):
            no = -1
        elif (config.player1 == "Computer") and (config.player2 == "Human"):
            no = 1
        best_move = ai.find_best_move_with_iterative_deepening(self, no, 2, 100)
        print(f"AI Move: {best_move}")

        if not best_move:
            print("No valid AI move found. Skipping AI turn.")
            return

        start_pos, end_pos = best_move
        ai_piece = self.find_piece_by_position(self, start_pos)

        if ai_piece is None:
            print(f"Error: No piece found at {start_pos}. AI move is invalid.")
            return

        row1, col1 = end_pos
        ai_piece.position = (row1, col1)  # Update grid position
        ai_piece.pos_gui = self.grid_to_pixel(row1, col1)  # Update GUI position
        print(f"AI Piece placed at grid: ({row1}, {col1})")

        # Update board logic
        self.board_logic.place_piece(ai_piece, (row1, col1))
        self.board_logic.display()

        # Debug: Ensure piece positions are consistent
        print(f"Updated AI piece positions: {[piece.position for piece in self.pieces]}")

        self.refresh_game_display()


        # for piece in self.pieces:
        #     piece.board = self.board_logic

    def refresh_game_display(self):
        """Refresh the game display to reflect the latest game state."""
        # Clear the screen
        self.screen.fill((240, 240, 240))

        # Redraw the hexagonal grid and all pieces
        self.draw_hex_grid()
        self.draw_pieces()

        # Update the Pygame display
        pygame.display.flip()

        # Repaint PyQt widget if integrated
        self.update()

    def find_piece_by_position(self, board, position):
        """Find the piece object at the given position."""
        for piece in board.pieces:  # Access pieces directly from the board
            if piece.position == position:
                return piece
        return None

    def is_point_in_hex(self, point, center):
        """Check if a point is inside a hexagon."""
        px, py = point
        cx, cy = center
        dx, dy = abs(px - cx), abs(py - cy)
        return dx <= self.hex_radius * 1.5 and dy <= self.hex_radius * (3 ** 0.5) / 2




# Main application code
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        # Add Pygame widget to the layout
        pygame_display = pygame_widget()
        layout.addWidget(pygame_display)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("Pygame Embedded in PyQt Layout")
        self.resize(900, 800)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
