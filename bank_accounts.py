#Construct a class hierarchy for bank accounts.
class BankAccount :
    def __init__(self, owner_name, balance = 0):
        self.owner_name = owner_name 
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount} to {self.owner_name}'s account. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount} from {self.owner_name}'s account. New balance: {self.balance}")
        else:
            print("Insufficient funds or invalid amount.")

    def get_balance(self):
        return self.balance
    
    def __str__(self):
        return  f"Account owner: {self.owner_name}, Balance: {self.balance}"
    
class SavingsAccount(BankAccount):
    def __init__(self, owner_name, balance=0, interest_rate = 0.02):
        super().__init__(owner_name, balance)
        self.interest_rate = interest_rate
    
    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Applied interest: {interest}. New balance: {self.balance}")

class CheckingAccount(BankAccount):
    def __init__(self, owner_name, balance=0, overdraft_limit=100):
        super().__init__(owner_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self.balance + self.overdraft_limit) >= amount:
            self.balance -= amount
            print(f"Withdrew {amount} from {self.owner_name}'s account. New balance: {self.balance}")
        else:
            print("Withdrawal denied: Exceeds overdraft limit.")

savings = SavingsAccount("Alice", balance=1000)
savings.deposit(200)           # 200 para yatırılıyor
savings.apply_interest()       # Faiz uygulanıyor
savings.withdraw(500)          # 500 para çekiliyor
print(savings)                 # Hesap bilgileri yazdırılıyor

checking = CheckingAccount("Bob", balance=500)
checking.deposit(300)          # 300 para yatırılıyor
checking.withdraw(1000)        # 1000 para çekiliyor (bakiyenin üstünde fakat overdraft limitiyle izin veriliyor)
print(checking)                # Hesap bilgileri yazdırılıyor
