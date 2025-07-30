## we need to generate a function benchmark
# constraints: 
# input is single integer n
# output has to be single integer s
import math
def constant_time(n):
    return 69

def log_time(n):
    s=0
    recur = int(math.log2(n))
    for i in range(recur):
        s+=i
    return s

def linear_time(n):
    s=0
    for i in range(n):
        s+=i
    return s

def quadratic_time(n):
    s=0
    for i in range(n):
        for j in range(n):
            s+=i+j
    return s

def cubic_time(n):
    s=0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                s += i+j+k
    return s

def biquadratic_time(n):
    s=0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    s += i+j+k+l
    return s

def random_funct(n):
    s = 0
    for i in range(n):
        for j in range(int(math.log2(n))):
            s += 1
        for k in range(n):
            s -= 1
    
    return s

def n_log_n_time(n):
    s = 0
    for i in range(n):
        # Simulate O(n log n) like merge sort
        for j in range(int(math.log2(n))):
            for k in range(n):
                s += 1
    return s

def sqrt_time(n):
    s = 0
    # Simulate O(sqrt(n)) like checking if number is prime
    for i in range(int(math.sqrt(n))):
        s += i
    return s

def exponential_time(n):
    s = 0
    # Simulate O(2^n) like recursive Fibonacci
    def fib(n):
        if n <= 1:
            return n
        return fib(n-1) + fib(n-2)
    return fib(n)

def factorial_time(n):
    s = 0
    # Simulate O(n!) like traveling salesman brute force
    def permute(arr, start):
        if start == len(arr):
            s += 1
            return
        for i in range(start, len(arr)):
            arr[start], arr[i] = arr[i], arr[start]
            permute(arr, start + 1)
            arr[start], arr[i] = arr[i], arr[start]
    
    arr = list(range(n))
    permute(arr, 0)
    return s

def mixed_complexity(n):
    s = 0
    # Function with mixed complexities
    # O(n) + O(log n) + O(n^2)
    for i in range(n):  # O(n)
        s += i
    
    for i in range(int(math.log2(n))):  # O(log n)
        s += i
    
    for i in range(n):  # O(n^2)
        for j in range(n):
            s += i + j
    return s

def binary_search_simulation(n):
    s = 0
    # Simulate binary search pattern
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        s += mid
        if mid < n/2:  # arbitrary condition
            left = mid + 1
        else:
            right = mid
    return s

def matrix_operations(n):
    s = 0
    # Simulate matrix operations
    for i in range(n):
        for j in range(n):
            for k in range(n):
                s += i * j * k  # matrix multiplication pattern
    return s

def tree_traversal(n):
    s = 0
    # Simulate tree traversal
    def build_tree(height):
        if height <= 0:
            return 1
        return build_tree(height-1) + build_tree(height-1)
    
    return build_tree(int(math.log2(n)))

# request - package
# leetcode



