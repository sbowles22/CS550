import math as m

valid_input = False

while not valid_input:

    print('\nPlease choose problem')

    problem_number = input('(1/2/3/End): ').lower()

    if problem_number == '1':
        pass
    if problem_number == '2':
        x = int(input('x = '))
        y = int(input('y = '))
        z = int(input('z = '))
        print((x > y) + (z > y) == 1)