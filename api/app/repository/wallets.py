BALANCE: dict[str,float]={}

def is_wallet_exist(wallet_name: str)->bool:
    return wallet_name in BALANCE

def add_income(wallet_name:str, amount: float)->float:
    BALANCE[wallet_name]+=amount
    return BALANCE[wallet_name]

def get_balance(wallet_name):
    return BALANCE[wallet_name:str]

def add_expence(wallet_name:str, amount:float)->float:
    BALANCE[wallet_name]-=amount
    return BALANCE[wallet_name]

def get_all_wallets()->dict[str,float]:
    return BALANCE.copy()

def create_wallet(wallet_name:str, initial_balance: float)->float:
    BALANCE[wallet_name]=initial_balance
    return BALANCE[wallet_name]
