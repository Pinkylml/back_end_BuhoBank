from .database import customer_collection
from .models import CustomerModel
import re
async def verifyDataCI(customer_data: CustomerModel) -> dict:
    query = {
        "ci": customer_data.ci
    }
    user_data= await customer_collection.find_one(query)
    print("en verugudataCI  \n",type(user_data))
    print(user_data)
    
    if user_data is None:
        return False,False
    else:
        credentials=verifyCredentias(user_data)
        return True,credentials


#para el nombre de usuario repetido
async def verifyDataUser(customer_data: CustomerModel) -> bool:
    query = {
        "user": customer_data.user
    }
    user_data = await customer_collection.find_one(query)
    if user_data is None:
        return False
    else:
        return True



#para el correo electronico repetido 
async def verifyDataEmail(customer_data: CustomerModel) -> bool:
    query = {
        "email": customer_data.email
    }
    user_data = await customer_collection.find_one(query)
    if user_data is None:
        return False
    else:
        return True
    
    
def verifyCredentias(user_data):
    user=user_data['user']
    print("el dicc: ",user)
    if user_data['user']:
        print(user_data['user'])
        return True
    else:
        print("El usuario no tiene  creada las credenciales")
        return False
    
#Requisitos para el cambio de contraseña nueva.
def verify_password_requirements(password: str) -> bool:
    # Requisitos mínimos: al menos 8 caracteres, una letra mayúscula, una letra minúscula, un dígito y un carácter especial
    if len(password) < 8:
        return False, "INVALID_PASSWORD_LENGTH"
    if not re.search(r"[A-Z]", password):
        return False,"MISSING_UPPERCASE"
    if not re.search(r"[a-z]", password):
        return False, "MISSING_LOWERCASE"
    if not re.search(r"\d", password):
        return False, "MISSING_DIGIT"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "MISSING_SPECIAL_CHARACTER"
    return True, "VALID_PASSWORD"
    

    

