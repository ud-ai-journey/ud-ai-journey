dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

print("Before merge:")
print("Dict1:", dict1)
print("Dict2:", dict2)

dict1.update(dict2)

print("\nAfter merging dict2 into dict1:")
print("Merged Dict:", dict1)