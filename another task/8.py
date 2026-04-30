class BankAccount():
    def __init__ (self,n,b):
        self.__account_number = n
        self.__balance = b 
    def add(self, count):
        self.__balance += count
        print(f"On the balance: {self.__balance}")
    def withdraw(self, count):
        if count <= self.__balance:
            self.__balance -=count
            print(f"On the balance: {self.__balance}")
        else:
            print("Insufficient funds")
            print(f"On the balance: {self.__balance}")
one = BankAccount(int(input("Account number: ")), int(input("Balance: ")))
one.add(int(input("Add to balance: ")))
one.withdraw(int(input("Remove from balance: ")))