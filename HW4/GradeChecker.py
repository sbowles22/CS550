# This code was created by Spencer Bowles around Sept. 13, 2019
# This code is meant to be a grade checker for CS550
# Sources:
# None
# OMH

valid_response = False

while not valid_response:

    grade = float(input('Grade = ').strip())
    valid_response = True

    if not 0 <= grade <= 5:
        print('Enter number 0-5!')
        valid_response = False
    elif grade >= 4.85:
        print('A+')
    elif grade >= 4.65:
        print('A')
    elif grade >= 4.5:
        print('A-')
    elif grade >= 4.2:
        print('B+')
    elif grade >= 3.85:
        print('B')
    elif grade >= 3.5:
        print('B-')
    elif grade >= 3.2:
        print('C+')
    elif grade >= 2.85:
        print('C')
    elif grade >= 2.5:
        print('C-')
    elif grade >= 2:
        print('D+')
    elif grade >= 1.5:
        print('D')
    elif grade >= 1:
        print('D-')
    else:
        print('F')
