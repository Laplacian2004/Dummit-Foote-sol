import sympy
import matplotlib.pyplot as plt
import numpy as np
import argparse
from bisect import bisect_left

# Optimized function to determine if a number is a power of a prime using binary search
def is_power_of_prime(n):
    # Precompute powers of primes up to n
    powers = []
    for p in sympy.primerange(2, int(n**0.5) + 1):
        power = int(p)  # Ensure power is explicitly treated as an integer
        while power <= n:
            powers.append(power)
            power *= p
    
    # Sort the powers for binary search
    powers.sort()
    
    # Use binary search to check if n is a power of a prime
    index = bisect_left(powers, n)
    return index < len(powers) and powers[index] == n

# Function to find permissible values of n_p
def permissible_values(n, p):
    values = []
    for k in range(0, n // p + 1):  # Check divisors of n
        np_candidate = k * p + 1
        if np_candidate % p == 1 and n % np_candidate == 0:
            values.append(np_candidate)
    return values
parser = argparse.ArgumentParser(description="Analyze permissible n_p values in given range.")
parser.add_argument("--low", type=int, default=3, help="Lower bound of the range (default: 3)")
parser.add_argument("--high", type=int, default=10000, help="Upper bound of the range (default: 10000)")
parser.add_argument("--step", type=int, default=2, help="Step of the range (default: 2)") 
args = parser.parse_args()


odd_numbers = [n for n in range(args.low, args.high, args.step) if not is_power_of_prime(n)]
results = {}

for n in odd_numbers:
    factors = sympy.factorint(n)  # Factorize n
    permissible = {}
    for p in factors.keys():
        permissible[p] = permissible_values(n, p)
    if any(len(vals) > 1 for vals in permissible.values()):
        results[n] = {
            "factors": factors,
            "permissible_values": permissible,
        }

# Save results in a .out file
with open("np_list.out", "w") as file:
    for n, data in results.items():
        row = [f"n = {n}"]
        for p, vals in data["permissible_values"].items():
            if vals:
                row.append(f"n_{p} = {', '.join(map(str, vals))}")
        file.write(" / ".join(row) + "\n")

# Plotting results
x = []  # n values
y = []  # Count of permissible value
z = []  # max permissible values

for n, data in results.items():
    x.append(n)
    count = sum(len(vals) for vals in data["permissible_values"].values())
    maxlen = max(len(vals) for vals in data["permissible_values"].values()) 
    y.append(count)
    z.append(maxlen)

plt.figure(figsize=(12, 6))
plt.scatter(x, y, color="blue", s=10, label="Permissible $n_p$ values")
plt.title(f"Number of permissible $n_p$ values for in ({args.low}, {args.high}) with step {args.step}")
plt.xlabel("$n$")
plt.ylabel("Count of permissible $n_p$ values")
plt.grid(True)
plt.legend()
plt.show()

# Calculate frequencies of each integer class
unique_classes, frequencies = np.unique(y, return_counts=True)

plt.bar(unique_classes, frequencies, color='skyblue', edgecolor='black')
plt.title("Number of permissible $n_p$ values frequencies")
plt.xlabel("Number of $n_p$ Values")
plt.ylabel("Frequency of $n$")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Calculate frequencies of each integer class
unique_classes, frequencies = np.unique(z, return_counts=True)

plt.bar(unique_classes, frequencies, color='teal', edgecolor='black')
plt.title("Number of max permissible $n_p$ values frequencies")
plt.xlabel("Number of $n_p$ Values")
plt.ylabel("Frequency of $n$")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

