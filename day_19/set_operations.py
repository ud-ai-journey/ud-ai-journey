a = set(input("Enter elements of Set A (space separated): ").split())
b = set(input("Enter elements of Set B (space separated): ").split())

print("\nUnion:", a.union(b))
print("Intersection:", a.intersection(b))
print("Difference (A - B):", a.difference(b))