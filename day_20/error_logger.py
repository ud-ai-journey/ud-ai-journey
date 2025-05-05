import datetime

error = input("Enter error message: ")
timestamp = datetime.datetime.now()

with open("error_log.txt", "a") as log:
    log.write(f"[{timestamp}] ERROR: {error}\n")

print("Error logged.")