def say_hello(name="Guest", greeting="Hello"):
    print(f"{greeting}, {name}!")

# Using default arguments
say_hello()
say_hello("Alice")
say_hello(greeting="Hi")
say_hello("Bob", "Good morning")

# Using keyword arguments
say_hello(name="Charlie", greeting="Hey there")
say_hello(greeting="Hola", name="David")