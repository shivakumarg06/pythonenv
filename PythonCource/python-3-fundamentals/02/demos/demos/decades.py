age = int(input("How old are you?\n"))

decades = age // 10
years = age % 10

print("You are " + str(decades) + 
      " decades and " + str(years) + " years old.")

# Example 2  Unspported oprend due to string input
age = input("How old are you?\n")

decades = age/10 
print(age)

# Example 3 fixed the string error by passing int input on the age, 
age = int(input("How old are you?\n"))

decades = age/10 
print("You are " + decades + "decades old.") # it will throw the error, due to value is flot, need to make it string
print("You are " + str(decades) + "decades old.")

# Example 4 instend of float value try devision, Integer devision modulers  
age = int(input("How old are you?\n"))

decades = age // 10
years = age % 10 
print("You are " + str(decades) + "decades and " + str(years) +  " years old.")