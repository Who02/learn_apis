while True:
    n = int(input("Enter size: "))
    if n%2!=0: break
    else: print("Size must be odd!")
for i in range(n):
    for j in range(n):
        if (i == 0 or i == n-1 or j == i or j == n-i-1): print('*', end="")
        else: print(" ", end="")
    print()