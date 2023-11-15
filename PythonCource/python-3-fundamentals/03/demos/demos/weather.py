# this scrit helps to understand if statement and Condition Statement 

# Example 2 Comparision 
temp = 95 
temp == 95 # value should be TRUE 

temp < 95 # Value should be FALSE

# Exmaple 3 
temperature = 95

if temperature > 80:
    print("It's to hot!")
    print("Stay Inside!")

# Exmaple 4 - Statement is false so it should give have a good day output
temperature = 75

if temperature > 80:
    print("It's to hot!")
    print("Stay Inside!")
print("Have a good day!")

# Exmaple 5 - 
temperature = 50

if temperature > 80:
    print("It's to hot!")
    print("Stay Inside!")

elif temperature < 60:
    print("It's to cold!")
    print("Stay Inside!")

else: 
    print("Enjo the outdoors!")

# Exmaple 5 - runing same output multiple times, making it operator conditions
# false or false

temperature = 75
if temperature > 80 or temperature <60:
    print("Stay Inside!")

else: 
    print("Enjo the outdoors!")

# false or true
    temperature = 50
if temperature > 80 or temperature <60:
    print("Stay Inside!")

else: 
    print("Enjo the outdoors!")
    
# Eample 6 
temperature = 75 
forecast = "rainy"

# true and flase = false 
if temperature < 80 and forecast != "rainy":
    print("Go outside!")
else:
    print("Stay inside!")

# true and true = true
forecast = "Sunny"
if temperature < 80 and forecast != "rainy":
    print("Go outside!")
else:
    print("Stay inside!")

# Example 
forecast = "rainy"

if not forecast == "rainy":
    print("Go outside!")
else:
    print("Stay inside!")

# Example 
raining = True 

if raining:
    print("Stay inside!")

# not True
if not raining:
    print("Go outside!")
else:
    print("Stay inside!")
