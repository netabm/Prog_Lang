from functools import reduce

###Task 1###
print("Task 1:")
fibonacci = lambda n, a=0, b=1: [a] + fibonacci(n-1, b, a+b) if n > 0 else []
print(fibonacci(10))

print()
###Task 2###
print("Task 2:")
concat_strings = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)

strings = ["Itay", "Neta", "Best", "Project", "Ever", "Wow"]
result = concat_strings(strings)
print(result)

print()
###Task 3###
print("Task 3:")
def cumulative_sum_of_squares(list_of_lists):
    return list(
        map(
            # Apply this lambda function to each sublist in list_of_lists
            lambda sublist: [
                (
                    lambda even_numbers: (
                        lambda squares: (
                            # Sum the squares
                            lambda sum: sum(squares)
                        )(lambda l: sum(l))  # Inner lambda to sum the list of squares
                    )(list(map(lambda x: x**2, even_numbers)))  # Map to square each even number
                )(list(filter(lambda x: x % 2 == 0, sublist)))  # Filter to get even numbers
            ],
            list_of_lists
        )
    )

input_lists = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
result = cumulative_sum_of_squares(input_lists)
print(result)

print()
###Task 4###
print("Task 4:")

def apply_cumulatively(binary_op):
    return lambda sequence: reduce(binary_op, sequence)

# Factorial
def factorial(n):
    if n == 0:
        return 1
    return apply_cumulatively(lambda x, y: x * y)(range(1, n + 1))

# Exponentiation
def exponentiation(base, exp):
    return apply_cumulatively(lambda x, y: x * y)([base] * exp)

print(factorial(5))
print(exponentiation(2, 3))

print()
###Task 5###
print("Task 5:")

nums = [1, 2, 3, 4, 5, 6]
sum_squared = reduce(lambda total, x: total + x, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))
print(sum_squared)

print()
###Task 6###
print("Task 6:")

count_palindromes = lambda lst: list(map(lambda sublist: reduce(lambda total, x: total + 1, filter(lambda s: s == s[::-1], sublist), 0), lst))
lst = [['wow', 'hello', 'level'], ['programming languages', 'lol'], ['amazing', 'racecar']]
result = count_palindromes(lst)
print(result)  # Output: [2, 1, 1]

print()
###Task 7###
print("Task 7:")

print("Lazy evaluation is a technique where values are only computed when they are actually needed, rather than all at once.\n"
          "This can make programs more efficient by saving time and memory.\n\n"
          "Eager Evaluation:\n"
          "In the first part of the program, eager evaluation is used.\n"
          "Here, the function that generates values is called, and all the values are created and stored in a list immediately.\n"
          "This means the program runs through the entire sequence, generating all values at once, and then processes each value to compute its square.\n"
          "This approach can be inefficient if the dataset is large because it requires storing all the values in memory at once.\n\n"
          "Lazy Evaluation:\n"
          "In the second part of the program, lazy evaluation is demonstrated.\n"
          "Instead of generating all values at once, the program creates each value only when it is needed.\n"
          "The function that generates values is used directly in the list comprehension,\nso it produces one value at a time as the list comprehension processes each value to compute its square.\n"
          "This means the program doesn’t need to store all the values in memory, making it more efficient.\n")

###Task 8###
print("Task 8:")

prime_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))], reverse=True)
sample_list = [10, 3, 5, 7, 11, 4, 6, 13, 17, 19, 23, 29, 31]
result = prime_desc(sample_list)
print(result)
