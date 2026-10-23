#Accumulate the sum of a list of numbers
nums = [3, 1, 4, 1, 5, 9, 2]
total = 0
for num in nums:
    total = total + num
print(total)

#Word Frequency Counter
sentence = "the quick brown fox jumps over the lazy dog the quick brown fox"
word_count = {}

words = sentence.split()
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
print(word_count)

#Remove duplicates from a list
nums = [3, 1, 4, 1, 5, 9, 2]
unique_nums = []
for num in nums:
    if num not in unique_nums:
        unique_nums.append(num)
print(unique_nums)

#Find the second largest number in a list
nums = [1, 4, 9, 16, 25, 36]
largest = second_largest = float('-inf')
for num in nums:
    if num > largest:
        second_largest = largest
        largest = num
    elif num > second_largest and num != largest:
        second_largest = num
print(second_largest)

#Merge two dictionaries, summing values for common keys
dict1 = {'a': 10, 'b': 20}
dict2 = {'b': 5, 'c': 15}
merged_dict = {}
for key in dict1:
    merged_dict[key] = dict1[key]
for key in dict2:
    if key in merged_dict:
        merged_dict[key] += dict2[key]
    else:
        merged_dict[key] = dict2[key]
print(merged_dict)

#Given two lists, return their intersection (items that are present in both lists)
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
intersection = []
for item in list1:
    if item in list2:
        intersection.append(item)
print(intersection)

#Reverse List (without using built-in functions)
nums = [1, 2, 3, 4, 5]
reversed_nums = []
for i in range(len(nums) -1, -1, -1):
    reversed_nums.append(nums[i])
print(reversed_nums)

#Sort a list of dictionaries by a specific key
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 20},
    {"name": "Charlie", "age": 25}
]
people.sort(key=lambda x: x["age"])
print(people)

#Anagram Checker
s1 = "listen"
s2 = "silent"
if sorted(s1) == sorted(s2):
    print("ANAGRAMS")
else:
    print("NOT ANAGRAMS")

#Given a list of items, count the frequency of each item
items = ["apple", "banana", "apple", "orange", "banana", "apple"]
item_count = {}

for word in items:
    if word in item_count:
        item_count[word] += 1
    else:
        item_count[word] = 1
print(item_count)