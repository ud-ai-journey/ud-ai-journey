balance = 1000  # starting balance

while True:
    print("\nATM Menu:")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")
    choice = input("Choose an option (1-4): ")

    if choice == '1':
        print(f"Your current balance is: ${balance}")
    elif choice == '2':
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            balance += amount
            print(f"Deposited ${amount}. New balance: ${balance}")
        else:
            print("Invalid amount.")
    elif choice == '3':
        amount = float(input("Enter amount to withdraw: "))
        if 0 < amount <= balance:
            balance -= amount
            print(f"Withdrew ${amount}. New balance: ${balance}")
        else:
            print("Invalid or insufficient funds.")
    elif choice == '4':
        print("Thank you! Goodbye.")
        break
    else:
        print("Invalid choice, please try again.")