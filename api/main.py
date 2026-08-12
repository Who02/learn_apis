from fastapi import FastAPI
from fastapi.responses import Response
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
app = FastAPI()
class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str| None = Field(None, max_length=255)
    @field_validator("amount")
    def amount_must_be_positive(cls, v: float)->float:
        if v<=0: raise ValueError("amount must be positive")
        return v
    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, n: str)->str:
        n=n.strip
        if not n: raise ValueError("name is empty")
        return n
        
class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0
    @field_validator("name")
    def name_not_empty(cls, n: str)->str:
        n=n.strip
        if not n: raise ValueError("name is empty")
        return n
    @field_validator("initial_balance")
    def balance_not_negative(cls, v: float)->float:
        if v< 0: raise ValueError("initial_balance cannot be negative")
        return v
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

@app.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    if wallet.name in BALANCE: 
        raise HTTPException(status_code=404, 
                            detail=f"wallet {wallet.name} already exist")
    BALANCE[wallet.name]=wallet.initial_balance
    return {f"Wallet {wallet.name} created",
            f"wallet: {wallet.name}, balance {wallet.initial_balance}"}
    
@app.post("/operation/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    BALANCE[operation.wallet_name]+=operation.amount
    return {
        "message": "income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount
    }

@app.post("operation/expence")
def add_expence(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    if operation.amount <=0: 
        raise HTTPException(
            status_code=400,
            detail=f"amount must be positive"
        )
    if operation.amount >BALANCE[operation.wallet_name]:
        raise HTTPException(
            status_code=400,
            detail=f"amount must be less than balance"
        )
    BALANCE[operation.wallet_name]-=operation.amount
    return {
        "message": "expence added",
        "wallet": operation.wallet_name,
        "amount": operation.amount
    }
    
    
    