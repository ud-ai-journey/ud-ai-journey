grades = {}

while True:
    name = input("Enter student name (or 'done' to stop): ").strip()
    if name.lower() == 'done':
        break
    grade = input(f"Enter grade for {name}: ").strip()
    grades[name] = grade

print("\nGradebook:")
for student, grade in grades.items():
    print(f"{student}: {grade}")