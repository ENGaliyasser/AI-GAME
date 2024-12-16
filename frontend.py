import re
from PyQt5.QtGui import QTextCursor
import PyQt5.QtWidgets
from pygame_widget import pygame_widget

import os

from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt
import config  # Import the config file
from config import config  # Import the updated config
class Back_End_Class(QtWidgets.QWidget, Ui_MainWindow):


    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(MainWindow)

        self.pygame_widget_instance = pygame_widget()
        self.thread = {}
        self.start.clicked.connect(self.go_to_page_2)
        self.endbutton.clicked.connect(self.go_to_page_3)

        self.startagain.clicked.connect(self.go_to_page_1)
        self.restart.clicked.connect(self.go_to_page_2)
        # Connect signals to slots
        self.p1.currentTextChanged.connect(self.on_p1_changed)
        self.p2.currentTextChanged.connect(self.on_p2_changed)
        self.d1.currentTextChanged.connect(self.on_d1_changed)
        self.d2.currentTextChanged.connect(self.on_d2_changed)
        # Connect config signals to update methods
        config.blackscore_changed.connect(self.set_black_score)
        config.whitescore_changed.connect(self.set_white_score)
        config.black_won_changed.connect(self.on_black_won)  # Connect to black won signal
        config.white_won_changed.connect(self.on_white_won)

    def go_to_page_1(self):
         """Switch to page 1 in the stacked widget."""
         self.stackedWidget.setCurrentIndex(0)  # Assuming page 2 is at index 1

    def go_to_page_2(self):
        """Switch to page 2 in the stacked widget."""
        self.stackedWidget.setCurrentIndex(1)  # Assuming page 2 is at index 1

    def go_to_page_3(self):
        """Switch to page 3 in the stacked widget."""
        self.stackedWidget.setCurrentIndex(2)  # Assuming page 2 is at index 1

    # Slots to update variables
    def on_p1_changed(self, value):
        config.player1 = value
        print(f"P1 changed to: {config.player1}")

    def on_p2_changed(self, value):
        config.player2 = value
        print(f"P2 changed to: {config.player2}")

    def on_d1_changed(self, value):
        config.diff1 = value
        print(f"D1 changed to: {config.diff1}")

    def on_d2_changed(self, value):
        config.diff2 = value
        print(f"D2 changed to: {config.diff2}")

    def set_white_score(self, value):
        """Set the value for the white score label."""
        self.w1.setText(f"{value}")
        self.w2.setText(f"{value}")

    def set_black_score(self, value):
        """Set the value for the black score label."""
        self.b1.setText(f"{value}")
        self.b2.setText(f"{value}")

    def on_black_won(self, value):
        """Handle when black wins."""
        if value:  # If black won
            self.stackedWidget.setCurrentIndex(2)  # Go to page 3
            self.winner_label.setText("Winner: Black")  # Update the winner label
            print("Black has won!")

    def on_white_won(self, value):
        """Handle when white wins."""
        if value:  # If white won
            self.stackedWidget.setCurrentIndex(2)  # Go to page 3
            self.winner_label.setText("Winner: White")  # Update the winner label
            print("White has won!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Back_End_Class()
    MainWindow.show()
    sys.exit(app.exec_())
