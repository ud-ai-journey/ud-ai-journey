balance = 1000.0  # Initial balance

while True:
    print("\nATM Menu:")
    print("1. Withdraw")
    print("2. Deposit")
    print("3. Check Balance")   
    print("4. Transfer funds")
    print("5. Exit")
    
    option = input("Select an option (1-5): ")
    
    if option == '1':
        amount = float(input("Enter amount to withdraw: "))
        if amount <= balance and amount > 0:
            balance -= amount
            print(f"Withdrew ${amount}. New balance: ${balance:.2f}")
        else:
            print("Invalid withdrawal amount.")
    
    elif option == '2':
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            balance += amount
            print(f"Deposited ${amount}. New balance: ${balance:.2f}")
        else:
            print("Invalid deposit amount.")
    
    elif option == '3':
        print(f"Your balance is: ${balance:.2f}")
    
    elif option == '4':
        transfer_amount = float(input("Enter amount to transfer: "))
        if transfer_amount <= balance and transfer_amount > 0:
            balance -= transfer_amount
            print(f"Transferred ${transfer_amount}. New balance: ${balance:.2f}")
        else:
            print("Invalid transfer amount.")
    
    elif option == '5':
        print("Thank you for using the ATM. Goodbye!")
        break
    
    else:
        print("Invalid option selected, please choose again.")