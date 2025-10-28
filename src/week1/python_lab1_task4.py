# Author: Hazal Guc
# Student ID: 231ADB264
# Task 4 – Text-based Arithmetic Analyzer

def count_characters(text):
    """Count non-space characters in a string."""
    return len([ch for ch in text if not ch.isspace()])

def count_words(text):
    """Count number of words in a string."""
    return len(text.split())

def extract_numbers(text):
    """Extract all numbers from text and return as list of floats."""
    numbers = []
    for part in text.split():
        if part.replace('.', '', 1).isdigit():
            numbers.append(float(part))
    return numbers

def analyze_text(text):
    """Analyze text and return summary as a dictionary."""
    chars = count_characters(text)
    words = count_words(text)
    nums = extract_numbers(text)
    total = sum(nums)
    avg = total / len(nums) if nums else 0
    return {
        "characters": chars,
        "words": words,
        "numbers_found": len(nums),
        "sum": total,
        "average": avg
    }

if __name__ == "__main__":
    text = input("Enter a text with numbers: ")
    result = analyze_text(text)
    print("\n--- Text Analysis Summary ---")
    print(f"Non-space characters: {result['characters']}")
    print(f"Word count: {result['words']}")
    print(f"Numbers found: {result['numbers_found']}")
    print(f"Sum of numbers: {result['sum']}")
    print(f"Average of numbers: {result['average']:.2f}")
