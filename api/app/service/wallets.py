from fastapi import  HTTPException
from app.repository import wallets as wallets_service
from app.schemas import CreateWalletRequest

def get_balance(wallet_name: str | None = None):
    if not wallet_name:
        wallets=wallets_service.get_all_wallets()
        return {"total balance": sum(wallets.values())}
    
    if not wallets_service.is_wallet_exist(wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
        
    return f"Wallet: {wallet_name}, balance: {wallets_service.get_balance(wallet_name)}"

def create_wallet(wallet: CreateWalletRequest):
    if wallets_service.is_wallet_exist(wallet.name):
        raise HTTPException(
            status_code=404, 
            detail=f"wallet {wallet.name} already exist"
            )
    
    new_balbance = wallets_service.create_wallet(wallet.name, wallet.initial_balance)
    
    return {f"Wallet {wallet.name} created",
            f"wallet: {wallet.name}, balance {new_balbance}"}
