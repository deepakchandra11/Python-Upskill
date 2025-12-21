#---------------------------------------------------------------------------------
#------------------------   Assignment 1               -----------------------
#---------------------------------------------------------------------------------
from functools import reduce

nums = [1,2,3,4]
list_by_2 = list(map(lambda x : x*2, nums))
print(list_by_2);


nums = [1,2,3,4,5,6,7,8,9,10]
evens = list(filter(lambda x : x%2 == 0, nums))
print(evens)


words = ["apple", "banana", "cherry", "date"]
longest_word = reduce(lambda x,y : y if len(x) < len(y) else x, words)
print(longest_word)


my_names = ["olumide", "akinremi", "josiah", "temidayo", "omoseun"]
fewer_than_7_chars_list = list(filter(lambda item: len(item) <=7, my_names))
print(fewer_than_7_chars_list)


nums = [1, 2, 3, 4, 5]
sum_of_nums = reduce(lambda acc,x : acc+x, nums)
print(sum_of_nums)

#---------------------------------------------------------------------------------
#------------------------   Assignment 2               -----------------------
#---------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------
#------------------------   Assignment 3               -----------------------
#---------------------------------------------------------------------------------
# 1) Using below list and enumerate(), print index followed by value. 
fruits = ["apple", "banana", "cherry"]

for index, item in enumerate(fruits):
  print(index, item)
  

#-------------------------------------------------------------------
# 2) Using below dict and enumerate, print key followed by value
  
person = {"name": "Alice", "age": 30, "city": "New York"}
for key, value in person.items():
  print(f"{key}:{value}") 

#-------------------------------------------------------------------
# 3) create a list of tuples where each tuple contains the index and the corresponding fruit, but only for even indices.

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

result = [(index, fruit) for i, fruit in enumerate(fruits, start=1) if i % 2 == 0]
    
print(result)

#---------------------------------------------------------------------------------
#------------------------ 	Assignment 4               -----------------------
#---------------------------------------------------------------------------------

# 1) Find the Maximum and Minimum Values in a List
numbers = [1, 32, 63, 14, 5, 26, 79, 8, 59, 10]

print(f"Max Value: {max(numbers)}, Min Value: {min(numbers)}")

#--------------------------------------------------------------------------
# 2) Given a set of numbers, find the maximum and minimum values.
setn = {5, 10, 3, 15, 2, 20}


print(f"Max Value: {max(setn)}, Min Value: {min(setn)}")

#---------------------------------------------------------------------------
# 3) Function to Find Shortest and Longest Word

def shortest_and_longest_word(words):
    return (min(words, key=len), max(words, key=len))


words = ["apple", "banana", "kiwi", "grapefruit", "orange"]
print(shortest_and_longest_word(words))

#---------------------------------------------------------------------------------
#------------------------   Assignment 5               -----------------------
#---------------------------------------------------------------------------------


# 1) ZeroDivisionError
def divide(a, b):
  try:
    res = a / b;
  except ZeroDivisionError as e:
    print(f"error: {e}")
    
divide(10, 0)

#--------------------------------------------------------------------------
# 2) index is out of range error
my_list = [1, 2, 3]

try :
  print(my_list[5])
except IndexError as e:
  print(f"Index Out of Bound error: {e}")

#---------------------------------------------------------------------------
# 3) appropriate exception handlings

def safe_divide(a, b):
    try:
        result = a / b
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    except TypeError:
        print("Error: Invalid input type")
    finally:
        print("Execution completed")


safe_divide(1, 0)
safe_divide(1, "a")

#---------------------------------------------------------------------------------
#------------------------   Assignment 6               -----------------------
#---------------------------------------------------------------------------------

# 1) Decorator to calculate start time, end time & total time
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()

for _ in range(10):
    print(next(fib))


#----------------------------------------------------------------------------
# 2) retry decorator
def retry(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
            print("All retry attempts failed")
        return wrapper
    return decorator


@retry(3)
def may_fail(name):
    print(f"Hello, {name}!")
    raise ValueError("Random failure")

may_fail("Deepak")


#----------------------------------------------------------------------------
# 3) validate_positive decorator

def validate_positive(func):
    def wrapper(x):
        if x <= 0:
            print("negative number")
            return
            #raise ValueError("square root of negative number can't be found")
        return func(x)
    return wrapper


@validate_positive
def square_root(x):
    return x ** 0.5


print(square_root(9))
print(square_root(-4))

#----------------------------------------------------------------------------
# 4) cache decorator

def cache(func):
    cached_results = {}

    def wrapper(*args):
        if args in cached_results:
            print("Returning cached result...")
            return cached_results[args]

        result = func(*args)
        cached_results[args] = result
        return result

    return wrapper


@cache
def expensive_computation(x):
    print("Performing computation...")
    return x * x


print(expensive_computation(5))
print(expensive_computation(5))


#----------------------------------------------------------------------------
# 5) requires_permission decorator
def requires_permission(func):
    def wrapper(user, *args, **kwargs):
        if 'admin' not in user.get('permissions', []):
            print("Access denied")
            return
        return func(user, *args, **kwargs)
    return wrapper


@requires_permission
def delete_user(user, user_id):
    print(f"User {user_id} deleted by {user['name']}")


user1 = {'name': 'Alice', 'permissions': ['admin']}
user2 = {'name': 'John', 'permissions': ['dev']}
user3 = {'name': 'Kurt', 'permissions': ['test']}


delete_user(user1, 101)
delete_user(user2, 102)
delete_user(user3, 103)

#---------------------------------------------------------------------------------
#------------------------   Assignment 7               -----------------------
#---------------------------------------------------------------------------------

# 1) Generator for Fibonacci Numbers
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()

for i in range(10):
    print(next(fib))


#----------------------------------------------------------------------------
# 2) Generator for Infinite Multiples
def infinite_multiples(n):
    multiple = n
    while True:
        yield multiple
        multiple += n


multiples_of_3 = infinite_multiples(3)

for _ in range(10):
    print(next(multiples_of_3))



#----------------------------------------------------------------------------
# 3) Generator to Repeat a Word a Fixed Number of Times

def repeat_word(word, times):
    for _ in range(times):
        yield word


repeated_word = repeat_word("hello", 5)

for value in repeated_word:
    print(value)


#---------------------------------------------------------------------------------
#------------------------   Assignment 8               -----------------------
#---------------------------------------------------------------------------------

# 1) Read and display entire content of a file
with open("sample.txt", "r") as file:
    content = file.read()
    print(content)


#----------------------------------------------------------------------------
# 2) count the number of words in a file
with open("words.txt", "r") as file:
    content = file.read()
    words = content.split()
    print("Number of words:", len(words))


#----------------------------------------------------------------------------
# 3) “Hello, Python!” into a file

with open("output.txt", "w") as file:
    file.write("Hello, Python!")

#----------------------------------------------------------------------------
# 4) CSV file named students.csv
import csv

data = [
    ["Name", "Roll Number", "Marks"],
    ["Alice", "101", "85"],
    ["Bob", "102", "90"],
    ["Charlie", "103", "88"]
]

with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)  


