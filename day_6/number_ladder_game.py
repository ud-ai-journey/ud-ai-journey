n = 4  # Number of rows
num = 1  # Starting number
row = 1  # Start from the first row

while row <= n:  # Outer loop for rows
    inner_count = 1  # Initialize inner count for this row
    while inner_count <= row:  # Inner loop for numbers in the current row
        print(num, end=' ')
        num += 1  # Increment the number
        inner_count += 1  # Move to the next position
    print()  # Move to the next line after finishing the row
    row += 1  # Move to the next row