# This project was created by Charles Spencer Bowles on Sept. 13, 2019
# The purpose of this code is to provide a non-linear text based experience as an RPG
# Sources:
# https://www.programiz.com/python-programming/user-defined-exception
# https://www.geeksforgeeks.org/clear-screen-python/ [1]

from os import system, name
import time
import random as rand


class Character:

    def __init__(self):
        self.user_class = ''
        self.max_hp = 0
        self.hp = 0
        self.moves = []
        self.all_moves = []
        self.name = ''
        self.gold = 3
        self.heath_pots = 2
        self.hp_increase = 0
        self.poison = 0

    def assign_class(self, user_class):
        if user_class == 'warrior':
            self.user_class = 'Warrior'
            self.max_hp = 5
            self.hp_increase = 2
            self.hp = 5
            self.moves = [slash]
            self.all_moves = [slash, bash, crash]
        elif user_class == 'ranger':
            self.user_class = 'Ranger'
            self.max_hp = 4
            self.hp_increase = 1
            self.hp = 4
            self.moves = [bow_and_arrow]
            self.all_moves = [bow_and_arrow, critical, tipped_knife]
        elif user_class == 'quit':
            self.user_class = 'Admin (God)'
            self.max_hp = 999
            self.hp = 999
            self.moves = [kill, null, poison]
            self.all_moves = [kill, null, poison]
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


class Cheat(Exception):
    pass


class Enemy:

    def __init__(self, name, starting_hp, moves):
        self.name = name
        self.max_hp = starting_hp
        self.hp = starting_hp
        self.moves = moves
        self.poison = 0

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            raise EnemyDeath
        elif self.hp >= self.max_hp:
            self.hp = self.max_hp


class Move:

    def __init__(self, name, damage, accuracy, poison=0):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.poison = poison


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
            try:
                cheats()
            except Cheat:
                valid_response = True
        elif 'credit' in user_response:
            credit()
        else:
            print('Please select a valid option\n')
            valid_response = False


# A setup function that runs through some functions to setup the game
def setup():
    get_class()
    get_name()
    intro()


# A function to allow the user to choose a class for the RPG
def get_class():
    title_text()
    print('Choose Class:\n\nWarrior    Ranger\n')

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
        try:
            if user_response[0] == 'y':
                valid_response = True
            elif user_response[0] == 'n':
                get_class()
                valid_response = True
            else:
                print('Please say yes or no')
        except IndexError:
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
            try:
                if user_response[0] == 'y':
                    valid_response = True
                elif user_response[0] == 'n':
                    get_name()
                    valid_response = True
                else:
                    print('Please say yes or no')
            except IndexError:
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
        'Type commands, attack the enemy, and if your health reaches 0,',
        'YOU DIE!',
        ''
    ]

    for line in instructions_lines:
        print(line)

    input('PRESS ENTER TO CONTINUE')
    title_screen()


# A function to belittle the player for being a dirty cheater
def cheats():
    title_text()
    call()
    if user_response == 'test':
        user.assign_class('quit')
        user.name = '_testing'
        raise Cheat
    title_screen()


# A function to display the creator of the game (He sounds like a cool dude)
def credit():
    print('This game was created and developed by Charles Spencer Bowles\n')
    input('PRESS ENTER TO CONTINUE')
    title_screen()


"""The Section dedicated to creating a title screen has ended"""
"""Now a section dedicated to inter-battle sections will begin"""


def run_location(place):
    clear()
    print(location_list[place] + '\n')
    input('PRESS ENTER TO CONTINUE')
    clear()
    if place == 0:
        print('A goblin jumps out of the trees and attacks you!\n')
        input('PRESS ENTER TO BATTLE!')
        initiate_battle(goblin)
    if place == 1:
        shop()
    if place == 2:
        print('An arrow skids by you as you spot a hostile elf\n')
        input('PRESS ENTER TO BATTLE!')
        initiate_battle(elf)
    if place == 3:
        print('The gnome lives for your blood, you should defend yourself\n')
        input('PRESS ENTER TO BATTLE!')
        initiate_battle(gnome)
    if place == 4:
        print('An orc towers over you, ready to smash you into the ground\n')
        input('PRESS ENTER TO BATTLE!')
        initiate_battle(orc)
    if place == 5:
        shop()
    if place == 6:
        print('A guard guards the lair in a guardy fashion in his guard tower\n')
        input('PRESS ENTER TO BATTLE!')
        initiate_battle(guard)
    if place == 7:
        print('The dragon\'s presence fills the room\n')
        input('PRESS ENTER TO BATTLE!')
        initiate_battle(dragon)


"""The section on inter battle sections has ended"""
"""The section on battles will begin"""


def initiate_battle(enemy):
    user.hp = user.max_hp
    user.poison = 0
    try:
        while True:
            user_menu(enemy)
            used_move = enemy.moves[rand.randint(0, len(enemy.moves) - 1)]
            print_condition(enemy)
            print(f'{enemy.name} uses {used_move.name}')
            time.sleep(1.2)
            use(used_move, user, enemy)

    except UserDeath:
        user_death()
    except EnemyDeath:
        enemy_death(enemy)


def print_condition(enemy):
    clear()
    print(f'Your health: {user.hp} / {user.max_hp}\n'
          f'Poison: {user.poison}\n\n'
          f'{enemy.name}\'s health: {enemy.hp} / {enemy.max_hp}\n'
          f'Poison: {enemy.poison}\n')


