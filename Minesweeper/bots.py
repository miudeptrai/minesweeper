class Bot:
    chance_matrix = None

    def __init__(self, name, string, board_len, board):
        self.name = name
        self.string = string #Not neccessary but just for fun
        self.board_len = board_len
        self.board = board
    
    def load_chance_matrix(self):
        pass