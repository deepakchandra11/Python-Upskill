#1) Check if All Numbers are Positive. Given a list of integers, determine if all numbers are positive. Using all()

numbers = [1, 2, 3, 4, 5]
result = all(n > 0 for n in numbers)
print(result)

#------------------------------------------------------------------------------------------
#2) Check if Any Number is Even. Given a list of integers, check if any number is even. Using any()

numbers = [1, 3, 5, 7, 8]
result = any(n % 2 == 0 for n in numbers)
print(result)

#------------------------------------------------------------------------------------------
#3) Determine if any number in a list is divisible by 5 an print.
numbers = [2, 10, 20, 11, 45, 23]
for n in numbers:
    if n % 5 == 0:
        print(n)
