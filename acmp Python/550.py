
def solve():
    n = int(input())
    if n%400 == 0:
        print(f"12/09/{n:04}")
    elif n%4 == 0 and n%100 != 0:
        print(f"12/09/{n:04}")
    else: print(f"13/09/{n:04}")
if __name__ == "__main__":
    solve()