# This code was created by Charles Spencer Bowles on Oct 5, 2019
# The purpose of this code is to emulate game-play of the popular computer game minesweeper
# Sources:
# https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it [1]
# OMH

from os import system, name  # for clear function
import sys  # for recursion depth
import random as rand  # to randomize mine generation

sys.setrecursionlimit(20000)  # this line sets recursion depth high enough to deal with larger boards [1]
NULL = -2  # setup NULL to be used as a placeholder in board generation

# This block of code deals with setting up variables from command line in order to generate board
try:  # Try block to allow raising of Value error on unreasonable board sized and number of mines and to make sure 3 arguments are given
    HEIGHT = int(sys.argv[1])  # Taking of ints from command line (doubles as an error checker for non int values)
    WIDTH = int(sys.argv[2])
    BOMBS = int(sys.argv[3])
    if not 1 <= HEIGHT <= 99:  # Checks to make sure board is not too massive that it breaks formatting in print_board()
        raise ValueError
    if not 1 <= WIDTH <= 99:
        raise ValueError
    if not 1 <= BOMBS < WIDTH * HEIGHT:  # Checks to make sure there is both bombs and that they dont fill every spot on the board
        raise ValueError
except IndexError or ValueError:  # This triggers whenever invalid inputs are given on the command line, and quits the program
    print('Please indicate 3 numbers between 1 an 99 when calling the python file\n'
          '(the third has to be less than the product of the first 2)')
    quit()


# Exception setup for both win and loss
class GameLoss(Exception):
    pass


class GameWin(Exception):
    pass


# Function to clear screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# This function creates the board once the first move has been given to prevent dying on first move
def create_board(x1, y1, width=WIDTH, height=HEIGHT, bombs=BOMBS):
    board = [[[i + j * width, u"\u25A1", False] for i in range(width)] for j in range(height)]  # creates a board with integers in [0 - width*height) and unicode characters and a false value which is used for checking if a space has been revealed
    # The false value is a simple to prevent infinite recursion during revealing 0s
    board[y1][x1][0] = -2  # sets first move to a NULL value
    for x in range(x1 + 1, width):  # These two for statements reduce every number following the first move by 1
        board[y1][x][0] -= 1
    for y in range(y1 + 1, height):
        for x in range(width):
            board[y][x][0] -= 1
    place_bombs(board, width, height, bombs)  # I could not place bombs and set values at the same time because of the way my board is generated as it would mess with the numbering
    set_values(board, width, height)  # So i set the values after all of the mines are placed
    return board


def print_board(board, raw=0):
    print('      ', end='')
    for i in range(len(board)):
        if i < 9:
            print(i + 1, end='  ')
        else:
            print(i + 1, end=' ')
    print('\n')
    for row in range(len(board)):
        if row < 9:
            print(f' {row + 1}', end='    ')
        else:
            print(f' {row + 1}', end='   ')
        for col in range(len(board[row])):
            try:
                print(board[row][col][(1, 0)[raw]], end='  ')
            except IndexError:
                print(row, col)
        print()


def reveal(x, y):
    global board
    if board[y][x][0] == -1:
        board[y][x][1] = '*'
        raise GameLoss
    else:
        board[y][x][1] = board[y][x][0]
        board[y][x][2] = True
        if board[y][x][0] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if not board[y + i][x + j][2]:
                            if y + i >= 0 and x + j >= 0:
                                reveal(x + j, y + i)
                    except IndexError:
                        pass


# This function checks if every space is either a mine or revealed, and if so, raises a game win
def win_check():
    try:
        for y in board:
            for x in y:
                if x[0] == -1 or x[2]:
                    pass
                else:
                    raise ValueError
        raise GameWin
    except ValueError:
        pass


