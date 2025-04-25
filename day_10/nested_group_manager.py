inventory = {
    "Fruits": {"apple": 10, "banana": 6},
    "Dairy": {"milk": 3, "cheese": 2},
    "Bakery": {"bread": 5, "bun": 8}
}

# Print categories and total items
for category, items in inventory.items():
    total_items = sum(items.values())
    print(f"{category} (Total items: {total_items}):")
    for item, quantity in items.items():
        print(f"  {item}: {quantity}")
    print()

# Allow stock updates
while True:
    update_category = input("Enter category to update (or type 'done' to finish): ")
    if update_category.lower() == 'done':
        break
    if update_category in inventory:
        update_item = input("Enter item to update: ")
        if update_item in inventory[update_category]:
            quantity = int(input("Enter quantity to add: "))
            inventory[update_category][update_item] += quantity
            print(f"Updated {update_item} in {update_category}. New total: {inventory[update_category][update_item]}")
        else:
            print(f"{update_item} not found in {update_category}.")
    else:
        print(f"{update_category} not found.")