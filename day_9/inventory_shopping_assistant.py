inventory = ["apples", "bananas", "milk", "eggs"]
quantities = [10, 5, 2, 12]

# Display inventory
if not inventory:
    print("Inventory is empty.")
else:
    for i in range(len(inventory)):
        print(f"- {inventory[i]}: {quantities[i]}")

# Add items to shopping list
shopping_list = []
while True:
    item = input("Enter item to add (or 'done'): ")
    if item.lower() == "done":
        break
    
    if item in inventory:  # Check if item is in inventory
        shopping_list.append(item)  # Add to shopping list
        print(f"{item} added to shopping list.")

    else:
        print(f"{item} not found in inventory.")
        
# Display shopping list (optional)
if shopping_list:
    print("\nShopping List:")
    for item in shopping_list:
        print(f"- {item}")