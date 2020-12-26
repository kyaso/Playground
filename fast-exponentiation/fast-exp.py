#!/usr/bin/python3
import sys
import time

def normal_exp(x, e):
    return x**e

def slow_exp(x, e):
#return # Uncomment this return statement if you don't want to run the slow version
    res = 1

    for i in range(0,e):
        res = res * x

    return res

def fast_exp(x, e):
    if e == 0:
        return 1

    e_bin = bin(e)[2:][::-1] # [2:] = truncate away the '0b' prefix; [::-1] = reverse string, so LSB is first character
    res = 1
    g = x
    for bit in e_bin:
        if bit == '1':
            res = res * g
        
        g = g*g

    return res

# Parse args
x = int(sys.argv[1])
e = int(sys.argv[2])

# Run normal exponentiation
start = time.perf_counter()
result_normal = normal_exp(x,e)
time_normal = time.perf_counter() - start

# Run slow exponentiation
start = time.perf_counter()
result_slow = slow_exp(x,e)
time_slow = time.perf_counter() - start

# Run fast exponentiation
start = time.perf_counter()
result_fast = fast_exp(x,e)
time_fast = time.perf_counter() - start

# Check results
if result_normal != result_slow:
    print("ERROR: Slow result not correct!")

if result_normal != result_fast:
    print("ERROR: Fast result not correct!")

# Report timings
print("Normal: Time = ", time_normal)
print("Slow: Time = ", time_slow)
print("Fast: Time = ", time_fast)
