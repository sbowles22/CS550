import sys

sys.argv[1] = int(sys.argv[1])

if sys.argv[1] == 1:
    num = float(input('Num = ')) % 10
    print(num <= 2 or num >= 8)
if sys.argv[1] == 2:
    num1 = float(input('Num 1 = '))
    num2 = float(input('Num 2 = '))
    print(num1 % num2 == 0 or num2 % num1 == 0)
if sys.argv[1] == 3:
    year = int(input('Year = '))
    print(year % 400 == 0 or (not year % 100 == 0 and year % 4 == 0))
if sys.argv[1] == 4:
    temp = int(input('Temperature = '))
    is_summer = input('is_summer = ').lower()
    print(60 <= temp <= (90 + (is_summer == 'true') * 10))
if sys.argv[1] == 5:
    nums = [0, 0, 0]
    nums[0] = int(input('a = '))
    nums[1] = int(input('b = '))
    nums[2] = int(input('c = '))
    nums.sort()
    print(nums)
    print((nums[1] - nums[0] <= 1 or nums[2] - nums[1] <= 1) and (nums[1] - nums[0] >= 2 or (nums[2] - nums[1]) >= 2))
