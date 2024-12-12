class Game:
    def __init__(self, difficulty="easy", mode=0):
        """
        Initialize the Game class.
        
        Parameters:
        - difficulty: "easy" or "hard". Determines AI depth. Default is "easy".
        - mode: 0 for AI-AI, 1 for User-AI (user is White), 2 for User-User. Default is 0.
        """
        # Difficulty settings
        self.difficulty = 5 if difficulty == "hard" else 2

        # Game mode: 0 = AI-AI, 1 = User-AI, 2 = User-User
        self.mode = mode

        # Round number, starting from 1
        self.round_no = 1

        # Turn tracking: 0 = Black, 1 = White
        self.turn = 0  # Black starts first

        # Game score
        self.score = {"Black": 0, "White": 0}


    def change_turn(self):
        """
        Change the turn between Black (0) and White (1).
        Increases the round number after both players (Black and White) have played.
        """
        if self.turn == 1:  # If it's White's turn now, and switching to Black, the round ends
            self.round_no += 1
        self.turn = 1 - self.turn  # Toggle between 0 (Black) and 1 (White)

    def __repr__(self):
        """
        String representation of the Game class.
        """
        mode_mapping = {0: "AI-AI", 1: "User-AI", 2: "User-User"}
        turn_mapping = {0: "Black", 1: "White"}
        return (f"Game(difficulty={'hard' if self.difficulty == 5 else 'easy'}, "
                f"mode={mode_mapping[self.mode]}, round_no={self.round_no}, "
                f"turn={turn_mapping[self.turn]}, score={self.score})")
