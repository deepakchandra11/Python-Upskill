#1. Ask the user for their name and greet them.
name = input("Please enter your name: ")
print(f"Hello, {name}!")

#----------------------------------------------------------------------------

#2. Perform basic arithmetic operations based on user input.
num1_str = input("Enter the first number: ")
num2_str = input("Enter the second number: ")

# Convert inputs to float to handle both integers and decimals
num1 = float(num1_str)
num2 = float(num2_str)

# Calculations
sum_result = num1 + num2
product_result = num1 * num2
division_result = num1 / num2

print(f"Sum: {sum_result}")
print(f"Multiplication: {product_result}")
print(f"Division: {division_result}")

#------------------------------------------------------------------------------

# 3. Split comma-separated names into a list.
names_input = input("Enter names separated by commas (e.g., Alice,Bob,Charlie): ")
names_list = [name.strip() for name in names_input.split(',')]
print(f"Input string: '{names_input}'")
print(f"List of names: {names_list}")

#------------------------------------------------------------------------------

# 4. Check voting eligibility based on age.
age_input = input("Please enter your age: ")
age = int(age_input)

VOTING_AGE = 18

print(f"Your age is: {age}")
if age >= VOTING_AGE:
    print("You are **eligible** to vote!")
else:
    years_left = VOTING_AGE - age
    print(f"You are currently **not eligible** to vote. You can vote in {years_left} year(s).")

#------------------------------------------------------------------------------

# 5. Using f-string print output for only up to 2 decimal places.
x = 3.14159
print(f"Original value: {x}")
print(f"Formatted output: {x:.2f}")