#1. Convert the following values to the specified types and print the resul
#a. Convert 3.75 to an integer
intVal = int(3.75)
print("Integer value: ", intVal)

#b. Convert "123" to a float
floatVal = float("123")
print("Float value: ", floatVal)

#c. Convert 0 to a boolean
boolVal = bool(0)
print("Boolean value: ", boolVal)

#d. Convert False to a string
strValue = str(False)
print("String value: ", strValue)

#----------------------------------------------------------------------------


#2. Convert all characters in the string to uppercase. 
x = "hello"
print(x.upper())

#----------------------------------------------------------------------------



#3. Given x = 5 and y = 3.14, calculate z = x + y and determine the data type of z. And convert it to integer.
x=5
y=3.14
z=x+y
print("type of z: ", type(z))

z_int = int(z)
print("int value of z: ", z_int)

#----------------------------------------------------------------------------


#4. Given the string s = 'hello', perform the following operations:

s = 'hello'
#a. Convert the string to uppercase.
s_upper = s.upper()
print("hello in uppercase: ", s_upper)

#b. Replace 'e' with 'a'
s_replaced = s.replace('e', 'a')
print("Replaced 'e' with 'a': ", s_replaced)

#c. Check if the string starts with 'he'
starts_with_he = s.startswith('he')
print("Starts with 'he': ",starts_with_he)

#d. Check if the string ends with 'lo'
ends_with_lo = s.endswith('lo')
print("Ends with 'lo': ", ends_with_lo)

