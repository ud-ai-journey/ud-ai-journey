# String Compression

input_string = "aaabbcccaaa"
compressed_string = ""
i = 0
while i < len(input_string):
    count = 1
    j = i + 1
    while j < len(input_string) and input_string[j] == input_string[i]:
        count += 1
        j += 1
    compressed_string += input_string[i] + str(count)
    i = j
print(compressed_string)  # Output: a3b2c3a3
