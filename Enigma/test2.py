import time


def sieve_of_sundaram(limit):
    primes = []
    # Create a list of integers from 1 to limit
    numbers = [i for i in range(1, limit+1)]
    # Iterate through the list
    for i in range(1, limit//2 + 1):
        for j in range(i, limit//2 + 1):
            num = i + j + (2 * i * j)
            if num <= limit:
                numbers[num-1] = 0
    # Append the prime numbers to the primes list
    primes = [2*n + 1 for n in numbers if n > 0]
    primes.insert(0, 2)
    #return primes


def run_time_average(func, limit, runs=1):
    total_time = 0
    for i in range(runs):
        start = time.time()
        func(limit)
        end = time.time()
        total_time += end - start
    return total_time / runs

total_time = run_time_average(sieve_of_sundaram, int(1e10))
print(f'Total time: {total_time} seconds')