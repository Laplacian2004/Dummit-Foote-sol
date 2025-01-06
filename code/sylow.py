import sympy
import matplotlib.pyplot as plt
from bisect import bisect_left

# Optimized function to determine if a number is a power of a prime using binary search
def is_power_of_prime(n):
    # Precompute powers of primes up to n
    powers = []
    for p in sympy.primerange(2, int(n**0.5) + 1):
        power = p
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
    for k in range(1, n // p + 1):  # Check divisors of n
        np_candidate = k * p + 1
        if np_candidate % p == 1 and n % np_candidate == 0:
            values.append(np_candidate)
    return values

# Main program
odd_numbers = [n for n in range(3, 10000, 2) if not is_power_of_prime(n)]
results = {}

for n in odd_numbers:
    factors = sympy.factorint(n)  # Factorize n
    permissible = {}
    for p in factors.keys():
        permissible[p] = permissible_values(n, p)
    if any(len(vals) > 0 for vals in permissible.values()):
        results[n] = {
            "factors": factors,
            "permissible_values": permissible,
        }

# Plotting results
x = []  # n values
y = []  # Count of permissible values

for n, data in results.items():
    x.append(n)
    count = sum(len(vals) for vals in data["permissible_values"].values())
    y.append(count)

plt.figure(figsize=(12, 6))
plt.scatter(x, y, color="blue", s=10, label="Permissible $n_p$ values")
plt.title("Number of permissible $n_p$ values for odd numbers < 10,000")
plt.xlabel("$n$")
plt.ylabel("Count of permissible $n_p$ values")
plt.grid(True)
plt.legend()
plt.show()
