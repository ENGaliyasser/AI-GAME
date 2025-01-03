# config.py
player1 = "Human"  # Default value
player2 = "Human"
diff1 = "Easy"
diff2 = "Easy"
from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtCore import QObject, pyqtSignal

class Config(QObject):
    # Define signals for when variables change
    blackscore_changed = pyqtSignal(int)
    whitescore_changed = pyqtSignal(int)
    black_won_changed = pyqtSignal(bool)  # Signal emitted when black_won changes
    white_won_changed = pyqtSignal(bool)  # Signal emitted when white_won changes
    turn_changed = pyqtSignal(int)  # Signal emitted when the turn changes

    def __init__(self):
        super().__init__()
        self._blackscore = 0
        self._whitescore = 0
        self._black_won = False
        self._white_won = False
        self._turn = 0 # Default turn
        self.player1 = "Human"  # Default value
        self.player2 = "Human"
        self.diff1 = "Easy"
        self.diff2 = "Easy"

    # Property for blackscore
    @property
    def blackscore(self):
        return self._blackscore

    @blackscore.setter
    def blackscore(self, value):
        if self._blackscore != value:
            self._blackscore = value
            self.blackscore_changed.emit(value)

    # Property for whitescore
    @property
    def whitescore(self):
        return self._whitescore

    @whitescore.setter
    def whitescore(self, value):
        if self._whitescore != value:
            self._whitescore = value
            self.whitescore_changed.emit(value)

    # Property for black_won
    @property
    def black_won(self):
        return self._black_won

    @black_won.setter
    def black_won(self, value):
        if self._black_won != value:
            self._black_won = value
            self.black_won_changed.emit(value)

    # Property for white_won
    @property
    def white_won(self):
        return self._white_won

    @white_won.setter
    def white_won(self, value):
        if self._white_won != value:
            self._white_won = value
            self.white_won_changed.emit(value)

    # Property for turn
    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, value):
        if self._turn != value:
            self._turn = value
            self.turn_changed.emit(value)



# Create a global instance
config = Config()