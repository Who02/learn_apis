from pydantic import BaseModel, Field, field_validator

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
