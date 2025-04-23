# Check for Anagram

word1 = "listen"
word2 = "silent"
sorted_word1 = sorted(word1)
sorted_word2 = sorted(word2)
if sorted_word1 == sorted_word2:
    print("Yes, it's an anagram!")
else:
    print("No, it's not an anagram.") # Output: Yes, it's an anagram!

