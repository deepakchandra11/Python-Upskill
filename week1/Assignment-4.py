# 1. Check if a number is even or odd (using a simple input/if/else structure)
num = int(input("Enter an integer to check if it's even or odd: "))
if num % 2 == 0:
    print(f"The number {num} is even.")
else:
    print(f"The number {num} is odd.")

#----------------------------------------------------------------------------

# 2. Reverse a string using a for loop and check if it is a palindrome.
strings_to_check = ["civic", "hello"]

for s in strings_to_check:
    reversed_s = ""
    for char in s:
        reversed_s = char + reversed_s

    is_palindrome = s == reversed_s
    print(f"String: '{s}', Reversed: '{reversed_s}'")
    if is_palindrome:
        print(f"  -> It is a palindrome.")
    else:
        print(f"  -> It is NOT a palindrome.")

#----------------------------------------------------------------------------

# 3. Generate the first N numbers of the Fibonacci sequence.
N = int(input("Enter the number of Fibonacci terms (N) to generate: "))
a, b = 0, 1
fib_sequence = [a]
for _ in range(N - 1):
    fib_sequence.append(b)
    a, b = b, a + b
print(f"First {N} Fibonacci numbers: {fib_sequence}")

#----------------------------------------------------------------------------

# 4. Find two values from the list that sum to 9.
num_list = [1, 2, 3, 4, 5]
target_sum = 9
found_pair = None

# Nested loops to check every pair (i, j) where i < j
for i in range(len(num_list)):
    for j in range(i + 1, len(num_list)): # Start j after i to avoid duplicates
        if num_list[i] + num_list[j] == target_sum:
            found_pair = [num_list[i], num_list[j]]
            break # Exit the inner loop once a pair is found
    if found_pair:
        break # Exit the outer loop once a pair is found

print(f"List: {num_list}")
if found_pair:
    print(f"Two values that add up to {target_sum}: {found_pair}")
else:
    print("No such pair found.")

#----------------------------------------------------------------------------

# 5. Print all even numbers between 1 and 20 using a while loop.
i = 2
even_numbers = []
while i <= 20:
    even_numbers.append(i)
    i += 2 # Increment by 2 to get the next even number

print(f"Even numbers between 1 and 20: {even_numbers}")

#----------------------------------------------------------------------------

# 6. Find the first occurrence of a number and stop searching.
numbers = [10, 20, 30, 40, 50]
search_for = 30
position = -1 # Default if not found

for index, number in enumerate(numbers):
    if number == search_for:
        position = index
        print(f"Found {search_for} at index **{position}**.")
        break
    print(f"Checking index {index}...") 
if position == -1:
    print(f"{search_for} not found in the list.")

#----------------------------------------------------------------------------

# 7. Print only the odd numbers from 1 to 10 using continue.
odd_numbers = []
for i in range(1, 11):
    if i % 2 == 0:
        continue
    odd_numbers.append(i)

print(f"Odd numbers from 1 to 10: {odd_numbers}")

#----------------------------------------------------------------------------

# 8. What will be the output for the pass statement example?
for i in range(5):
    if i == 3:
        pass 
    print(i)

#----------------------------------------------------------------------------

# 9. Day of the week checker (Weekday or Weekend).
day = input("Enter a day of the week (e.g., Monday, Sunday): ").strip().lower()

match day:
    case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
        result = "It's a weekday, need to go to work"
    case "saturday" | "sunday":
        result = "Hurray, It's the weekend!"
    case _:
        result = "Invalid input. Please enter a valid day of the week."

print(f"Input: {day.capitalize()}")
print(result)