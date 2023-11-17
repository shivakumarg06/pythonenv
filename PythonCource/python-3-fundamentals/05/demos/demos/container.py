# Two list merger in container
# Combining Lists and Dictionary

# Lists
# Let's say we have three separated menu lists: Breakfast, Lunch, Dinner...

breakfast = ["Egg Sandwich", "Bagel", "Coffee"]

lunch = ["BLT", "PB&J", "Turkey Sandwich"]

dinner = ["Soup", "Salad", "Spaghetti", "Taco"]

# how would we combine these into one lists?

menus = [
    ["Egg Sandwich", "Bagel", "Coffee"],
    ["BLT", "PB&J", "Turkey Sandwich"],
    ["Soup", "Salad", "Spaghetti", "Taco"],
]

print("Breakfast Menu:\t", menus[0])
print("Lunch Menu:\t", menus[0])
print("Dinner Menu:\t", menus[0])

# output from inner list
print(menus[0])
print(menus[0][1])

# Dictionary of Lists
menus = {
    "Breakfast": ["Egg Sandwich", "Bagel", "Coffee"],
    "Lunch": ["BLT", "PB&J", "Turkey Sandwich"],
    "Dinner": ["Soup", "Salad", "Spaghetti", "Taco"],
}

print("Breakfast Menu:\t", menus["Breakfast"])
print("Lunch Menu:\t", menus["Lunch"])
print("Dinner Menu:\t", menus["Dinner"])

# Dictionary with Loops for better doing
menus = {
    "Breakfast": ["Egg Sandwich", "Bagel", "Coffee"],
    "Lunch": ["BLT", "PB&J", "Turkey Sandwich"],
    "Dinner": ["Soup", "Salad", "Spaghetti", "Taco"],
}

for name, menu in menus.items():
    print(
        name, ":", menu
    )  # Now the loos has access to both the key and the value here.

# with Represent Objects
# lets say we have a person and we want to represent their attributes, such as their name, age, and city they're from.

person = {"name": "Sarah Smith", "city": "Orlando", "age": "100"}
print(person.get("name"), "is", person.get("age"), "years old.")
