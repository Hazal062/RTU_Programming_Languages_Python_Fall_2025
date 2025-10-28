# Author: Hazal Guc
# Student ID: 231ADB264
# Task 3 – Function with Combined Logic

def analyze_sentence(text):
    """Return length, word count, and whether 'Python' appears in text."""
    length = len(text)
    words = text.split()
    contains_python = "python" in text.lower()
    return length, len(words), contains_python

if __name__ == "__main__":
    sentence = input("Enter a sentence: ")
    length, word_count, has_python = analyze_sentence(sentence)
    print(f"Total characters: {length}")
    print(f"Word count: {word_count}")
    print(f"Contains 'Python': {has_python}")
