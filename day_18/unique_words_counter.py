paragraph = input("Enter a paragraph: ")

words = paragraph.split()

unique_words = set(words)

print(f"\nNumber of unique words: {len(unique_words)}")
print("Unique words:", unique_words)