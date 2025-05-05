filename = input("Enter the filename: ")

try:
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in reversed(lines):
            print(line.strip())
except FileNotFoundError:
    print("File not found.")