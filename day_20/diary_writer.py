entry = input("Write your diary entry: ")

with open("diary.txt", "a") as file:
    file.write(entry + "\n")

print("Entry saved to diary.txt!")