#----------------------------------------------------------------------------
# 5) Large file decorator 

def large_file(filename):
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()

file_content = large_file("file.txt")

for line in file_content:
    print(line)


#---------------------------------------------------------------------------------
#------------------------   Assignment 9               -----------------------
#---------------------------------------------------------------------------------
# 1) class Person
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


p = Person("Alice", 30)
print(f"Name: {p.name}, Age: {p.age}")


#--------------------------------------------------------------------------
# 2) class BankAccount
class BankAccount:
    def __init__(self, account_number, customer_name, balance=0):
        self.account_number = account_number
        self.customer_name = customer_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            print(f"Withdrawn {amount}. Remaining balance: {self.balance}")

    def check_balance(self):
        print("Current balance:", self.balance)


account = BankAccount("ACC101", "John")
account.deposit(500)
account.withdraw(200)
account.check_balance()


#---------------------------------------------------------------------------
# 3) class Book

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @classmethod
    def from_string(cls, data):
        title, author = data.split(", ")
        return cls(title, author)


book = Book.from_string("Python Programming, John Doe")

print("Title:", book.title)
print("Author:", book.author)

#---------------------------------------------------------------------------
# 4) Inheritance

class Animal:
    def sound(self):
        print("Animal makes a sound")


class Dog(Animal):
    def sound(self):
        print("Dog barks")


class Cat(Animal):
    def sound(self):
        print("Cat meows")


dog = Dog()
cat = Cat()

dog.sound()
cat.sound()




#---------------------------------------------------------------------------
# 5) multiple Inheritance

class Father:
    def skills(self):
        print("Gardening")


class Mother:
    def skills(self):
        print("Cooking")


class Child(Father, Mother):
    def child_method():
      print("Child Method")


child = Child()
child.skills()


#---------------------------------------------------------------------------------
#------------------------   Assignment 10               -----------------------
#---------------------------------------------------------------------------------

# 1) Using datetime, ​​add a week and 12 hours to a date.  Given date: March 22, 2020, at 10:00 AM. print original date time and new date time
from datetime import datetime, timedelta

original_date = datetime(2020, 3, 22, 10, 0)

new_date = original_date + timedelta(weeks=1, hours=12)

print(f"Original Date: {original_date}, New Date: {new_date}")


#--------------------------------------------------------------------------
# 2) Code to get the dates of yesterday, today, and tomorrow.
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)



#---------------------------------------------------------------------------
# 3) List all the files and folders in the current working directory and remove the directory “test” that was created.

import os

# Current working directory
cwd = os.getcwd()
print("Current Working Directory:", cwd)

# Create folder "test"
os.mkdir("test")

# List files and folders
print("Contents of CWD:")
print(os.listdir(cwd))

# Remove the folder "test"
os.rmdir("test")

#---------------------------------------------------------------------------
# 4) Write a Python program to rename a file from old_name.txt to new_name.txt.

import os

os.rename("old_name.txt", "new_name.txt")



#---------------------------------------------------------------------------
# 5) Create a file and Write a Python program to get the size of a file named example.txt 

import os

# Create file
with open("example.txt", "w") as file:
    file.write("Hello Python")

# Get file size
size = os.path.getsize("example.txt")
print("File Size:", size, "bytes")

#---------------------------------------------------------------------------
# 6) Convert the string "Feb 25 2020 4:20PM" into a Python datetime object
from datetime import datetime

date_str = "Feb 25 2020 4:20PM"
dt = datetime.strptime(date_str, "%b %d %Y %I:%M%p")

print(dt)



#---------------------------------------------------------------------------
# 7) Subtract 7 days from the date 2025-02-25 and print the result.

from datetime import datetime, timedelta

date_obj = datetime(2025, 2, 25)
new_date = date_obj - timedelta(days=7)

print("New date:", new_date.date())


#---------------------------------------------------------------------------
# 8) Format the date 2020-02-25 as "Tuesday 25 February 2020"

from datetime import datetime

date_obj = datetime(2020, 2, 25)
formatted_date = date_obj.strftime("%A %d %B %Y")

print(formatted_date)
