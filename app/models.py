from pydantic import BaseModel, EmailStr
from typing import Optional, List
from typing import Union

"""class AddressModel(BaseModel):
    street: str
    city: str
    state: str
    zip: str"""

class CustomerModel(BaseModel):
    name: str
    lastname: str
    #address: AddressModel
    ci:str
    cell: str
    email: EmailStr
    user:str
    password:str
    pass_conf:str
    #accounts: Optional[List[str]] = []

class LogInModel(BaseModel):
    user: str
    password: str
    
class UpdatePass(BaseModel):
    user_id:str
    current_password:str
    new_password:str
    parameter: int

class EmailParams(BaseModel):
    email: EmailStr
    
class id_clinet(BaseModel):
    id: str
    

class TransferData(BaseModel):
    selectedAccount: str
    amount: float
    beneficiary: str
    accountNumber: str
    description: str = None
    notification: str = None


class verifyCode(BaseModel):
    codigo: str
    email: EmailStr
    parameter:int


class payBillModel(BaseModel):
    contract: int
    parameter: int 
    account: int
    beneficiary: str