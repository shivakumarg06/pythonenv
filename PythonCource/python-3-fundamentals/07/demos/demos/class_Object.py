# Example - Simple method of class...


class Robot_Dog:
    def __init__(self, name_val, breed_val):
        self.name = name_val
        self.breed = breed_val


# Main Program
my_dog = Robot_Dog("Spot", "Chihuaha")
print(my_dog.name)
print(my_dog.breed)

# Example - we create a class method just like a function. Except a method has self as the paramter.


class Robot_Dog:
    def __init__(self, name_val, breed_val):
        self.name = name_val
        self.breed = breed_val

    def bark(self):
        print("Woof Woof!")


# Main Program
my_dog = Robot_Dog("Spot", "Chihuaha")
print(my_dog.name)
print(my_dog.breed)
my_dog.bark()  # objectName, dot, methodName
