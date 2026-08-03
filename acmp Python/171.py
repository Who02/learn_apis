def solve():
    n = int(input())
    ans = 0
    for i in range(9,1,-1):
        if n%i == 0: ans+=1
        while n%i == 0: n//=i
    for i in range(1,n):
        if n%i == 0: ans+=1
    print(ans)
if __name__ == "__main__":
    solve()