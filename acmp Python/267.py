
def solve():
    n, x, y = map(int, input().split())
    
    time = min(x,y)
    n -= 1
    left = -1
    right = n*x
    
    while right - left > 1:
        mid = int((right + left)/2)
        if (mid//x + mid//y) >= n: right = mid
        else: left = mid
    
    print(time+ right)
    

if __name__ == "__main__":
    solve()