from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import CustomerModel, LogInModel,UpdatePass
from .crud import add_customer,update_customer,checkData, update_password
from fastapi.encoders import jsonable_encoder
from .verifyData import verifyDataCI, verifyDataEmail,verifyDataUser, verify_password_requirements



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


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
            new_customer = await add_customer(customer)
            if new_customer:
                response=jsonable_encoder({"code":"USER_CREATE"})
                return JSONResponse(status_code=201, content=response)
        
                    
        

@app.post("/login", response_model=dict)
async def logIn (Credentials: LogInModel):
    authenticate,bank_accounts = await checkData(Credentials)
    if authenticate:
        if len(bank_accounts)>0:
            response_data = {
                "authenticated": authenticate,
                "code":"HAVE_ACCOUNTS",
                "accounts_list":bank_accounts
            }
          
        else:
           
            response_data = {
            "authenticated": authenticate,
            "code":"NO_HAVE_ACCOUNTS"
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
        return JSONResponse(status_code=400, content={ "code": "INVALID_NEW_PASSWORD",message:"code "})

    try:
        result = await update_password(new_data)
        if "code" in result:
            if result["code"] == "INCORRECT_CURRENT_PASSWORD":
                return JSONResponse(status_code=400, content={ "code": "INCORRECT_CURRENT_PASSWORD"})
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})