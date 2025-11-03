
"""
Lab 3.4 – Functional Tools Practice

Goals:
- Learn to apply functional tools (`map`, `filter`, `zip`).
- Compare functional style to list comprehensions.

Instructions:
Given:
    prices = [12.5, 9.9, 15.0, 22.3, 5.0]
    quantities = [2, 5, 1, 3, 4]

1. Use map() and a lambda to compute total cost for each item (price * quantity).
2. Use filter() to keep only totals above 30.
3. Use zip() to pair prices with quantities.
4. Try doing the same using list comprehensions for comparison.
"""

prices = [12.5, 9.9, 15.0, 22.3, 5.0]
quantities = [2, 5, 1, 3, 4]

# TODO: Compute totals using map()
totals = []

# TODO: Filter totals above 30
high_totals = []

# TODO: Pair prices and quantities with zip()
pairs = []

# TODO: Repeat using list comprehensions
totals_comp = []
high_totals_comp = []

# TODO: Print results
print("Totals:", totals)
print("Totals > 30:", high_totals)
print("Price-quantity pairs:", pairs)
print("Totals (comprehension):", totals_comp)
print("Totals > 30 (comprehension):", high_totals_comp)
