# String Toolkit Mini Program

# Prompt user for an input string
input_string = input("Enter a string: ")

while True:
    # Display the menu
    print("\nString Toolkit Menu:")
    print("1. Count letters")
    print("2. Reverse string")
    print("3. Replace a word")
    print("4. Check for palindrome")
    print("5. Exit")

    # Get the user's choice
    choice = input("Choose an option (1-5): ")

    if choice == '1':
        # Count letters
        letter_count = sum(c.isalpha() for c in input_string)
        print(f"Total letters: {letter_count}")

    elif choice == '2':
        # Reverse string
        reversed_string = input_string[::-1]
        print(f"Reversed string: {reversed_string}")

    elif choice == '3':
        # Replace a word
        old_word = input("Enter the word to replace: ")
        new_word = input("Enter the new word: ")
        updated_string = input_string.replace(old_word, new_word)
        print(f"Updated string: {updated_string}")

    elif choice == '4':
        # Check for palindrome
        is_palindrome = input_string == input_string[::-1]
        if is_palindrome:
            print("The string is a palindrome.")
        else:
            print("The string is not a palindrome.")

    elif choice == '5':
        # Exit the program
        print("Exiting the String Toolkit. Goodbye!")
        break

    else:
        print("Invalid option, please try again.")