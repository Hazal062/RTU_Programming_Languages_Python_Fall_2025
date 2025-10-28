# Author: Hazal Guc
# Student ID: 231ADB264
# Task 2 – Greeting Function with String Manipulation

def greet_user(name):
    """Return a greeting message after cleaning and capitalizing the name."""
    name = name.strip().capitalize()
    return f"Hello, {name}! Welcome to Python!"

if __name__ == "__main__":
    name_input = input("Enter your name: ")
    message = greet_user(name_input)
    print(message)
