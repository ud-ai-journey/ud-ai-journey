sentence = input("Enter a sentence: ")
vowels = "aeiouAEIOU"

for char in sentence:
    if char in vowels:
        print(char)