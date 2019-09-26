import sys

try:
    if sys.argv[1].lower() == 'f':
        temp = float(sys.argv[2]) * (9/5) + 32.0
    elif sys.argv[1].lower() == 'c':
        temp = (float(sys.argv[2]) - 32.0) * (5/9)
    else:
        print('ERROR: Please input C or F as argument 1')
        quit()

    temp = round(temp)
    print(f'{temp}°{sys.argv[1].title()}')

except ValueError:
    print('ERROR: Please input a number for argument 2')

except IndexError:
    print('ERROR: Please enter 2 arguments')
