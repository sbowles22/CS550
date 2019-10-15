# This code was created by Charles Spencer Bowles on Oct 5, 2019
# The purpose of this code is to emulate game-play of the popular computer game minesweeper
# The game is emulated by making a 3D list (called a board) where the parameters are y, x, and then data/visuals
# The visual board lacks information during the beginning, however once a square is revealed for the data underneath, information is shared with the user
# This information comes in the number of mines around the space, and is important as, if one reveals a mine, they die
# The goal of the user is to reveal all non-mine spaces without revealing any mines
# The amount of time that the user takes to beat the board is recorded, and is stored in an external log so the user can track their progress on their minesweeper skill
# Sources:
# https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it [1]
# https://unicode-table.com/en/#control-character
# https://dbader.org/blog/python-check-if-file-exists
# https://stackoverflow.com/questions/2769061/how-to-erase-the-file-contents-of-text-file-in-python
# OMH

from os import system, name  # for clear function
import os.path  # for record keeping
import sys  # for recursion depth
import random as rand  # to randomize mine generation
import time  # for stopwatch


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


# This function iterates through every item in the board and prints it
def print_board(board, raw=0):
    print('      ', end='')  # This chunk of code prints the upper row of numbers
    for i in range(len(board)):
        if i < 9:
            print(i + 1, end='   ')
        else:
            print(i + 1, end='  ')
    print('\n')
    for row in range(len(board)):  # This for loop prints every line starting with a line number
        if row < 9:
            print(f' {row + 1}', end='    ')
        else:
            print(f' {row + 1}', end='   ')
        for col in range(len(board[row])):
            print(board[row][col][(1, 0)[raw]], end='   ')
        print('\n')


# This function is to setup variables for the creation of boards
def setup():
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
        return HEIGHT, WIDTH, BOMBS
    except IndexError or ValueError:  # This triggers whenever invalid inputs are given on the command line, and quits the program
        print('Please indicate 3 numbers between 1 an 99 when calling the python file\n'
              '(the third has to be less than the product of the first 2)')
        quit()


# This function creates the board once the first move has been given to prevent dying on first move
def create_board(x1, y1, width, height, bombs):
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


# This function handles revealing squares and checking for a game loss
def reveal(x, y):
    global board
    if board[y][x][0] == -1:  # This section raises a game loss
        board[y][x][1] = '*'
        raise GameLoss
    else:
        board[y][x][1] = board[y][x][0]
        board[y][x][2] = True
        if board[y][x][0] == 0:  # This section reveals spaces and, if a zero, reveals all unrevealed squares around it
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


# This function is the game loop
def game():
    move(1)  # The first move is different to prevent flagging on the first move and to only generate a new board on the first move
    while True:
        move()


# This function is both used to flag and un-flag spaces
def flag(board, x, y):
    if not board[y][x][2]:
        if board[y][x][1] == '🏳':
            board[y][x][1] = u"\u25A1"
        else:
            board[y][x][1] = '🏳'


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


# This function displays the board, gets the user's move, and runs the reveal anf flag functions
# It differs on the first move, where the user doesnt have the option to flag bc there is no reason for them to flag a square
def move(first=0):
    global board
    display = 'Which square would you like to reveal?'  # Display is a variable that will be displayed after the screen is cleared, and fixes the problem with having to sleep after an error
    while True:  # Loop keeps on until a there is a valid input
        clear()
        print_board(board)
        try:
            user_response = input(f'\n {display} Format: x y {("(f)", "")[first]}\n\n > ').split()
            for i in user_response:  # putting quit into the program quits the program
                if 'quit' in i:
                    clear()
                    quit()
            if 2 <= len(user_response) <= (3, 2)[first]:  # Checking if the input has 2 or 3 inputs, or only 2 if it is the first move
                x = int(user_response[0]) - 1
                y = int(user_response[1]) - 1
                try:
                    if first:
                        board = create_board(x, y, WIDTH, HEIGHT, BOMBS)  # Only creates board ion first move
                    if user_response[2][0].lower() == 'f':  # checks 3rd parameter for flag to see if a the program should flag a space
                        try:
                            flag(board, x, y)
                            break
                        except IndexError:  # A large block of error checking and error messages that are dynamic to if it is the first move
                            display = 'Please enter proper coordinates,'
                    else:
                        display = 'Third argument not recognized,'
                except IndexError:
                    try:
                        if board[y][x][1] == '🏳':
                            display = 'Cannot reveal flagged square,'
                        else:  # This is the only valid path for inputs, so it is the only one that reveals
                            reveal(x, y)
                            break
                    except IndexError:
                        display = 'Please enter valid coordinates,'
                else:
                    display = f'Please enter {("2-3", "2")[first]} valid arguments,'
            else:
                display = f'Please enter {("2-3", "2")[first]} arguments,'
        except ValueError or IndexError:
            display = f'Please enter 2 coordinates to reveal a coordinate {("and possibly an f to flag", "")[first]},'
    if first:  # Begins the game timer after the first move
        global game_time
        game_time = time.time()
    win_check()


