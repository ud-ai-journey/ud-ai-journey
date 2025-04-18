# Basic brainstorming of formulas
# speed = distance / time
# distance = speed * time
# time = distance / speed

# Introduction
name = input("Hi Buddy, What's your name?: ")
r1 = f"Nice to know you {name} - Let's learn about speed-distance-time from your car and travel mate."

# Gather input from the user
speed = float(input(f"What's the usual speed you go in your car {name}?: "))
distance = float(input(f"{name}, How much distance did you cover till now in your car?: "))
time = float(input(f"{name}, How much time did it take to reach the destination in your car?: "))

# Common Rules
if speed <= 0 or time <= 0 or distance <= 0:
    print("Mate, Speed, Time, and Distance must all be greater than zero!")
else:
    choice = input(f"Hey {name}, what do you want to know about?\n1) Speed \n2) Distance \n3) Time\n").strip().lower()

    # Calculate values
    avg_time = distance / speed
    total_distance = time * speed
    calculated_speed = distance / time
    ideal_speed = 100   

    # Determine user choice
    if choice == "time":
        print(f"Hey {name}, your average time during the travel is: {avg_time:.2f} hours")

    elif choice == "distance":
        print(f"Hey {name}, your total distance covered during the travel is: {total_distance:.2f} km")

    elif choice == "speed":
        print(f"Hey {name}, your average speed during the travel is: {calculated_speed:.2f} km/h")
        if calculated_speed > ideal_speed:
            print(f"{name}, you are exceeding the speed limit... Let's go slow mate because slow and steady wins the race :)")
    else:
        print("Mate, I didn’t get that! Please choose from time, distance, or speed.")