def user_menu(enemy):
    print_condition(enemy)

    valid_response = False

    while not valid_response:
        print_condition(enemy)
        print('Moves or Items\n')
        call()
        try:
            if 'm' == user_response[0]:
                valid_response2 = False
                while not valid_response2:
                    print_condition(enemy)
                    print('Your moves are: (type back to go back to the menu)\n')
                    list_moves()
                    print()
                    call()
                    if 'back' in user_response[:4]:
                        user_menu(enemy)
                        valid_response2 = True
                    else:
                        for move in user.moves:
                            if user_response == move.name.lower():
                                valid_response = True
                                valid_response2 = True
                                use(move, enemy, enemy)
                                break
                    if not valid_response2:
                        print('Please enter a move or back')
                        time.sleep(2)

            elif 'i' == user_response[0]:
                valid_response2 = False
                while not valid_response2:
                    print_condition(enemy)
                    print('Your items are: (type back to go back to the menu)\n'
                          f'Health Potions: {user.heath_pots}')
                    call()
                    try:
                        if 'back' in user_response[:4]:
                            user_menu(enemy)
                            valid_response2 = True
                        elif 'h' == user_response[0]:
                            if user.heath_pots > 0:
                                user.damage(-2)
                                print_condition(enemy)
                                print('Used health potion')
                                user.heath_pots -= 1
                                time.sleep(1.2)
                            else:
                                print_condition(enemy)
                                print('No health potions left')
                                time.sleep(1.2)
                        elif 'd' == user_response[0]:
                            user.damage(2)
                        else:
                            print('Please enter an item or back')
                            time.sleep(2)
                    except IndexError:
                        print('Please enter an item or back')
                        time.sleep(2)
            else:
                print('Please select Moves or Items')
                time.sleep(2)
        except IndexError:
            print('Please select Moves or Items')
            time.sleep(2)


def use(move, target, enemy):
    if rand.randint(1, 100) <= move.accuracy:
        target.damage(move.damage)
        target.poison += move.poison
        print_condition(enemy)
        print(f'{target.name} was hit by {move.name.lower()}!\n')
    else:
        print_condition(enemy)
        print(f'{move.name} missed!\n')
    input('PRESS ENTER TO CONTINUE')
    if target.poison > 0:
        target.damage(target.poison)
        target.poison -= 1
        print_condition(enemy)
        print(f'{target.name} was hit by {target.poison + 1} poison damage\n')
        input('PRESS ENTER TO CONTINUE')


def user_death():
    clear()
    print(f'Sadly, after all of their travels, {user.name} hath been slain.\nThey died with {user.gold} gold in their '
          f'pocket and no legacy to their name')
    input('PRESS ENTER TO DIE')
    quit()


def enemy_death(enemy):
    clear()
    if enemy.name != 'Dragon':
        gold_prize = rand.randint(1, 3)
        user.gold += gold_prize
        print(f'The {enemy.name} has \'fainted\'\nYou gained {gold_prize} gold!')
        try:
            user.moves.append(user.all_moves[len(user.moves)])
            print(f'You learned the move {user.moves[-1].name}')
        except IndexError:
            pass
        user.max_hp += user.hp_increase
        print(f'Your max hp is now {user.max_hp}')
    else:
        print(f'The dragon hath been slain!\n{user.name} must be the greatest {user.user_class} that has ever '
              f'lived!\nYou took the treasure of {rand.randint(1, 5) * 100} gold and invested it because you are '
              f'smart with money!\n')
    input('PRESS ENTER TO CONTINUE')


"""This ends the section on battles"""
"""The section of shops begins"""


def shop():
    valid_response = False
    while not valid_response:
        clear()
        print(f'Gold: {user.gold}\n\n'
              'Shop\'s wares:\n'
              'Health Potions - 2 gold\n\n'
              'Type in an item\'s name to buy it or just leave\n')
        call()
        try:
            if 'leave' in user_response[:5]:
                valid_response = True
            elif 'h' == user_response[0]:
                if user.gold >= 2:
                    user.gold -= 2
                    print('Bought health potion')
                    user.heath_pots += 1
                    time.sleep(1.2)
                else:
                    print('Not enough money')
                    time.sleep(1.2)
            else:
                print('Please enter an item or leave')
                time.sleep(2)
        except IndexError:
            print('Please enter an item or leave')
            time.sleep(2)


"""The sections on shops ends"""
# Move Creation
null = Move('.', 0, 100)
poison = Move('Poison', 0, 100, 2)
kill = Move('Kill', 999, 100)
slash = Move('Slash', 1, 90)
bash = Move('Bash', 2, 50)
crash = Move('Crash', 5, 30)
bow_and_arrow = Move('Bow and Arrow', 2, 70)
critical = Move('Critical', 7, 35)
bite = Move('Bite', 0, 85, 2)
slash_plus = Move('Slash+', 3, 90)
tipped_knife = Move('Tipped Knife', 1, 75, 2)
fire_breath = Move('Fire Breath', 3, 90)

# Enemy Creation
goblin = Enemy('Goblin', 3, [slash])
elf = Enemy('Elf', 5, [bow_and_arrow, bow_and_arrow, critical])
gnome = Enemy('Gnome', 7, [bite])
orc = Enemy('Orc', 10, [crash])
guard = Enemy('Guard', 9, [slash_plus])
dragon = Enemy('Dragon', 15, [fire_breath])

# Create global variables for the user and their response
user = Character()
user_response = ''

# Run the title screen
title_screen()

# List of location tooltips
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

for i in range(8):
    run_location(i)

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
