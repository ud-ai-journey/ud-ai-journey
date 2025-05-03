word = input("Enter a word or phrase: ").lower().replace(" ", "")

if word == word[::-1]:
    print("It's a palindrome!")
else:
    print("It's not a palindrome.")