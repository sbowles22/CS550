# This project was created by Charles Spencer Bowles on Sept. 13, 2019
# The purpose of this code is to provide a non-linear text based experience as an RPG
# Sources:
# https://www.programiz.com/python-programming/user-defined-exception
# https://www.geeksforgeeks.org/clear-screen-python/ [1]

from os import system, name
import time


class Character:

    def __init__(self):
        self.user_class = ''
        self.max_hp = 0
        self.hp = 0
        self.moves = []
        self.name = ''
        self.location = 0
        self.gold = 3

    def assign_class(self, user_class):
        if user_class == 'warrior':
            self.user_class = 'Warrior'
            self.max_hp = 5
            self.hp = 5
            self.moves = [slash]
        else:
            raise ClassCreationError

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            raise UserDeath
        elif self.hp >= self.max_hp:
            self.hp = self.max_hp


class UserDeath(Exception):
    pass


class EnemyDeath(Exception):
    pass


class ClassCreationError(Exception):
    pass


class Enemy:

    def __init__(self, name, starting_hp):
        self.name = name
        self.max_hp = starting_hp
        self.hp = starting_hp


class Move:

    def __init__(self, name, damage, accuracy):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy


slash = Move('Slash', 1, 90)


def call():
    global user_response
    user_response = input('> ').strip().lower()
    print('')
    if user_response == 'quit':
        quit()


# Code taken from [1]
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


"""The following section of code seeks to create a title screen and setup for the game"""


# A function to clear the screen and display the title text
def title_text():
    # ________________  _____      _____   ________________   _________     ________          ________
    # |              |  \    \    /    /   |              |  |     _   \   |    _   \      __/  ___   \
    # |_____    _____|   \    \  /    /    |_____    _____|  |    / \   \  |   / \   \   _/  __/   \___\
    #      |   |          \    \/    /          |   |        |    \_/   /  |   \_/   /  /   /
    #      |   |           \        /           |   |        |       __/   |    ____/  |   |       _______
    #      |   |           /        \           |   |        |       \     |   |       |   |      |__     |
    #      |   |          /    /\    \          |   |        |   |\   \    |   |        \_  \__   __/  /| |
    #      |   |         /    /  \    \         |   |        |   | \   \   |   |          \__  \_/  __/ |_|
    #      |___|        /____/    \____\        |___|        |___|  \___\  |___|             \_____/
    clear()
    print("\n ________________  _____      _____  ________________   _________     ________          ________\n |     "
          "         |  \\    \\    /    /  |              |  |     _   \\   |    _   \\      __/  ___   \\\n |_____   "
          " _____|   \\    \\  /    /   |_____    _____|  |    / \\   \\  |   / \\   \\   _/  __/   \\___\\\n       | "
          "  |         \\    \\/    /          |   |       |    \\_/   /  |   \\_/   /  /   /\n       |   |          "
          "\\        /           |   |       |       __/   |    ____/  |   |       _______\n       |   |          /   "
          "     \\           |   |       |       \\     |   |       |   |      |__     |\n       |   |         /    "
          "/\\    \\          |   |       |   |\\   \\    |   |        \\_  \\__   __/  /| |\n       |   |        /   "
          " /  \\    \\         |   |       |   | \\   \\   |   |          \\__  \\_/  __/ |_|\n       |___|       "
          "/____/    \\____\\        |___|       |___|  \\___\\  |___|             \\_____/\n\n")


# A function to create a menu for options when the game boots
def title_screen():

    valid_response = False


    while not valid_response:

        valid_response = True

        title_text()
        print("         Play!          Instructions          Cheats           Credits           Quit\n")

        call()
        if 'play' in user_response:
            setup()
        elif 'instruction' in user_response:
            instructions()
        elif 'cheat' in user_response:
            cheats()
        elif 'credit' in user_response:
            credit()
        else:
            print('Please select a valid option\n')
            valid_response = False


# A setup function that runs through the functions to setup the game
def setup():

    get_class()
    get_name()
    intro()


# A function to allow the user to choose a class for the RPG
def get_class():

    title_text()
    print('Choose Class:\n\nWarrior\n')

    valid_response = False

    while not valid_response:
        call()
        try:
            user.assign_class(user_response)
            valid_response = True
        except ClassCreationError:
            print('Please choose a class that exists\n')

    print(f'You are a {user.user_class}\nYou start with {user.max_hp} HP\nYour moves are:')
    list_moves()

    valid_response = False
    while not valid_response:
        print('\nWould you like to play as this class?\n')
        call()
        if user_response[0] == 'y':
            valid_response = True
        elif user_response[0] == 'n':
            get_class()
            valid_response = True
        else:
            print('Please say yes or no')


