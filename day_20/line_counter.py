filename = input("Enter the file name: ")

try:
    with open(filename, "r") as file:
        count = len(file.readlines())
        print(f"The file has {count} lines.")
except FileNotFoundError:
    print("File not found.")