sys.setrecursionlimit(20000)  # this line sets recursion depth high enough to deal with larger boards [1]
NULL = -2  # setup NULL to be used as a placeholder in board generation
HEIGHT, WIDTH, BOMBS = setup()
game_time = 0


while True:  # Game loop
    board = [[[NULL, u"\u25A1", False]] * WIDTH] * HEIGHT  # A placeholder board to print before the actual board is printed
    try:
        game()
    except GameLoss:
        for y in board:  # This block of code reveals all bombs on the board before the board is printed
            for x in y:
                if x[0] == -1:
                    x[1] = '*'
        display = 'YOU LOSE, '
    except GameWin:
        record = round(time.time() - game_time, 1)  # The amount of time it took to clear the board rounded to 1 decimal
        display = f'YOU WIN! It only took you {record} seconds.\n '
        if os.path.isfile('records.txt'):  # To check if the records file exists, if so, all data is dumped into old_record, if not, it is created and a dummy record is created
            record_file = open('records.txt', 'r+')
            old_record = record_file.readlines()
            record_file.close()
        else:
            record_file = open('records.txt', 'w')
            old_record = ['0 0 0 0']
            record_file.close()
        for i in range(len(old_record)):  # Change all parts of the old record lists into lists
            old_record[i] = old_record[i].split()
        try:
            for line in old_record:  # Goes through all lines of old_record, and if a record is found with the same parameters as an existing record, the old record is compared to the new time
                if list(map(str, [HEIGHT, WIDTH, BOMBS])) == line[:3]:
                    if float(line[3]) > record:  # This block of code overwrites old record if new record is faster
                        line[3] = record
                        display += f'Congrats on beating your previous record!\n Your new record for a {HEIGHT} x {WIDTH} board with {BOMBS} bombs is {record} seconds!'
                    else:
                        display += f'Better luck next time, and try to beat your old record of {line[3]} seconds!'
                    raise RecursionError  # Chose recursion error as it would otherwise never occur in this code, this raise prevents the "record not found" piece of code from triggering if thw record exists
            display += f'You set your record of {record} seconds for a {HEIGHT} x {WIDTH} board with {BOMBS} bombs!\n Try to beat it next time!'  # The record not found piece of code that runs if the record is set with a new set of parameters
            old_record.append([HEIGHT, WIDTH, BOMBS, record])
        except RecursionError:
            pass
        record_file = open('records.txt', 'w')  # Writes the new file with the old_record list, which, possibly, has been modified
        for piece in old_record:
            for part in piece:
                record_file.write(str(part) + ' ')
            record_file.write('\n')
        record_file.close()
        display += '\n '
    while True:  # A loop that runs until the user chooses to rerun the program
        clear()
        print_board(board)
        user_response = input(f'\n {display}Would you like to play again? (Yes/No)\n\n > ').strip().lower()
        try:
            if user_response[0] == 'y':
                break
            if user_response[0] == 'n':
                clear()
                quit()
        except IndexError:
            pass
