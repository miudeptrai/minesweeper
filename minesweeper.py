import random

board = [['.' for _ in range(5)] for _ in range(5)] #Display
matrix = [[0 for _ in range(5)] for _ in range(5)]
neighbours_tiles = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)] #(i,j) <=> (y,x)
graph = {}
visited = [[False for _ in range(len(matrix))] for _ in range(len(matrix))]

def numTile(i: int, j: int, mines_pos: tuple[int]) -> None:
    global matrix

    mine_count = 0
    for add_i, add_j in neighbours_tiles:
        new_i = i + add_i
        new_j = j + add_j

        if 0 <= new_i < len(matrix) and 0 <= new_j < len(matrix) and (new_i, new_j) in mines_pos: mine_count += 1
    
    matrix[i][j] = mine_count

def prepareMatrix() -> None:
    global matrix

    mines_pos = []

    #Determining whether or not a tile should be a mine-tile
    matrix_len = len(matrix)
    for i in range(matrix_len):
        for j in range(matrix_len):
            randomiser = random.randint(0,4) #This is the chance of getting a mine-tile. Currently 1/5
            if randomiser == 0:
                matrix[i][j] = -1 #-1 is the indicator for a mine-tile
                mines_pos.append((i,j))

    #Changing the tile's number based on the neighbour tiles. If a neighbour tile is a mine-tile, raise the tile's number by 1
    for i in range(matrix_len):
        for j in range(matrix_len):
            if matrix[i][j] != -1:
                numTile(i, j, mines_pos)

def printBoard() -> None:
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end=' ')
        
        print()

def isValidInput(input: tuple[int]) -> bool:
    x, y = input

    if (x >= 0 and x < len(board)) and (y >= 0 and y < len(board)) and (board[y][x] == '.' or board[y][x] == 'f'): return True

    return False

def promptForInput(prompt: str) -> tuple[str | int]:
    while True:
        action = input(prompt)

        if action[0].isnumeric() and action[2].isnumeric() and isValidInput((int(action[0]), int(action[2]))): break
    
    if action[-1] == 'f': return "flag", int(action[0]), int(action[2])

    return "dig", int(action[0]), int(action[2])

def revealTile(i: int, j: int) -> None:
    global board

    board[i][j] = str(matrix[i][j])

    if matrix[i][j] == 0:
        if visited[i][j]: return

        visited = True

        neighbours = graph[(i,j)]
        for new_i, new_j in neighbours:
            revealTile(new_i, new_j)

def isLose() -> bool:
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '-1': return True
    
    return False

def printMatrix() -> None: #Debug tool
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j], end=' ')
        
        print()

def addToGraph() -> None:
    global graph

    neighbours = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for add_i, add_j in neighbours_tiles:
                new_i = i + add_i
                new_j = j + add_j
                if 0 <= new_i < len(matrix) and 0 <= new_j < len(matrix): neighbours.append((new_i,new_j))
            
            graph[(i,j)] = neighbours
            neighbours = []

def main() -> None:
    prepareMatrix()
    addToGraph()

    printBoard()
    while True:
        action, x, y = promptForInput("Please choose a starting position: ")

        if action == "dig": break
    
    revealTile(y, x)

    while True:
        printBoard()

        if isLose():
            print("BOOM!!!")
            print("A mine exploded")
            print("You lose!")

            printMatrix()

            break

        action, x, y = promptForInput("Action: ")

        if action == "flag": board[y][x] = 'f'
        else: revealTile(y, x)

def debugMain() -> None:
    addToGraph()
    print(graph)

print("Welcome to Minesweeper!")
print("To dig a position type x and y in this form: x,y")
print("To place a flag just add a 'f' at the end")

main()