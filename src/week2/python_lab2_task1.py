# Student name: Hazal Guc
# Student ID: 231ADB264

"""
Lab 3.1 🧊 Simple Datasets and Aggregates

Goals:
- Create and manipulate Python lists and dictionaries.
- Compute aggregates such as sum, average, max, and min.

Instructions:
1. Create a list `temperatures` with daily temperatures for one week.
2. Create a dictionary `city_population` with at least 5 cities and their populations.
3. Compute:
   - The average temperature.
   - The maximum and minimum population.
   - The total population of all cities.
4. Print your results in a clear, formatted way.
"""

# TODO: Create the datasets – up to you to fill in the data
temperatures = [12, 14, 11, 13, 15, 16, 14]
city_population = {
    "Riga": 605802,
    "Vilnius": 587581,
    "Tallinn": 437619,
    "Liepaja": 68238,
    "Daugavpils": 82274,
}

# TODO: Compute aggregates
average_temperature = sum(temperatures) / len(temperatures)
largest_city = max(city_population.keys(), key=lambda x: city_population[x])
largest_population = city_population[largest_city]
total_population = sum(city_population.values())

# TODO: Print results
print("Average temperature:", average_temperature)
print("Largest city:", largest_city, "-", largest_population)
print("Total population:", total_population)
