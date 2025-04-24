numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if not numbers:
    print("List is empty")
else:
    max_num = numbers[0]
    min_num = numbers[0]
    total = 0
    for number in numbers:
        if number > max_num:
            max_num = number
        if number < min_num:
            min_num = number
        total += number
    average = total / len(numbers) if numbers else 0  # Avoid ZeroDivisionError
    print("Max:", max_num)
    print("Min:", min_num) 
    print("Sum:", total)
    print("Average:", average)