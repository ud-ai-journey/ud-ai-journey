subjects = ['Math', 'Science', 'English', 'History']

for subject in subjects:
    marks = float(input(f"Enter your marks for {subject} (0-100): "))
    
    if 0 <= marks <= 100:
        if marks >= 90:
            grade = 'A'
        elif marks >= 80:
            grade = 'B'
        elif marks >= 70:
            grade = 'C'
        elif marks >= 60:
            grade = 'D'
        else:
            grade = 'Fail'
            
        print(f"Your grade in {subject} is: {grade}")
    else:
        print("Invalid marks entered. Please enter a number between 0 and 100.")