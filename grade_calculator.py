# Grade Calculator
marks = []

#Loop until we get exactly 5 valid marks
while len(marks) < 5:
    try:
        #len(marks) + 1 is used to display the subject number (1 to 5)
        mark = float(input(f"Enter marks for subject {len(marks) + 1}: "))
        #Check if the mark is within the valid range (0 to 100)
        if 0 <= mark <= 100:
            marks.append(mark)
        else:
            print("Error: Marks must be between 0 and 100. Please try again.")
    except ValueError:
        print("Error: Invalid input. Please enter a numeric value.")
        
average = sum(marks) / len(marks)

if average >= 90:
    grade = 'A'
elif average >= 80:
    grade = 'B'
elif average >= 70:
    grade = 'C'
elif average >= 60:
    grade = 'D'
else:
    grade = 'F'

print("\n--- REPORT CARD ---")
print(f"Average Marks: {average:.2f}")
# The :.2f format specifier is used to display the average marks rounded to two decimal places.
print(f"Final Grade: {grade}")