# Count Vowels and Consonants

sentence = "The quick brown fox"
vowels = "aeiouAEIOU"
vowel_count = 0
consonant_count = 0
for char in sentence:
    if char in vowels:
        vowel_count += 1
    elif char.isalpha():
        consonant_count += 1
print(f"Vowels: {vowel_count}, Consonants: {consonant_count}") # Output: Vowels: 5, Consonants: 11


