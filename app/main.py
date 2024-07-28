from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import CustomerModel, LogInModel,UpdatePass,EmailParams,id_clinet,TransferData,verifyCode
from .crud import add_customer,update_customer,checkData, update_password,create_new_bank_account
from .crud import make_transfer
from .crud import get_accounts
from .crud import consultBankAccount
from fastapi.encoders import jsonable_encoder
from .verifyData import verifyDataCI, verifyDataEmail,verifyDataUser, verify_password_requirements
import os
import resend
from .modules.send_email import send_email,preVerifyToSendEmail, prepare_email
from .modules.verifyCode import verifyCodeFunction
import random
from .database import setup_database
from .modules.sendCodeTransfer import prepareEmailTransfer



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await setup_database()

@app.post("/register_user", response_description="Add new customer", response_model=CustomerModel)
async def create_customer(customer: CustomerModel):
    ci,credentials=await verifyDataCI(customer)
    if ci:
        print("entro a actualizar")
        if credentials:
            response=jsonable_encoder({"code":"CI_REPEAT"})
            return JSONResponse(status_code=201, content=response)
        else:        
            if await verifyDataUser(customer):
                response = jsonable_encoder({"code": "USER_REPEAT"})
                return JSONResponse(status_code=201, content=response)
            else:
                update = await update_customer(customer)
                if update:
                    response=jsonable_encoder({"code":"USER_CREATE"})
                    return JSONResponse(status_code=201, content=response)
    else:
        print("entro a agregar nuevo")
        if await verifyDataUser(customer):
            response = jsonable_encoder({"code": "USER_REPEAT"})
            return JSONResponse(status_code=201, content=response)
        elif await verifyDataEmail(customer):
            response = jsonable_encoder({"code": "EMAIL_REPEAT"})
            return JSONResponse(status_code=201, content=response)
        else:
            new_customer,new_account = await add_customer(customer)
            if new_customer:
                response=jsonable_encoder({"code":"USER_CREATE",
                                           "account":new_account})
                return JSONResponse(status_code=201, content=response)
        
                    
        

@app.post("/login", response_model=dict)
async def logIn (Credentials: LogInModel):
    authenticate,bank_accounts,user = await checkData(Credentials)
    id=str(user["_id"])
    name_user=user["name"]+" "+user['lastname']
    user_email=user['email']
    if authenticate:
        if len(bank_accounts)>0:
            response_data = {
                "authenticated": authenticate,
                "code":"HAVE_ACCOUNTS",
                "id":id,
                "accounts_list":bank_accounts,
                "name_user":name_user,
                "user_email":user_email
            }
          
        else:
            response_data = {
            "authenticated": authenticate,
            "code":"NO_HAVE_ACCOUNTS",
           "id":id,
            }
        # Convierte el diccionario en JSON serializable
        response_json = jsonable_encoder(response_data)

        # Devuelve la respuesta como JSONResponse
        return JSONResponse(status_code=201, content=response_json)

#Funcion para cambiar la contraseña
@app.post("/change_password", response_model=dict)
async def change_password(new_data:UpdatePass):
    # Verificar que la nueva contraseña cumpla con los requisitos mínimos
    is_valid, message = verify_password_requirements(new_data.new_password)
    if not is_valid:
        return JSONResponse(status_code=201, content={ "code": "INVALID_NEW_PASSWORD","message":message})

    try:
        result = await update_password(new_data)
        if "code" in result:
            if result["code"] == "INCORRECT_CURRENT_PASSWORD":
                return JSONResponse(status_code=201, content={ "code": "INCORRECT_CURRENT_PASSWORD"})
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    



@app.post("/send_email")
async def send_mail(customer:CustomerModel):
    print("Entro end pint")
    status,response=await preVerifyToSendEmail(customer)
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)



@app.post("/send_email_to_transfer")
async def send_mail(customer_id:EmailParams):
    email=customer_id.email
    print(email)
    print("typoe of",type(email))
    status,response=await prepareEmailTransfer(email)
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)
    
    
   


@app.post("/create_bank_account")
async def send_mail(id: id_clinet):
    account,responce=await create_new_bank_account(id)
    responce['account_number']=account
    responce['balance']=0.0
    responce=jsonable_encoder(responce)
    return JSONResponse(status_code=200, content=responce)
    
    
@app.post("/transfer")
async def transfer(transfer_data:TransferData):
    transfer_data_dict=transfer_data.dict(by_alias=True)
    status,response=await make_transfer(transfer_data_dict)
    if status==200:
        return JSONResponse(status_code=status,content=response)
    else:
        return JSONResponse(status_code=status,content=response)


@app.post("/verify_code_email")
async def verify_code_email(data:verifyCode):
    print(data)
    status, response=await verifyCodeFunction(data,data.parameter)
    response=jsonable_encoder(response)
    return JSONResponse(status_code=status,content=response)
    

@app.get("/client_accounts/{client_id}")
async def get_client_accounts(client_id: str):
    used_data=await get_accounts(client_id)
    response={
        "accounts_list":used_data
    }
    response=jsonable_encoder(response)
    return response


@app.get("/search_bank_account/{bank_account}")
async def get_client_accounts(bank_account:int):
    status, response=await consultBankAccount(bank_account)
    response=jsonable_encoder(response)
    return response
    


@app.post("/recover_password")
async def recover_password(request: EmailParams):
    status, response = await prepare_email(request.email, 1)
    responseJ = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=responseJ)
