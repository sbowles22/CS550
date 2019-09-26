def greet(*args):
    for name in args:
        print(f'Hello, {name}!')


greet("Bob", "Timothy", "Sue", "Gerold")