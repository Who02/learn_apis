from fastapi import FastAPI
from fastapi.responses import Response
from fastapi import HTTPException
from pydantic import BaseModel
app = FastAPI()
class OperationRequest(BaseModel):
    wallet_name: str
    amount: float
    description: str| None = None
    
BALANCE = {}

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if not wallet_name:
        return {"total balance": sum(BALANCE.values())}
    
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
        
    return f"Wallet: {wallet_name}, balance: {BALANCE[wallet_name]}"

@app.post("/wallets/{name}")
def create_wallet(name: str, initial_balance: float = 0):
    if name in BALANCE: 
        raise HTTPException(status_code=404, 
                            detail=f"wallet {name} already exist")
    BALANCE[name]=initial_balance
    return {f"Wallet {name} created",
            f"wallet: {name}, balance {initial_balance}"}
    
@app.post("/operation/income")
def add_income():
    pass

@app.post("operation/expence")
def add_expence():
    pass
    
    