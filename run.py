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

# Import `Back_End_Class` from your main logic
from frontend import Back_End_Class
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Back_End_Class()
    MainWindow.show()
    sys.exit(app.exec_())
