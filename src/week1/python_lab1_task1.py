# Author: Hazal Guc
# Student ID: 231ADB264
# Task 1 – Simple Function with Arithmetic

import math

def circle_area(radius):
    """Return the area of a circle given its radius."""
    return math.pi * (radius ** 2)

if __name__ == "__main__":
    radius = float(input("Enter radius: "))
    area = circle_area(radius)
    print(f"Area of the circle: {area:.2f}")
