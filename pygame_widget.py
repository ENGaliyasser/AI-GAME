import pygame
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow , QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QImage
import math
from piecesboard import Board, Piece  # Importing the logic from the provided file

class pygame_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.Surface((900, 800))  # Offscreen surface for rendering

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
            Piece(type=-1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=1, color=(139, 69, 19), pos_gui=(750, 50)),
            Piece(type=-1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=1, color=(139, 69, 19), pos_gui=(800, 50)),
            Piece(type=-1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=1, color=(139, 69, 19), pos_gui=(850, 50)),
            Piece(type=-1, position=(-1, -1), insect_type="Beetle", board=self.board_logic, player=1, color=(0, 0, 255), pos_gui=(750, 100)),
            Piece(type=-1, position=(-1, -1), insect_type="Beetle", board=self.board_logic, player=1, color=(0, 0, 255), pos_gui=(800, 100)),
            Piece(type=-1, position=(-1, -1), insect_type="Hopper", board=self.board_logic, player=1, color=(0, 255, 0), pos_gui=(750, 150)),
            Piece(type=-1, position=(-1, -1), insect_type="Hopper", board=self.board_logic, player=1, color=(0, 255, 0), pos_gui=(800, 150)),
            Piece(type=-1, position=(-1, -1), insect_type="Hopper", board=self.board_logic, player=1, color=(0, 255, 0), pos_gui=(850, 150)),
            Piece(type=-2, position=(-1, -1), insect_type="Qbee", board=self.board_logic, player=1, color=(255, 255, 0), pos_gui=(750, 200)),
            Piece(type=-1, position=(-1, -1), insect_type="Spider", board=self.board_logic, player=1, color=(255, 0, 0), pos_gui=(750, 250)),
            Piece(type=-1, position=(-1, -1), insect_type="Spider", board=self.board_logic, player=1, color=(255, 0, 0), pos_gui=(800, 250)),
            Piece(type=1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=2, color=(139, 69, 19), pos_gui=(750, 450)),
            Piece(type=1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=2, color=(139, 69, 19), pos_gui=(800, 450)),
            Piece(type=1, position=(-1, -1), insect_type="Ant", board=self.board_logic, player=2, color=(139, 69, 19), pos_gui=(850, 450)),
            Piece(type=1, position=(-1, -1), insect_type="Beetle", board=self.board_logic, player=2, color=(0, 0, 255), pos_gui=(750, 500)),
            Piece(type=1, position=(-1, -1), insect_type="Beetle", board=self.board_logic, player=2, color=(0, 0, 255), pos_gui=(800, 500)),
            Piece(type=1, position=(-1, -1), insect_type="Hopper", board=self.board_logic, player=2, color=(0, 255, 0), pos_gui=(750, 550)),
            Piece(type=1, position=(-1, -1), insect_type="Hopper", board=self.board_logic, player=2, color=(0, 255, 0), pos_gui=(800, 550)),
            Piece(type=1, position=(-1, -1), insect_type="Hopper", board=self.board_logic, player=2, color=(0, 255, 0), pos_gui=(850, 550)),
            Piece(type=2, position=(-1, -1), insect_type="Qbee", board=self.board_logic, player=2, color=(255, 255, 0), pos_gui=(750, 600)),
            Piece(type=1, position=(-1, -1), insect_type="Spider", board=self.board_logic, player=2, color=(255, 0, 0), pos_gui=(750, 650)),
            Piece(type=1, position=(-1, -1), insect_type="Spider", board=self.board_logic, player=2, color=(255, 0, 0), pos_gui=(800, 650)),
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
        self.timer.start(16)  # ~60 FPS

        # Set the size of the QWidget
        self.setFixedSize(900, 800)
        # Button to centralize pieces
        self.centralize_button = QPushButton("Centralize Pieces", self)
        # self.centralize_button.clicked.connect(self.centralize_pieces)
        self.centralize_button.move(10, 10)

    def grid_to_pixel(self, row, col):
        """Convert grid (row, col) to pixel (x, y)."""
        x = self.hex_radius * 1.5 * col + self.x_offset
        y = self.hex_radius * math.sqrt(3) * (row + 0.5 * (col % 2)) + self.y_offset
        return x, y

    def pixel_to_grid(self, x, y):
        """Convert pixel (x, y) to grid (row, col) with precise hex boundary alignment."""
        # Calculate axial coordinates (q, r) in the hex grid
        q = (x - self.x_offset) / (self.hex_radius * 1.5)
        r = (y - self.y_offset) / (self.hex_radius * math.sqrt(3)) - 0.5 * (int(q) % 2)

        # Calculate the cube coordinates for the hex (needed for proper snapping)
        cube_x = q
        cube_z = r
        cube_y = -cube_x - cube_z

        # Round to nearest hex grid position
        rx = round(cube_x)
        ry = round(cube_y)
        rz = round(cube_z)

        # Fix rounding errors by ensuring x + y + z = 0
        x_diff = abs(rx - cube_x)
        y_diff = abs(ry - cube_y)
        z_diff = abs(rz - cube_z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        # Convert cube coordinates back to grid row/col
        col = rx
        row = rz

        return row, col

    # ------------------------------- Hex Grid Creation -------------------------------

    def create_hex_grid(self, rows, cols):
        """Create a hexagonal grid of given dimensions."""
        hex_grid = []
        for row in range(rows):
            row_list = []
            for col in range(cols):
                x = self.hex_radius * 3 / 2 * col
                y = self.hex_radius * (3 ** 0.5) * (row + 0.5 * (col % 2))
                row_list.append((x + 60, y + 80))  # Offset for center alignment
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
                    2,  # Border width
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

    def mousePressEvent(self, event):
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
        else:
            # Invalid move, return piece to its start position
            self.selected_piece.pos_gui = self.start_gui_position
            self.selected_piece.position = self.start_grid_position
            print(f"Invalid move. Returning piece to {self.start_gui_position}")

        self.selected_piece = None  # Deselect the piece

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
