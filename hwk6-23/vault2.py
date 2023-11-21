import sys
import time

def read_vault(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        vault = [[int(coin) for coin in line.strip().split(',')] for line in lines]
    return vault

def find_optimal_path(vault):
    rows = len(vault)
    cols = len(vault[0])

    dp = [[0] * cols for _ in range(rows)]

    # Fill the first row and column of the dp table
    dp[0][0] = vault[0][0]
    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + vault[i][0]
    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + vault[0][j]

    # Fill the rest of the dp table
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + vault[i][j]

    # Reconstruct the path
    path = []
    i, j = rows - 1, cols - 1
    while i > 0 or j > 0:
        if i == 0:
            path.append('W')
            j -= 1
        elif j == 0:
            path.append('N')
            i -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            path.append('N')
            i -= 1
        else:
            path.append('W')
            j -= 1

    path.reverse()
    return path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vault.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    start_time = time.perf_counter_ns()

    vault = read_vault(input_file)
    path = find_optimal_path(vault)

    end_time = time.perf_counter_ns()

    total_coins = sum(vault[i][j] for i, j in zip(range(len(vault)), [0] + [path.index('N') + 1 for _ in range(len(path))]))

    print(''.join(path))
    print(total_coins)
    print(end_time - start_time)
