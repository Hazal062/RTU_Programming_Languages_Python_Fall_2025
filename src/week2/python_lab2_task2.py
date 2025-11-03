# Student name: Hazal Guc
# Student ID: 231ADB264

"""
Lab 3.2 🧮 Comprehensions and Transformations

Goals:
- Practice list, set, and dictionary comprehensions.
- Transform and filter data concisely.

Instructions:
Given the list:
    numbers = [3, 8, -2, 7, 0, -5, 10]

1. Create a list `squares` with the square of each number.
2. Create a list `positives` containing only positive numbers.
3. Create a set `even_squares` of the squares of even numbers.
4. Create a dictionary `cubes` mapping each number to its cube.
5. Print all results.
"""

# Fill in your own numbers or generate 10 random integers
numbers = [3, 8, -2, 7, 0, -5, 10]

# TODO: Implement comprehensions
squares = [n ** 2 for n in numbers]
positives = [n for n in numbers if n > 0]
even_squares = {n ** 2 for n in numbers if n % 2 == 0}
cubes = {n: n ** 3 for n in numbers}

# TODO: Print results
print("Squares:", squares)
print("Positives:", positives)
print("Even squares:", even_squares)
print("Cubes:", cubes)
