try:
    with open("poem.txt", "r") as file:
        content = file.read()
        print("\nPoem content:\n", content)
except FileNotFoundError:
    print("poem.txt not found.")