# 1. Find max and min values in a list
nums = [1, 2, 3, 4, 5]
max_value = max(nums)
min_value = min(nums)
print(f"list: {nums}")
print(f"Max value: {max_value}, Min value : {min_value}")

#----------------------------------------------------------------------------

# 2. Merge two lists
list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]
merged_list = list1 + list2
print(f"list 1: {list1}")
print(f"list 2: {list2}")
print(f"merged list: {merged_list}")

#----------------------------------------------------------------------------

# 3. Count occurrences of a value in a list
list1 = [1, 3, 4, 5, 2, 1, 3, 9, 3]
count_of_3 = list1.count(3)
print(f"list: {list1}")
print(f"ocurrence of 3: {count_of_3}")


#----------------------------------------------------------------------------

# 4. Sort the list
list1 = [1, 3, 4, 5, 2, 1, 3, 9, 3]
sorted_list = sorted(list1)
print(f"list: {list1}")
print(f"sorted list: {sorted_list}")

#----------------------------------------------------------------------------

# 5. Set: Add an element
list1 = {1, 2, 3, 4, 5}
list1.add(6)
print(f"list: {list1}")
print(f"6 added: {list1}")

#----------------------------------------------------------------------------

# 6. Set: Remove an element
list1 = {1, 2, 3, 4, 5}
list1.remove(3)
print(f"list: {list1}")
print(f"3 removed: {list1}")


#----------------------------------------------------------------------------

# 7. Set: Find intersection
set1 = {1, 2, 3}
set2 = {3, 4, 5}
intersection_set = set1 & set2
print(f"intersection set: {intersection_set}")


#----------------------------------------------------------------------------

# 8. Tuple: Count occurrences
fruits = ('apple', 'banana', 'apple', 'cherry')
apple_count = fruits.count('apple')
print(f"occurrence of apples: {apple_count}")

#----------------------------------------------------------------------------

# 9. Tuple: Concatenate
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
concatenated_tuple = tuple1 + tuple2
print(f"tuple1: {tuple1}")
print(f"tuple2: {tuple1}")
print(f"concatenated tuple: {concatenated_tuple}")


#----------------------------------------------------------------------------

# 10. Dictionary: Access a value
person_access = {"name": "Alice", "age": 30, "city": "New York"}
age_value = person_access["age"]
print(f"age: {age_value}")


#----------------------------------------------------------------------------

# 11. Dictionary: Add a new key/value
person_add = {"name": "Alice", "age": 30, "city": "New York"}
person_add["gender"] = "M"
print(f"person object after gender addition: {person_add}")

#----------------------------------------------------------------------------

# 12. Dictionary: Remove a key
person_remove = {"name": "Alice", "age": 30, "city": "New York"}
person_remove.pop("city")
print(f"person object after city removal: {person_remove}")

#----------------------------------------------------------------------------

# 13. Dictionary: Merge two dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged_dict = dict1 | dict2
print(f"merged dictionary: {merged_dict}")
