input_string = input("Enter a word or number: ")

# Clean the string: Remove spaces, punctuation, and convert to lower case
cleaned_string = ''.join(char.lower() for char in input_string if char.isalnum())
word_count = len(input_string.split())

# Check if cleaned string is equal to its reverse
is_palindrome = cleaned_string == cleaned_string[::-1]

if is_palindrome:
    print(f"Yes, '{input_string}' is a palindrome with {word_count} word(s).")
else:
    print(f"Nope, '{input_string}' is not a palindrome and has {word_count} word(s).")