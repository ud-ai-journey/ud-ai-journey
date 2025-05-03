full_name = input("Enter your full name: ").strip()

# Assuming the full name has at least first and last name
name_parts = full_name.split()

# First and last name
first_name = name_parts[0]
last_name = name_parts[-1]

# Initials
initials = ''.join([part[0].upper() for part in name_parts])

# Name formats
uppercase_name = full_name.upper()
lowercase_name = full_name.lower()
titlecase_name = full_name.title()

# Reversed full name
reversed_name = full_name[::-1]

print(f"First Name: {first_name}")
print(f"Last Name: {last_name}")
print(f"Initials: {initials}")
print(f"Uppercase: {uppercase_name}")
print(f"Lowercase: {lowercase_name}")
print(f"Title Case: {titlecase_name}")
print(f"Reversed Name: {reversed_name}")