# A function that will get the name of the player
def get_name():

    title_text()
    print(f'What is your name, young {user.user_class.lower()}?\n')
    user.name = input('> ').strip()

    if len(user.name) < 1:
        print('That is no name!\n')
        time.sleep(2)
        get_name()
    else:
        valid_response = False

        while not valid_response:
            print(f'\nWould you like to be named {user.name}, young {user.user_class.lower()}?\n')
            call()
            if user_response[0] == 'y':
                valid_response = True
            elif user_response[0] == 'n':
                get_name()
                valid_response = True
            else:
                print('Please say yes or no')


# A function to provide an introduction to the player
def intro():
    title_text()
    print(f'A young {user.user_class.lower()} sets out on their journey to become\nthe greatest adventurer of all time '
          f'and slay the dragon!\n\n     Godspeed, {user.name}.\n')
    input('PRESS ENTER TO CONTINUE')


# A function to list all of the moves a user has in his or her arsenal (Grammatically correctly)
def list_moves():
    for move in range(len(user.moves)):
        if len(user.moves) == 1:
            print(user.moves[move].name)
        elif len(user.moves) == 2:
            print(f'{user.moves[0].name} and {user.moves[1].name}')
            break
        elif len(user.moves) >= 3:
            if move != len(user.moves) - 1:
                print(f'{user.moves[move].name}, ', end='')
            else:
                print(f'and {user.moves[move].name}')


# A function to display an overview of the game, plot, and instructions
def instructions():
    instructions_lines = [
        'You are an adventurer attempting to find a dragon.',
        'If you manage to defeat the dragon,',
        'you\'ll be able to steal its treasure!',
        '',
        'But, to find the dragon, you must first',
        'fight, win, and stay alive on this text adventure!',
        '',
        'Types commands, attack the enemy, and if your health reaches 0,',
        'YOU DIE!',
        ''
    ]

    for line in instructions_lines:
        print(line)

    input('PRESS ENTER TO CONTINUE')
    title_screen()


# A function to belittle the player for being a dirty cheater
def cheats():
    print('Cheats are for losers!\n')
    input('PRESS ENTER TO CONTINUE')
    title_screen()


# A function to display the creator of the game (He sounds like a cool dude)
def credit():
    print('This game was created and developed by Charles Spencer Bowles\n')
    input('PRESS ENTER TO CONTINUE')
    title_screen()


# Create global variables for the user and their response
user = Character()
user_response = ''

# Run the title screen
title_screen()

"""The Section dedicated to creating a title screen has ended"""
"""Now a section dedicated to inter-battle sections will begin"""

location_list = [
    'As you begin your journey, you follow a path heading into a forest.',
    'In the forest, you find a shopkeeper selling his wares',
    'You leave the forest, revealing the path continues across an open field.',
    'The path from the field leads you into a scorched village.',
    'Leaving the village you see a small shop stall set up.',
    'As possibly the last shop you\'ll ever see fades into the distance, an entrance to a cave appears, you walk in.',
    'Things begin to heat up as you continue into the cave and you can begin to see the dim glow of lava on the walls.',
    f'You have fought hordes to be here, but it is finally your moment, young {user.user_class.lower()}, '
    'the dragon\'s lair awaits.'
]


def run_location(place):
    clear()
    print(location_list[place])
    if place == 1:
        pass
    if place == 2:
        pass
    if place == 3:
        pass
    if place == 4:
        pass
    if place == 5:
        pass
    if place == 6:
        pass
    if place == 7:
        pass
    if place == 8:
        pass


"""The section on inter battle sections has ended"""
"""The section on battles will begin"""


def initiate_battle(enemy):
    display_conditions(enemy)


def display_conditions(enemy):
    clear()
    print(f'You\'re health: {user.hp} / {user.max_hp}')
    print(f'Enemy health: {enemy.hp} / {enemy.max_hp}')


"""
Comments:

My Notes: Sorry, there is no gameplay as of now,
if you have any specific ideas, please dont hesitate to share (E.g. Status Effect moves would be nice)


Ting - Your start is really good. I think you're in a good place to start implementing some of the attacks or fighting classes.
# I really like the way the selection screen works! now just make the story cool!

#Stan Nice start, just keep on with this style and it's going to be great. But do spend more time on the adventure it self than the combat system.

# Kate - This looks really great so far! I like the big letters at the beginning. Also, one tiny thing
(not to be annoying!!! seriously!) but I think it should be "Your health" not "You're health!" Really great job!!!

# I like it! The ASCII art took dedication. Nice job. It's a little hard to judge based on the lack of gameplay,
# but all of the instructions were very clear and simple. Good start!
# - Chandler

#I really love the layout of the game! Its going to be fun once you have written more of the story. You should add more classes

#damn that title slide looks like it took a lot of effort! seems like an ambitious game, and i look forward to playing it once gameplay is available - claire
"""