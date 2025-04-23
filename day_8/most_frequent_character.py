# Find the Most Frequent Character

sentence = "helloooooo"
char_counts = {}
for char in sentence:
    char_counts[char] = char_counts.get(char, 0) + 1
max_count = 0
max_char = ''
for char, count in char_counts.items():
    if count > max_count:
        max_count = count
        max_char = char
print(f"{max_char} occurred {max_count} times") # Output: o occurred 6 times

