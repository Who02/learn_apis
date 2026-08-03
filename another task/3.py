year = int(input("Enter year: "))
if year%400 == 0 and year % 4 == 0:
    print("Високостный")
else: print("Не високостный")