def find_ans(n: int):
    if n == 0: return 10
    if n==1: return 1
    digits = []
    for d in range(9,1,-1):
        while n%d ==0:
            digits.append(d)
            n//=d
    if n>1: return -1
    digits.sort()
    return ''.join(map(str, digits))
def solve():
    current, n = map(int, input().split())
    ans = int(find_ans(n))
    if ans<=current and ans>=0: print("YES")
    else: print("NO")
if __name__ == "__main__":
    solve()