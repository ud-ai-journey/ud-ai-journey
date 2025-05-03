students = []

print("Enter data for 3 students:")

for i in range(3):
    name = input(f"Enter name of student {i+1}: ")
    score_input = input(f"Enter score for {name}: ")
    while True:
        try:
            score = float(score_input)
            break
        except ValueError:
            score_input = input("Invalid score. Please enter a numeric value: ")
    students.append((name, score))

scores = [score for _, score in students]
average_score = sum(scores) / len(scores)
highest_score = max(scores)
lowest_score = min(scores)

# Find students with highest and lowest scores
highest_students = [name for name, score in students if score == highest_score]
lowest_students = [name for name, score in students if score == lowest_score]

print("\nStudent Scores:")
for name, score in students:
    print(f"{name} scored {score}")

print(f"\nAverage score: {average_score:.2f}")
print(f"Highest score: {highest_score} by {', '.join(highest_students)}")
print(f"Lowest score: {lowest_score} by {', '.join(lowest_students)}")