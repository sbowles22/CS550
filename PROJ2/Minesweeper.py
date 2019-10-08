# This code was created by Charles Spencer Bowles on Oct 5, 2019
# The purpose of this code is to emulate game-play of the popular computer game minesweeper
# Sources:
# https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
# OMH

from os import system, name
import sys
import random as rand

sys.setrecursionlimit(20000)
NULL = -2
try:
    HEIGHT = int(sys.argv[1])
    WIDTH = int(sys.argv[2])
    BOMBS = int(sys.argv[3])
    if not 1 <= HEIGHT <= 99:
        raise ValueError
    if not 1 <= WIDTH <= 99:
        raise ValueError
    if not 1 <= BOMBS < WIDTH * HEIGHT:
        raise ValueError
except IndexError or ValueError:
    print('Please indicate 3 numbers between 1 an 99 when calling the python file\n'
          '(the third has to be less than the product of the first 2)')
    quit()


class GameLoss(Exception):
    pass


class GameWin(Exception):
    pass


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def create_board(y1, x1, width=WIDTH, height=HEIGHT, bombs=BOMBS):
    board = [[[i + j * width, u"\u25A1", False] for i in range(width)] for j in range(height)]
    board[y1][x1][0] = -2
    for x in range(x1 + 1, width):
        board[y1][x][0] -= 1
    for y in range(y1 + 1, height):
        for x in range(width):
            board[y][x][0] -= 1
    for a in range(bombs):
        num = rand.randint(0, width * height - 2 - a)
        found = False
        for y in board:
            for x in y:
                if found:
                    if x[0] >= 0:
                        x[0] -= 1
                else:
                    if x[0] == num:
                        found = True
                        x[0] = -1
    for y in range(height):
        for x in range(width):
            if board[y][x][0] != -1:
                board[y][x][0] = 0
                try:
                    if x - 1 >= 0 and y - 1 >= 0:
                        if board[y - 1][x - 1][0] == -1:
                            board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if y - 1 >= 0:
                        if board[y - 1][x][0] == -1:
                            board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if y - 1 >= 0:
                        if board[y - 1][x + 1][0] == -1:
                            board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if x - 1 >= 0:
                        if board[y][x - 1][0] == -1:
                            board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if board[y][x + 1][0] == -1:
                        board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if x - 1 >= 0:
                        if board[y + 1][x - 1][0] == -1:
                            board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if board[y + 1][x][0] == -1:
                        board[y][x][0] += 1
                except IndexError:
                    pass
                try:
                    if board[y + 1][x + 1][0] == -1:
                        board[y][x][0] += 1
                except IndexError:
                    pass
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
            user_response = input(f'\n {display}, Format: x y\n\n > ').split()
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
                        display = 'Please enter valid coordinates'
                else:
                    display = 'Please enter 2 valid arguments'
            else:
                display = 'Please enter 2 arguments'
        except ValueError or IndexError:
            display = 'Please enter 2 coordinates to reveal a coordinate'
    win_check()
    while True:
        display = 'Which square would you like to reveal?'
        while True:
            clear()
            print_board(board)
            try:
                user_response = input(f'\n {display}, Format: x y (f)\n\n > ').split()
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
                                if not board[y][x][2]:
                                    if board[y][x][1] == 'F':
                                        board[y][x][1] = u"\u25A1"
                                    else:
                                        board[y][x][1] = 'F'
                                break
                            except IndexError:
                                display = 'Please enter proper coordinates'
                        else:
                            display = 'Third argument not recognized'
                    except IndexError:
                        try:
                            if board[y][x][1] == 'F':
                                display = 'Cannot reveal flagged square'
                            else:
                                reveal(x, y)
                                break
                        except IndexError:
                            display = 'Please enter valid coordinates'
                else:
                    display = 'Please enter 3 arguments'
            except ValueError or IndexError:
                display = 'Please enter 2 coordinates to reveal and possibly an f to flag a coordinate'
        win_check()


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
        print_board(board)
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

