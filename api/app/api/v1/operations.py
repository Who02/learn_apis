from fastapi import APIRouter
from app.service import operations as operation_service
from app.schemas import OperationRequest

router=APIRouter()

@router.post("/operation/income")
def add_income(operation: OperationRequest):
    return operation_service.add_income(operation)

@router.post("operation/expence")
def add_expence(operation: OperationRequest):
    return operation_service.add_expence(operation)
