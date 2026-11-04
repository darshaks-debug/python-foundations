#Print all even number from 0 to 20 using for loop
for num in range(0, 21, 2):
    print(num)

#Modulo operator to check if a number is even or odd using is_even function
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False
print(is_even(4))  # Output: True
print(is_even(7))  # Output: False

#maxof_three function to find the maximum of three numbers
def max_of_three(a,b,c):
    if a >= b and a >= c:
        return a
    elif b >= a and b>= c:
        return b
    else:
        return c
print(max_of_three(30, 18, 26)) # Output: 30

#FizzBuzz program to print numbers from 1 to 100 with Fizz for multiples of 3, Buzz for multiples of 5, and FizzBuzz for multiples of both
for i in range(1, 101):
    if i % 3 ==0 and i % 5 ==0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

#count vowels function to count the number of vowels in a given string
def count_vowels(string):
    vowels = "aeiouAEIOU"
    count =0
    for char in string:
        if char in vowels:
            count += 1
    return count
print(count_vowels("Hello World")) # Output: 3

# reverse_string function to reverse a given string without using inbuilt functions
def reverse_string(text):
    reversed_string = ""
    for char in text:
        reversed_string = char + reversed_string
    return reversed_string
print(reverse_string("It is a beautiful day"))

# print the multiplication table of a given number
num = int(input("Enter a number: "))
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

#is_prime() function to check if a number is prime or not
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

print(is_prime(11))
print(is_prime(15)) 