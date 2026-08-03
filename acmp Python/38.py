def solve():
    n = int(input())
    nums = list(map(int, input().split()))
    
    # dp[i][j] — максимальная разница (текущий игрок − соперник) на отрезке nums[i..j]
    dp = [[0] * n for _ in range(n)]
    
    # База: отрезок из одного элемента
    for i in range(n):
        dp[i][i] = nums[i]
    
    # Заполняем для отрезков длины 2, 3, ..., n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Берём левый элемент: nums[i] − оптимальная разница на остатке [i+1, j]
            left = nums[i] - dp[i + 1][j]
            # Берём правый элемент: nums[j] − оптимальная разница на остатке [i, j-1]
            right = nums[j] - dp[i][j - 1]
            dp[i][j] = max(left, right)
    
    diff = dp[0][n - 1]
    print(diff)
    if diff > 0:
        print(1)
    elif diff < 0:
        print(2)
    else:
        print(0)

if __name__ == "__main__":
    solve()