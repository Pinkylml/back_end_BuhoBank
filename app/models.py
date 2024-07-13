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

class EmailParams(BaseModel):
    from_email: EmailStr
    to: List[EmailStr]
    subject: str
    html: str