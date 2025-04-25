students = {
    "Alice": {"Math": 85, "Science": 92},
    "Bob": {"Math": 78, "Science": 88},
    "Charlie": {"Math": 90, "Science": 95}
}

# Allow adding new students
while True:
    add_student = input("Do you want to add a new student? (yes/no): ").strip().lower()
    if add_student == 'no':
        break
    elif add_student == 'yes':
        name = input("Enter the student's name: ")
        marks = {}
        while True:
            subject = input("Enter subject name (or type 'done' to finish): ")
            if subject.lower() == 'done':
                break
            mark = int(input(f"Enter {name}'s mark for {subject}: "))
            marks[subject] = mark
        students[name] = marks
    else:
        print("Invalid response. Please enter 'yes' or 'no'.")

# Print each student's details
for student, marks in students.items():
    total = sum(marks.values())
    average = total / len(marks)
    
    if average >= 90:
        grade = "A+"
    elif average >= 80:
        grade = "A"
    elif average >= 70:
        grade = "B"
    else:
        grade = "C"
    
    print(f"Report Card for {student}:")
    for subject, mark in marks.items():
        print(f"  {subject}: {mark}")
    print(f"  Total: {total}, Average: {average:.2f}, Grade: {grade}\n")

# Find subject-wise topper
subject_toppers = {}
for student, marks in students.items():
    for subject, mark in marks.items():
        if subject not in subject_toppers or mark > subject_toppers[subject]['mark']:
            subject_toppers[subject] = {'student': student, 'mark': mark}

print("Subject-wise Toppers:")
for subject, topper in subject_toppers.items():
    print(f"{subject}: {topper['student']} with mark {topper['mark']}")