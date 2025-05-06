import datetime

def get_time_based_greeting(name):
    current_time = datetime.datetime.now().hour
    if 5 <= current_time < 12:
        return f"Good morning, {name}!"
    elif 12 <= current_time < 18:
        return f"Good afternoon, {name}!"
    else:
        return f"Good evening, {name}!"

if __name__ == "__main__":
    user_name = input("Enter your name: ")
    greeting = get_time_based_greeting(user_name)
    print(greeting)