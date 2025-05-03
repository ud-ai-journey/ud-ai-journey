print("Enter 5 grocery items:")
grocery_items = []

for i in range(5):
    item = input(f"Item {i+1}: ")
    grocery_items.append(item)

print("\nYour grocery list:", grocery_items)

# Display sorted list
sorted_list = sorted(grocery_items)
print("\nSorted grocery list:", sorted_list)

# Update an item
update_index = int(input("\nEnter the number (1-5) of the item to update: ")) - 1
if 0 <= update_index < len(grocery_items):
    new_item = input("Enter the new item: ")
    grocery_items[update_index] = new_item
    print("Updated list:", grocery_items)
else:
    print("Invalid index. No update performed.")

# Remove an item
remove_item = input("\nEnter an item to remove: ")
if remove_item in grocery_items:
    grocery_items.remove(remove_item)
    print("List after removal:", grocery_items)
else:
    print(f"'{remove_item}' not found in the list.")