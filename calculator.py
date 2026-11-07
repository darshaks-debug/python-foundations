while True:
    command = input("Press Enter to Calculate, or type 'quit' to exit: ")
    if command.lower() == 'quit':
        break
    try:
        num1 = float(input("First Number: "))
        op = input("Operation (+ - * /): ")
        num2 = float(input("Second Number: "))
        
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            result = num1 / num2
        else:
            result = "INVALID OPERATION"
        print(f"{num1} {op} {num2} = {result}")
        
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except ZeroDivisionError:
        print("Error: You cannot divide by Zero.")