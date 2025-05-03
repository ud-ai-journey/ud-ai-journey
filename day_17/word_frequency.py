sentence = input("Enter a sentence: ").lower()
words = sentence.split()

frequency = {}

for word in words:
    # Remove punctuation if necessary
    word = word.strip('.,!?";:\'()[]{}')
    if word:
        frequency[word] = frequency.get(word, 0) + 1

print("Word Frequencies:")
for word, count in frequency.items():
    print(f"{word}: {count}")