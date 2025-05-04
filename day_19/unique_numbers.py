numbers = []

for _ in range(10):
    num = int(input("Enter a number: "))
    numbers.append(num)

unique = set(numbers)
print("\nUnique numbers:", unique)
