# This code has been written Charles Spencer Bowles around Sept. 9, 2019
# This code has been created to solve the gravitational force equation, prove the pythagorean identity,
# and find the distance of a point from the origin
# Sources:
# None
# OMH

import math as m

valid_input = False

while not valid_input:

    print('\nPlease choose problem')

    problem_number = input('(1/2/3/End): ').lower()

    if problem_number == '1':

        """
        The problem student forgot to use order of operations when writing his code.
        To fix his mistake I take the input values and use 3 methods to compute a correct value
        
        Method 1: Use parenthesis to order the operation properly
        Method 2: Use pythons built in pow() function to directly quote the formula
        Method 3: Use the pow() function from the math library and rules of exponents to eliminate division
        """

        mass1 = float(input('\nMass 1: '))
        mass2 = float(input('Mass 2: '))
        radius = float(input('Radius: '))

        force = 6.67408 * 10**-11 * mass1 * mass2 / (radius * radius)  # Method 1
        print(f'Force = {force} N')

        force = 6.67408 * 10**-11 * mass1 * mass2 / pow(radius, 2)  # Method 2
        print(f'Force = {force} N')

        force = 6.67408 * 10 ** -11 * mass1 * mass2 * m.pow(radius, -2)  # Method 3
        print(f'Force = {force} N')

    elif problem_number == '2':

        """
        The output value is not always 1.0 because of floating point errors
        Floating point errors occur with the manipulation of highly complex or irration floating point numbers
        The computer cannot store the exact value of the float so it will round
        This rounding error will create small deviations from the intended answer
        """

        theta = float(input('\nTheta: '))
        print(pow(m.sin(theta), 2) + pow(m.cos(theta), 2))

    elif problem_number == '3':

        """
        This snippet of code with take two inputs (x and y) 
        and use them to calculate the distance of the point (x, y) from the origin
        I use the formula d^2 = (x1-x2)^2 + (y1-y2)^2 to achieve this
        I have done some slight tweaking to achieve a simpler formula
        x2 and y2 are known to be 0, as the origin point is (0, 0)
        also i have taken the square root of both sides (.5th power)        
        """

        x = float(input('\nx: '))
        y = float(input('y: '))

        print(pow(pow(x, 2) + pow(y, 2), .5))

    elif problem_number == 'end':
        valid_input = True

    else:
        print('\nPlease choose a number I can understand ')