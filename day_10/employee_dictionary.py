employees = [
    {"id": 101, "name": "John", "role": "Manager"},
    {"id": 102, "name": "Alice", "role": "Developer"},
    {"id": 103, "name": "Bob", "role": "Designer"}
]

# Allow searching employees by name or ID
while True:
    search_query = input("Enter employee ID or Name to search (or type 'exit' to quit): ")
    if search_query.lower() == 'exit':
        break

    found_employee = None
    for employee in employees:
        if str(employee["id"]) == search_query or employee["name"].lower() == search_query.lower():
            found_employee = employee
            break

    if found_employee:
        print(f"Found Employee: ID: {found_employee['id']}, Name: {found_employee['name']}, Role: {found_employee['role']}")
    else:
        print("Employee not found.")