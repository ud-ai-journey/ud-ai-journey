import math

def is_even(number):
    return "Even ✅" if number % 2 == 0 else "Odd ✅"

def is_prime(number):
    if number < 2:
        return "Not Prime ❌"
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return "Not Prime ❌"
    return "Prime ✅"

def is_palindrome(number):
    return "Palindrome ✅" if str(number) == str(number)[::-1] else "Not Palindrome ❌"

def is_perfect_square(number):
    root = int(math.sqrt(number))
    if root * root == number:
        return f"Perfect Square ✅ ({root} x {root})"
    return "Not Perfect Square ❌"

def is_buzz_number(number):
    if number % 7 == 0 or str(number).endswith('7'):
        return "Buzz Number 🌟"
    return "Not a Buzz Number ❌"

def analyze_number(number):
    print(f"\nResults for {number}:")
    print(f"- {is_even(number)}")
    print(f"- {is_prime(number)}")
    print(f"- {is_palindrome(number)}")
    print(f"- {is_perfect_square(number)}")
    print(f"- {is_buzz_number(number)}")

def main():
    print("🔢 Smart Number Analyzer 🔢")
    user_input = input("Enter number(s) (comma-separated for multiple): ")
    
    try:
        # Split input by commas and convert to integers
        numbers = [int(num.strip()) for num in user_input.split(',')]
        
        # Analyze each number
        for number in numbers:
            analyze_number(number)
            
    except ValueError:
        print("🚨 Please enter valid numbers (integers, comma-separated)!")

if __name__ == "__main__":
    main()