# 1. Convert numeric strings to integers
print("--- 1. Convert Strings to Integers ---")
strings = ["1", "2", "3", "4", "5"]
integers = [int(s) for s in strings]
print(f"Original: {strings}")
print(f"Integers: {integers}")

#----------------------------------------------------------------------------

# 2. Extract integers greater than 10
numbers = [1, 5, 13, 4, 16, 7]
filtered_numbers = [n for n in numbers if n > 10]
print(f"Original: {numbers}")
print(f"Filtered: {filtered_numbers}")

#----------------------------------------------------------------------------

# 3. Create a list of squares for numbers from 1 to 5
squares = [x**2 for x in range(1, 6)]
print(f"Squares: {squares}")

#----------------------------------------------------------------------------

# 4. Convert a 2D list into a 1D list (Flattening)
matrix = [[1, 3, 4], [23, 32, 56, 74], [-2, -6, -9]]
flat_list = [element for sublist in matrix for element in sublist]
print(f"Original 2D: {matrix}")
print(f"Flattened 1D: {flat_list}")

#----------------------------------------------------------------------------

# 5. Create a dictionary from two lists (keys and values)
keys = ['a', 'b', 'c']
values = [1, 2, 3]
new_dict = {k: v for k, v in zip(keys, values)}
print(f"Keys: {keys}, Values: {values}")
print(f"Dictionary: {new_dict}")

#----------------------------------------------------------------------------

# 6. Filter a dictionary based on values (scores > 80)
scores = {'Alice': 85, 'Bob': 70, 'Charlie': 90}
high_scorers = {name: score for name, score in scores.items() if score > 80}
print(f"Original Scores: {scores}")
print(f"High Scorers (>80): {high_scorers}")