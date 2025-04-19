# 🌟 Pattern 7: Pyramid (center aligned)
n = 5
for i in range(n):
    print(" " * (n - i) + "*" * (2 * i + 1))  # Spaces on left + growing star pattern