def game():
    global board
    display = 'Which square would you like to reveal?'
    while True:
        clear()
        print_board(board)
        try:
            user_response = input(f'\n {display} Format: x y\n\n > ').split()
            for i in user_response:
                if 'quit' in i:
                    clear()
                    quit()
            if len(user_response) == 2:
                x = int(user_response[0]) - 1
                y = int(user_response[1]) - 1
                if x in range(WIDTH) and y in range(HEIGHT):
                    board = create_board(x, y)
                    try:
                        reveal(x, y)
                        break
                    except IndexError:
                        display = 'Please enter valid coordinates,'
                else:
                    display = 'Please enter 2 valid arguments,'
            else:
                display = 'Please enter 2 arguments,'
        except ValueError or IndexError:
            display = 'Please enter 2 coordinates to reveal a coordinate,'
    win_check()
    while True:
        display = 'Which square would you like to reveal?'
        while True:
            clear()
            print_board(board)
            try:
                user_response = input(f'\n {display} Format: x y (f)\n\n > ').split()
                for i in user_response:
                    if 'quit' in i:
                        clear()
                        quit()
                if 3 >= len(user_response) >= 2:
                    x = int(user_response[0]) - 1
                    y = int(user_response[1]) - 1
                    try:
                        if user_response[2][0].lower() == 'f':
                            try:
                                flag(board, x, y)
                                break
                            except IndexError:
                                display = 'Please enter proper coordinates,'
                        else:
                            display = 'Third argument not recognized,'
                    except IndexError:
                        try:
                            if board[y][x][1] == 'F':
                                display = 'Cannot reveal flagged square,'
                            else:
                                reveal(x, y)
                                break
                        except IndexError:
                            display = 'Please enter valid coordinates,'
                else:
                    display = 'Please enter 3 arguments,'
            except ValueError or IndexError:
                display = 'Please enter 2 coordinates to reveal and possibly an f to flag a coordinate,'
        win_check()


# This function is both used to flag and un-flag spaces
def flag(board, x, y):
    if not board[y][x][2]:
        if board[y][x][1] == 'F':
            board[y][x][1] = u"\u25A1"
        else:
            board[y][x][1] = 'F'


# The way that the mines are placed is very atypical compared to taking random points and checking if the points were already taken by a mine
# This algorithm gets a board where all free spaces are numbered 0 - (n-1), where n is the number of free spaces
# The algorithm then randomly chooses a number 0 - (n-1) and seeks for that number in the board and places a mine
# The algorithm then subtracts every value after the mine by 1 and repeats the algorithm for every mine requested
# The algorithm is created in this way to prevent the possibility of a large board with a large number of mines getting stuck
# Normal algorithms (pick and check) can get stuck rechecking mined squares and take inconsistent amounts of time to create a board
# This algorithm, however, cannot get stuck
def place_bombs(board, width, height, bombs):
    for a in range(bombs):  # Here is the algorithm for placing bombs this for loop loops a bomb number of times
        num = rand.randint(0, width * height - 2 - a)  # A random number on the board is generated
        found = False  # This boolean will be used later to adjust the values of ever number after the bomb
        for y in board:  # These 2 for loops iterate through every space on the board
            for x in y:
                if found:  # This if statement will only happen after the bomb has been placed and will subtract ever space after by 1
                    if x[0] >= 0:  # This second if statement is to prevent the program from subtracting bombs and the first move by 1
                        x[0] -= 1
                else:
                    if x[0] == num:  # This if checks to see if the random number is in a space
                        found = True
                        x[0] = -1  # Sets the space to a bomb


# This function is used to make every non mine square equal to the number of mines around it
def set_values(board, width, height):
    for y in range(height):
        for x in range(width):
            if board[y][x][0] != -1:
                board[y][x][0] = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        try:
                            if y + i >= 0 and x + j >= 0:
                                if board[y + i][x + j][0] == -1:
                                    board[y][x][0] += 1
                        except IndexError:
                            pass


while True:
    board = [[[NULL, u"\u25A1", False]] * WIDTH] * HEIGHT
    try:
        game()
    except GameLoss:
        clear()
        for y in board:
            for x in y:
                if x[0] == -1:
                    x[1] = '*'
        display = 'YOU LOSE'
    except GameWin:
        display = 'YOU WIN'
    while True:
        clear()
        print_board(board)
        user_response = input(f'\n {display}, would you like to play again? (Yes/No)\n\n > ').strip().lower()
        try:
            if user_response[0] == 'y':
                break
            if user_response[0] == 'n':
                clear()
                quit()
        except IndexError:
            pass
