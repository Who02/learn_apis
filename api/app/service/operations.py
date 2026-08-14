from fastapi import HTTPException
from app import schemas as OperationRequest
from app.repository import wallets as wallets_repository

def add_income(operation: OperationRequest):
    if wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
                status_code=404,
                detail=f"Wallet {operation.wallet_name} not found"
            )
    
    new_balance=wallets_repository.add_income(operation.wallet_name, operation.amount)
    
    return {
        "message": "income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }
    
def add_expence(operation: OperationRequest):
    if wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    if operation.amount <=0: 
        raise HTTPException(
            status_code=400,
            detail=f"amount must be positive"
        )
    if operation.amount >wallets_repository.get_balance(operation.wallet_name):
        raise HTTPException(
            status_code=400,
            detail=f"amount must be less than balance"
        )
    new_balance=wallets_repository.add_expence(operation.wallet_name, operation.amount)
    return {
        "message": "expence added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }
