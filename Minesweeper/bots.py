class Bot:
    chance_matrix = None

    def __init__(self, name, string, board_len, board):
        self.name = name
        self.string = string
        self.board_len = board_len
        self.board = board
    
    def load_chance_matrix(self):
        pass