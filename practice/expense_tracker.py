#Expense Tracker
import json
try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except FileNotFoundError:
    expenses = []

while True:
    command = input("Enter a command (add, list, total, exit): ").lower()

    if command == "add":
        try:
            amount = float(input("Enter Expense Amount: "))
            if amount < 0:
                print("Amount cannot be negative. Please try again.")
                continue
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            continue

        description = input("Enter Expense Description: ")
        if description.strip() == "":
            print("Description cannot be empty. Please try again.")
            continue

        dict_expense = {"amount": amount, "description": description}
        expenses.append(dict_expense)
        print("Expense added!")
        with open("expenses.json", "w") as file:
            json.dump(expenses, file)

    elif command == "list":
        for expense in expenses:
            print(f"Amount: {expense['amount']}, Description: {expense['description']}")

    elif command == "total":
        total_amount = sum(expense['amount'] for expense in expenses)
        print(f"Total Expenses: {total_amount}")

    elif command == "exit":
        print("Exiting the expense tracker.")
        break

    else:
        print("Invalid command. Please try again.")