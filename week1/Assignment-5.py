# 1. Calculate the area of a rectangle with a default width

def calculate_area(length: float, width: float = 10) -> float:
    return length * width

#----------------------------------------------------------------------------

# 2. Recursive function to compute the factorial of a non-negative integer

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

#----------------------------------------------------------------------------

# 3. Function to reverse a string

def reverse_string(s: str) -> str:
    return s[::-1]

#----------------------------------------------------------------------------

# 4. Function to sum all numbers in two different lists

def sum_list_numbers(list1, list2):
    return sum(list1) + sum(list2)

#----------------------------------------------------------------------------

# 5. Function to get distinct and sorted elements from a list

def get_distinct_and_sorted(input_list: list) -> list:
    
    unique_elements = set(input_list)
    return sorted(list(unique_elements))

#----------------------------------------------------------------------------

print("--- 1. Rectangle Area ---")
print(f"Area (length=5, default width=10): {calculate_area(5)}")

print("\n--- 2. Factorial (Recursive) ---")
print(f"Factorial of 5 (5!): {factorial(5)}")

print("\n--- 3. Reverse String ---")
original_string = "python"
reversed_str = reverse_string(original_string)
print(f"Original: '{original_string}'")
print(f"Reversed: '{reversed_str}'")

print("\n--- 4. Sum List Numbers ---")
list_a = [8, 2, 3, 0, 7]
list_b = [3, -2, 5, 1]
print(f"List A & B Sum: {sum_list_numbers(list_a, list_b)}")

print("\n--- 5. Distinct and Sorted Elements ---")
list_c = [4, 1, 2, 3, 3, 1, 3, 4, 5, 1, 7]
distinct_sorted = get_distinct_and_sorted(list_c)
print(f"Original List: {list_c}")
print(f"Distinct & Sorted: {distinct_sorted}")