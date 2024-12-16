import re
from PyQt5.QtGui import QTextCursor
import PyQt5.QtWidgets
from pygame_widget import pygame_widget

import os

from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt
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

    def go_to_page_1(self):
         """Switch to page 1 in the stacked widget."""
         self.stackedWidget.setCurrentIndex(0)  # Assuming page 2 is at index 1

    def go_to_page_2(self):
        """Switch to page 2 in the stacked widget."""
        self.stackedWidget.setCurrentIndex(1)  # Assuming page 2 is at index 1

    def go_to_page_3(self):
        """Switch to page 3 in the stacked widget."""
        self.stackedWidget.setCurrentIndex(2)  # Assuming page 2 is at index 1





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Back_End_Class()
    MainWindow.show()
    sys.exit(app.exec_())
