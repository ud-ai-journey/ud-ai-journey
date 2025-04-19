# 🌟 Pattern 8: Inverted pyramid (center aligned)
n = 5
for i in range(n, 0, -1):
    print(" " * (n - i) + "*" * (2 * i - 1))  # Starts wide and narrows
