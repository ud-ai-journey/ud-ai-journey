import string

password = input("Enter your password: ")

length = len(password)
digits = sum(c.isdigit() for c in password)
uppercase = sum(c.isupper() for c in password)
lowercase = sum(c.islower() for c in password)
symbols = sum(c in string.punctuation for c in password)

score = 0

# Basic criteria
if length >= 8:
    score += 1
if digits >= 1:
    score += 1
if uppercase >= 1:
    score += 1
if lowercase >= 1:
    score += 1
if symbols >= 1:
    score += 1

print(f"Password Strength Score: {score} out of 5")

if score == 5:
    print("Strong password!")
elif score >= 3:
    print("Moderate password.")
else:
    print("Weak password. Try adding more uppercase, numbers, or symbols.")