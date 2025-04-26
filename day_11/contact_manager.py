import os
import shutil  # For the backup functionality

# Define the directory and file paths for contacts
BASE_DIR = 'day_11'
CONTACTS_FILE = os.path.join(BASE_DIR, 'contacts.txt')
BACKUP_FILE = os.path.join(BASE_DIR, 'contacts_backup.txt')

# Ensure the directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Load contacts from a file if it exists
contacts = {}

if os.path.exists(CONTACTS_FILE):
    with open(CONTACTS_FILE, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Check for non-empty lines
                try:
                    name, phone, email = line.split(',')
                    contacts[name.lower()] = {'phone': phone, 'email': email}
                except ValueError:
                    print(f"Warning: Skipped corrupted entry: {line}")

while True:
    print("\nContact Management System")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Display Contacts")
    print("6. Exit")

    choice = input("Choose an option (1-6): ")

    if choice == '1':
        name = input("Enter contact name: ")
        phone = input("Enter contact phone (10 digits): ")
        
        while not phone.isdigit() or len(phone) != 10:
            print("Invalid phone number. Please enter a 10-digit number.")
            phone = input("Enter contact phone (10 digits): ")

        email = input("Enter contact email: ")
        contacts[name.lower()] = {'phone': phone, 'email': email}
        print(f"Added contact: {name}")

    elif choice == '2':
        search_name = input("Enter name to search: ")
        found = False
        for name in contacts:
            if name == search_name.lower():
                found = True
                contact = contacts[name]
                print(f"Found contact: {name.title()} - {contact['phone']} - {contact['email']}")
                break
        if not found:
            print("Contact not found.")

    elif choice == '3':
        search_name = input("Enter name to update: ")
        if search_name.lower() in contacts:
            new_phone = input("Enter new phone (or leave blank to keep current): ")
            if new_phone:
                while not new_phone.isdigit() or len(new_phone) != 10:
                    print("Invalid phone number. Please enter a 10-digit number.")
                    new_phone = input("Enter new phone (or leave blank to keep current): ")
                contacts[search_name.lower()]['phone'] = new_phone
            
            new_email = input("Enter new email (or leave blank to keep current): ")
            if new_email:
                contacts[search_name.lower()]['email'] = new_email
            
            print(f"Updated contact: {search_name.title()}")
        else:
            print("Contact not found.")

    elif choice == '4':
        delete_name = input("Enter name to delete: ")
        if delete_name.lower() in contacts:
            del contacts[delete_name.lower()]
            print(f"Deleted contact: {delete_name.title()}")
        else:
            print("Contact not found.")

    elif choice == '5':
        print("Contacts List:")
        if contacts:
            # Sort contacts alphabetically by name before displaying
            for name in sorted(contacts):
                info = contacts[name]
                print(f"{name.title()} - {info['phone']} - {info['email']}")
        else:
            print("No contacts found.")

    elif choice == '6':
        # Create a backup of the existing contacts.txt before saving
        if os.path.exists(CONTACTS_FILE):
            shutil.copy(CONTACTS_FILE, BACKUP_FILE)
        
        # Save contacts to FILE in the specified folder on exit
        with open(CONTACTS_FILE, 'w') as file:
            for name, info in contacts.items():
                file.write(f"{name},{info['phone']},{info['email']}\n")
        print("Contacts have been saved. Exiting Contact Manager.")
        break

    else:
        print("Invalid option. Please choose again.")