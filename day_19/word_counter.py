sentence = input("Enter a sentence: ")
words = sentence.split()
counter = {}

for word in words:
    counter[word] = counter.get(word, 0) + 1

print("\nWord Frequencies:")
for word, count in counter.items():
    print(f"{word}: {count}")