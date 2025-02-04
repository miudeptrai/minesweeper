import random

size = 10
board = [['.' for _ in range(size)] for _ in range(size)] #Display
matrix = [[0 for _ in range(size)] for _ in range(size)]
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

def findStartingNeighbours(i: int,j: int) -> list[tuple[int]]:
    starting_neighbours = []

    for add_i, add_j in neighbours_tiles:
        new_i = i + add_i
        new_j = j + add_j

        if 0 <= new_i < len(matrix) and 0 <= new_j < len(matrix): starting_neighbours.append((i,j))
    
    return starting_neighbours

def prepareMatrix(y: int, x: int) -> None:
    global matrix

    mines_pos = []
    starting_neighbours = findStartingNeighbours(y,x)

    #Determining whether or not a tile should be a mine-tile
    matrix_len = len(matrix)
    for i in range(matrix_len):
        for j in range(matrix_len):
            randomiser = random.randint(0,4) #This is the chance of getting a mine-tile. Currently 1/4
            #Make sure the starting position will always be a 0-tile
            if randomiser == 0 and not (i,j) in starting_neighbours:
                matrix[i][j] = 9 #9 is the indicator for a mine-tile
                mines_pos.append((i,j))

    #Changing the tile's number based on the neighbour tiles. If a neighbour tile is a mine-tile, raise the tile's number by 1
    for i in range(matrix_len):
        for j in range(matrix_len):
            if matrix[i][j] != 9:
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
    global visited

    if visited[i][j]: return

    visited[i][j] = True

    board[i][j] = str(matrix[i][j])

    #Too tired to explain this block
    if matrix[i][j] == 0:
        neighbours = graph[(i,j)]
        for new_i, new_j in neighbours:
            revealTile(new_i, new_j)

def isLose() -> bool:
    #If there's 9 which means mine
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '9': return True
    
    return False

def isWin() -> bool:
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            #Check for any possible unwinable scenerios
            if board[i][j] == 'f' and matrix[i][j] != 9: return False
            if board[i][j] == '.': return False
    
    return True

def printMatrix() -> None: #Debug tool
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j], end=' ')
        
        print()

def addToGraph() -> None:
    global graph

    #All tiles will represent its neighbours in graph
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
    #Greet
    print("Welcome to Minesweeper!")
    print("To dig a position type x and y in this form: x,y")
    print("To place a flag just add a 'f' at the end")

    #Pre-game(Choosing a position)
    printBoard()
    while True:
        action, x, y = promptForInput("Please choose a starting position: ")

        if action == "dig": break
    
    #Preparation
    prepareMatrix(y,x)
    addToGraph()

    revealTile(y, x)

    while True:
        printBoard()

        #Check if lose then break if yes
        if isLose():
            print("BOOM!!!")
            print("A mine exploded")
            print("You lose!")

            printMatrix()

            break
        #Check if win then break if yes
        if isWin():
            print("You win!")

            printMatrix()

            break

        action, x, y = promptForInput("Action: ")

        #Check whether or not the action is digging or placing a flag
        if action == "flag": board[y][x] = 'f'
        else: revealTile(y, x)

def debugMain() -> None: #Debug tool
    addToGraph()
    print(graph)

main()