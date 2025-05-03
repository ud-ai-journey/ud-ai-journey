message = input("Enter your message: ")

replacements = {
    'a': '@',
    'e': '3',
    'i': '!',
    'o': '0',
    'u': '^'
}

encoded_message = ""
for char in message:
    lower_char = char.lower()
    if lower_char in replacements:
        # Preserve original case if desired, or just replace all
        encoded_message += replacements[lower_char]
    else:
        encoded_message += char

print("Encoded Message:", encoded_message)