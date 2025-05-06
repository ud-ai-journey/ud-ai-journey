from calculator_module import add, subtract
from math_utilities import factorial

result_add = add(10, 5)
print(f"10 + 5 = {result_add}")

result_sub = subtract(20, 7)
print(f"20 - 7 = {result_sub}")

num = 5
fact_result = factorial(num)
print(f"Factorial of {num} is {fact_result}")
