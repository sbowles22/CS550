# This code was written and developed by Charles Spencer Bowles around Sept. 9, 2019
# This code is meant to simulate a conversation between the user and the computer
# Sources:
# https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/ (Sept. 7 2019)
# OMH

import time  # to use sleep commend to simulate computer thought and comedic timing

print('\nHi! I\'m ChatBot, an interactive conversation program. What\'s your name?\n')
# introduction to establish connection and ask for name

user_name = input('Name: ').strip()  # takes and strips name (and stores under user_name variable)

if user_name[0].islower:  # capitalises name if the name is not capitalized
    user_name = user_name.title()

time.sleep(.5)  # pause to increase user experience

print(f'\nIt\'s great to meet you {user_name} how was your day?\n')  # uses name to ask user how their day was

valid_input = False

while not valid_input:  # will ask how a user's day was until a valid input is given

    user_feeling = input('(Good/Eh/Bad): ').lower().strip()  # takes user input and stores in user_feeling

    time.sleep(.5)  # pause to increase user experience

    if user_feeling == 'good':  # a response for users with a good day
        print('\nThat\'s amazing! I hope you keep having a great day!\n')
        time.sleep(1.2)  # pause to increase user experience
        print('You wanna hear a joke?\n')
        valid_input = True
    elif user_feeling == 'eh':  # a response for users with an eh day
        print('\nThat\'s okay! You don\'t always have to be decisive.\n')
        time.sleep(1.2)  # pause to increase user experience
        print('May I tell you a joke to make your day better?\n')
        valid_input = True
    elif user_feeling == 'bad':  # a response for users with a bad day
        print('\nAww, well keep your hopes up, just make sure tomorrow is better!\n')
        time.sleep(1.2)  # pause to increase user experience
        print('Can I tell you a joke to cheer you up?\n')
        valid_input = True
    else:  # invalid input handling
        print('\nI\'m sorry, but could you please choose an option I can understand?\n')
        time.sleep(.8)  # pause to increase user experience
        print(f'How was your day, {user_name}?\n')

valid_input = False

while not valid_input:  # will ask user if they want to hear a joke until a valid response is given

    user_joke = input('(Yes/No): ').lower().strip()  # takes and stores user input

    time.sleep(.5)  # pause to increase user experience

    if user_joke == 'yes':  # the joke itself
        print('\nWhat do you call a cow with no legs?')
        time.sleep(.5)  # pauses for comedic timing
        for i in range(3):  # more comedic pauses
            time.sleep(.7)
            print('.')
        time.sleep(.8)  # even more comedic pause
        print('GROUND BEEF! Hope you have a great day. Goodbye!\n')
        valid_input = True
    elif user_joke == 'no':  # a response for those without a sense of humor
        print(f'\nWell, okay then. Have a great day, {user_name}!')
        valid_input = True
    else:  # invalid input handling
        print('\nI\'m sorry, but could you please choose an option I can understand?\n')
        time.sleep(.8)  # pause to increase user experience
        print(f'Would you like to hear a joke, {user_name}?\n')