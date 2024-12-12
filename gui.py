# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 524)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setStyleSheet("/* General Background */\n"
"QWidget {\n"
"    background-color: #2c3e50; /* Dark slate blue background */\n"
"    font-family: Arial, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"/* Title Label */\n"
"QLabel {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #f1c40f; /* Golden yellow for the title */\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Drop-down Menus */\n"
"QComboBox {\n"
"    background-color: #34495e; /* Dark grayish blue background */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #f1c40f; /* Golden yellow border on hover */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    background-color: #2c3e50; /* Same dark background */\n"
"    border: none;\n"
"}\n"
"\n"
"/* Text Fields */\n"
"QLineEdit {\n"
"    background-color: #34495e; /* Dark grayish blue background */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #f1c40f; /* Golden yellow border on focus */\n"
"    outline: none;\n"
"}\n"
"\n"
"/* Buttons */\n"
"QPushButton {\n"
"    background-color: #1abc9c; /* Teal button */\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    text-transform: uppercase;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #16a085; /* Darker teal on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #0e6655; /* Even darker teal on press */\n"
"}\n"
"\n"
"/* Optional: Tooltips */\n"
"QToolTip {\n"
"    background-color: #34495e; /* Dark grayish blue background */\n"
"    color: #ecf0f1; /* Light text */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"")
        self.page.setObjectName("page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.page)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 1, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.page)
        self.label_18.setMinimumSize(QtCore.QSize(0, 0))
        self.label_18.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 1, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.page)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_2, 1, 3, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.page)
        self.label_21.setMinimumSize(QtCore.QSize(0, 0))
        self.label_21.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_21.setObjectName("label_21")
        self.gridLayout_2.addWidget(self.label_21, 3, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.page)
        self.label_16.setMinimumSize(QtCore.QSize(0, 0))
        self.label_16.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 4, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.page)
        self.label_19.setMinimumSize(QtCore.QSize(0, 0))
        self.label_19.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_19.setObjectName("label_19")
        self.gridLayout_2.addWidget(self.label_19, 1, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.page)
        self.label_17.setMinimumSize(QtCore.QSize(0, 0))
        self.label_17.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 4, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.page)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 4, 1, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.page)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_3, 3, 3, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 4, 3, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.page)
        self.label_20.setMinimumSize(QtCore.QSize(0, 0))
        self.label_20.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_20.setObjectName("label_20")
        self.gridLayout_2.addWidget(self.label_20, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.page)
        self.label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(-1)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)
        self.comboBox_4 = QtWidgets.QComboBox(self.page)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_4, 3, 1, 1, 1)
        self.start = QtWidgets.QPushButton(self.page)
        self.start.setObjectName("start")
        self.gridLayout_2.addWidget(self.start, 5, 0, 1, 4)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setStyleSheet("/* General Background */\n"
"QWidget {\n"
"    background-color: #2c3e50; /* Dark slate blue background */\n"
"    font-family: Arial, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"/* Title Label */\n"
"QLabel {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #f1c40f; /* Golden yellow for the title */\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Drop-down Menus */\n"
"QComboBox {\n"
"    background-color: #34495e; /* Dark grayish blue background */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #f1c40f; /* Golden yellow border on hover */\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    background-color: #2c3e50; /* Same dark background */\n"
"    border: none;\n"
"}\n"
"\n"
"/* Text Fields */\n"
"QLineEdit {\n"
"    background-color: #34495e; /* Dark grayish blue background */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #f1c40f; /* Golden yellow border on focus */\n"
"    outline: none;\n"
"}\n"
"\n"
"/* Buttons */\n"
"QPushButton {\n"
"    background-color: #1abc9c; /* Teal button */\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    text-transform: uppercase;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #16a085; /* Darker teal on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #0e6655; /* Even darker teal on press */\n"
"}\n"
"\n"
"/* Optional: Tooltips */\n"
"QToolTip {\n"
"    background-color: #34495e; /* Dark grayish blue background */\n"
"    color: #ecf0f1; /* Light text */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"")
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget = pygame_widget(self.page_2)
        self.widget.setStyleSheet("/* General Background */\n"
"QWidget {\n"
"    background-color: #2c3e50; /* Dark slate blue background */\n"
"    font-family: Arial, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}")
        self.widget.setObjectName("widget")
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)
        self.endbutton = QtWidgets.QPushButton(self.page_2)
        self.endbutton.setObjectName("endbutton")
        self.gridLayout_3.addWidget(self.endbutton, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setStyleSheet("/* General Background */\n"
"#page_3 {\n"
"    background-color: #2c3e50; /* Dark slate blue background */\n"
"    font-family: Arial, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #ecf0f1; /* Light text color */\n"
"}\n"
"\n"
"/* Title Label: \"THE END\" */\n"
"#end {\n"
"    font-size: 36px;\n"
"    font-weight: bold;\n"
"    color: #e74c3c; /* Bright red for emphasis */\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Labels for Score and Winner */\n"
"#score {\n"
"    font-size: 28px; /* Larger text size */\n"
"    font-weight: bold; /* Bolder appearance */\n"
"    color: #ecf0f1; /* Light text color */\n"
"    text-align: center;\n"
"}\n"
"#score_2 {\n"
"    font-size: 28px; /* Larger text size */\n"
"    font-weight: bold; /* Bolder appearance */\n"
"    color: #ecf0f1; /* Light text color */\n"
"    text-align: center;\n"
"}\n"
"#winner {\n"
"    font-size: 32px; /* Larger text size */\n"
"    font-weight: bold; /* Bolder appearance */\n"
"    color: #2ecc71; /* Greenish color */\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Score Numbers */\n"
"#scorenumbers {\n"
"    font-size: 50px;\n"
"    font-weight: bold;\n"
"    color:#2ecc71; /* green for the score */\n"
"    text-align: center;\n"
"}\n"
"#scorenumbers_2 {\n"
"    font-size: 50px;\n"
"    font-weight: bold;\n"
"    color: #e74c3c; /* red for the score */\n"
"    text-align: center;\n"
"}\n"
"/* Buttons */\n"
"#restart, #startagain {\n"
"    background-color: #1abc9c; /* Teal button background */\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    text-transform: uppercase;\n"
"}\n"
"\n"
"#restart:hover, #startagain:hover {\n"
"    background-color: #16a085; /* Darker teal on hover */\n"
"}\n"
"\n"
"#restart:pressed, #startagain:pressed {\n"
"    background-color: #0e6655; /* Even darker teal on press */\n"
"}\n"
"\n"
"/* Status Bar */\n"
"QStatusBar {\n"
"    background-color: #34495e; /* Slightly darker than main background */\n"
"    color: #ecf0f1; /* Light text */\n"
"    border: 1px solid #7f8c8d; /* Soft gray border */\n"
"    padding: 2px;\n"
"}\n"
"")
        self.page_3.setObjectName("page_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.end = QtWidgets.QLabel(self.page_3)
        self.end.setAlignment(QtCore.Qt.AlignCenter)
        self.end.setObjectName("end")
        self.gridLayout_4.addWidget(self.end, 0, 0, 1, 2)
        self.score_2 = QtWidgets.QLabel(self.page_3)
        self.score_2.setAlignment(QtCore.Qt.AlignCenter)
        self.score_2.setObjectName("score_2")
        self.gridLayout_4.addWidget(self.score_2, 5, 0, 1, 1)
        self.scorenumbers_2 = QtWidgets.QLabel(self.page_3)
        self.scorenumbers_2.setAlignment(QtCore.Qt.AlignCenter)
        self.scorenumbers_2.setObjectName("scorenumbers_2")
        self.gridLayout_4.addWidget(self.scorenumbers_2, 5, 1, 1, 1)
        self.winner = QtWidgets.QLabel(self.page_3)
        self.winner.setAlignment(QtCore.Qt.AlignCenter)
        self.winner.setObjectName("winner")
        self.gridLayout_4.addWidget(self.winner, 8, 0, 2, 2)
        self.startagain = QtWidgets.QPushButton(self.page_3)
        self.startagain.setObjectName("startagain")
        self.gridLayout_4.addWidget(self.startagain, 12, 1, 1, 1)
        self.restart = QtWidgets.QPushButton(self.page_3)
        self.restart.setObjectName("restart")
        self.gridLayout_4.addWidget(self.restart, 12, 0, 1, 1)
        self.score = QtWidgets.QLabel(self.page_3)
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.score.setObjectName("score")
        self.gridLayout_4.addWidget(self.score, 4, 0, 1, 1)
        self.scorenumbers = QtWidgets.QLabel(self.page_3)
        self.scorenumbers.setAlignment(QtCore.Qt.AlignCenter)
        self.scorenumbers.setObjectName("scorenumbers")
        self.gridLayout_4.addWidget(self.scorenumbers, 4, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_3)
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AI Hive Game"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Choose"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Human"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Computer"))
        self.label_18.setText(_translate("MainWindow", "Player 1 Mode"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Choose"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Human"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Computer"))
        self.label_21.setText(_translate("MainWindow", "Difficulty"))
        self.label_16.setText(_translate("MainWindow", "Player 1 Name "))
        self.label_19.setText(_translate("MainWindow", "Player 2 Mode"))
        self.label_17.setText(_translate("MainWindow", "Player 2 Name "))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Choose"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Human"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "Computer"))
        self.label_20.setText(_translate("MainWindow", "Difficulty"))
        self.label.setText(_translate("MainWindow", "AI HIVE GAME"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "Choose"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "Human"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "Computer"))
        self.start.setText(_translate("MainWindow", "START"))
        self.endbutton.setText(_translate("MainWindow", "END"))
        self.end.setText(_translate("MainWindow", "THE END"))
        self.score_2.setText(_translate("MainWindow", "Player 2 Score:"))
        self.scorenumbers_2.setText(_translate("MainWindow", "560"))
        self.winner.setText(_translate("MainWindow", "Player 1 WON"))
        self.startagain.setText(_translate("MainWindow", "Start Again"))
        self.restart.setText(_translate("MainWindow", "Restart"))
        self.score.setText(_translate("MainWindow", "Player 1 Score:"))
        self.scorenumbers.setText(_translate("MainWindow", "560"))
from pygame_widget import pygame_widget
