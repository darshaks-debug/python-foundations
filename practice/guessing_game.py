#Guessing Game
import random
while True: #Outer Loop Here
    target = random.randint(1, 100)
    attempts = 0
    print("\n I'm thinking of a number between 1 and 100. Can you guess it?")
    while True: #Inner Loop Here
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue #Skips the rest of the inner loop and goes back to the start of the inner loop
        attempts += 1

        if guess < target:
            print("Too Low! Try again.")
        elif guess > target:
            print("Too High! Try again.")
        else:
            print(f"Congratulations! You've guessed the number {target} in {attempts} attempts.")
            break #Exit the inner loop if the guess is correct