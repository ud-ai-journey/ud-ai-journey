my_list = [1, 2, 2, 3, 4, 4, 5, 5, 5, 6]

seen = set()
duplicates = []
seen_duplicates = set()  # Crucial for handling multiple duplicates

for item in my_list:
    if item in seen:
        if item not in seen_duplicates:
            duplicates.append(item)
            seen_duplicates.add(item)
    else:
        seen.add(item)

if duplicates:
  print("Duplicate elements:", duplicates)
else:
  print("No duplicate elements found.")

