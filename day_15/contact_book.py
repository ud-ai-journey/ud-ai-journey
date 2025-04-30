import json
import os
import re
import csv

# File paths
CONTACTS_FILE = 'contacts.json'
BACKUP_FILE = 'contacts_backup.json'
CSV_FILE = 'contacts_export.csv'

# Load contacts
if not os.path.exists(CONTACTS_FILE):
    contacts = []
else:
    with open(CONTACTS_FILE, 'r') as f:
        try:
            contacts = json.load(f)
            if not isinstance(contacts, list):
                contacts = []
        except json.JSONDecodeError:
            contacts = []

# Validation regex
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# Helper validation functions
def validate_email(email):
    return re.match(email_pattern, email) is not None

def validate_phone(phone):
    return phone.isdigit() and 7 <= len(phone) <= 15

while True:
    print("\n--- Contact Book Manager ---")
    print("1. Add New Contact")
    print("2. Search Contacts")
    print("3. Delete Contact")
    print("4. Update Contact")
    print("5. Export Contacts to CSV")
    print("6. Backup Contacts")
    print("7. Exit")
    choice = input("Select an option (1-7): ").strip()

    if choice == '1':
        # Add Contact
        name = input("Enter Name: ").strip()
        phone = input("Enter Phone (digits only): ").strip()
        email = input("Enter Email: ").strip()
        address = input("Enter Address: ").strip()

        # Validate inputs
        if not validate_phone(phone):
            print("Invalid phone number. Must be digits only and length between 7 and 15.")
            continue
        if not validate_email(email):
            print("Invalid email format.")
            continue

        # Check duplicates
        duplicate = False
        for contact in contacts:
            if contact['phone'] == phone:
                print("A contact with this phone number already exists.")
                duplicate = True
                break
            if contact['email'].lower() == email.lower():
                print("A contact with this email already exists.")
                duplicate = True
                break
        if duplicate:
            continue

        # Add contact
        contacts.append({
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        })

        # Save
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(contacts, f, indent=4)
        print("Contact added successfully.")

    elif choice == '2':
        # Search Contacts (partial match on name, phone, email)
        query = input("Enter Name, Phone, or Email to search: ").strip().lower()
        results = []
        for contact in contacts:
            if (query in contact['name'].lower() or
                query in contact['phone'] or
                query in contact['email'].lower()):
                results.append(contact)

        # Sort results alphabetically by name
        results_sorted = sorted(results, key=lambda c: c['name'].lower())

        if results_sorted:
            print(f"\nFound {len(results_sorted)} contact(s):")
            for idx, contact in enumerate(results_sorted, 1):
                print(f"\nContact {idx}:")
                print(f"Name: {contact['name']}")
                print(f"Phone: {contact['phone']}")
                print(f"Email: {contact['email']}")
                print(f"Address: {contact['address']}")
            print(f"\nTotal contacts found: {len(results_sorted)}")
        else:
            print("No contacts found matching the query.")

    elif choice == '3':
        # Delete Contact
        phone = input("Enter Phone of contact to delete: ").strip()
        found = False
        for i, contact in enumerate(contacts):
            if contact['phone'] == phone:
                confirm = input(f"Are you sure you want to delete contact {contact['name']}? (y/n): ").lower()
                if confirm == 'y':
                    contacts.pop(i)
                    with open(CONTACTS_FILE, 'w') as f:
                        json.dump(contacts, f, indent=4)
                    print("Contact deleted successfully.")
                else:
                    print("Deletion canceled.")
                found = True
                break
        if not found:
            print("Contact not found.")

    elif choice == '4':
        # Update Contact
        phone = input("Enter Phone of contact to update: ").strip()
        found = False
        for contact in contacts:
            if contact['phone'] == phone:
                print(f"Updating contact: {contact['name']}")
                new_name = input(f"Enter new Name [{contact['name']}]: ").strip()
                new_email = input(f"Enter new Email [{contact['email']}]: ").strip()
                new_address = input(f"Enter new Address [{contact['address']}]: ").strip()

                # Validate email if changed
                if new_email:
                    if not validate_email(new_email):
                        print("Invalid email format. Update canceled.")
                        break
                else:
                    new_email = contact['email']

                # Update fields
                contact['name'] = new_name if new_name else contact['name']
                contact['email'] = new_email
                contact['address'] = new_address if new_address else contact['address']

                with open(CONTACTS_FILE, 'w') as f:
                    json.dump(contacts, f, indent=4)
                print("Contact updated successfully.")
                found = True
                break
        if not found:
            print("Contact not found.")

    elif choice == '5':
        # Export to CSV
        with open(CSV_FILE, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'phone', 'email', 'address'])
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)
        print(f"Contacts exported to {CSV_FILE}.")

    elif choice == '6':
        # Backup contacts
        with open(BACKUP_FILE, 'w') as backup_file:
            json.dump(contacts, backup_file, indent=4)
        print("Backup created successfully.")

    elif choice == '7':
        print("Exiting Contact Book. Goodbye!")
        break

    else:
        print("Invalid choice. Please select a valid option.")