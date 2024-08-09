from ..models import payBillModel
from ..database import account_collection, customer_collection
import httpx
from datetime import datetime

#Funciones auxiliares
#Funcion para obtener el monto. 
async def getAmount(number_account, param):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://back-endfacturas.onrender.com/get_bill_amount/{number_account}/{param}")
        response_data = response.json()
        monto = response_data.get("monto")
        print(monto)
        return monto

#Funcion para registrar el pago realizado al la cuenta de servicios


async def checkPaid(contratc, params):
    contratcDic = {
            "account_number": contratc,
            "type_params": str(params)
        }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://back-endfacturas.onrender.com/checkPaid/", json=contratcDic)
        response_data = response.json()
        code = response_data.get("Code")
        print(code)
        return code
        
def getServices(params):
    if params == 0:
        return "Luz"
    elif params == 1:
        return "Agua"
    elif params == 2:
        return "Internet"
    elif params == 3:
        return "Telefonia fija"

async def DoPay(account_source,  contract, amount, params):
    #Buscar cuenta y sacar balance
    services_str = getServices(params)
    search_account_src = await account_collection.find_one({"account_number": account_source})
    if search_account_src:
        balance = search_account_src.get("balance")
        if balance < amount:
            return {"code": "fondos insuficientes"}
        else: 
            #realizar transferencia
            search1 = await customer_collection.find_one({"email":"serviciosbuhobanco@gmail.com"})
            if search1: 
                account_dest = search1.get("accounts")[0]
                search_account_dest = await account_collection.find_one({"account_number": account_dest})
                #Ahora que tenemos los datos de la cuenta de destino y la de origen, procedemos a realizar la transferencia
                filter_source = {"account_number": int(search_account_src.get("account_number"))}
                filter_destiny = {"account_number": int(search_account_dest.get("account_number"))}
                new_balance_dest = search_account_dest.get("balance") + amount
                new_balance_src = search_account_src.get("balance") - amount
                fecha_movimiento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_movement_src = {
                    "fecha_movimiento": fecha_movimiento,
                    "saldo_entra": 0.0,
                    "saldo_sale": amount,
                    "saldo_anterior": (search_account_src.get("balance")),
                    "saldo_resultante": search_account_src.get("balance") - amount,
                    "cuenta_origen": int(search_account_src.get("account_number")),
                    "cuenta_destino": int(search_account_dest.get("account_number")),
                    "Descripcion": f"Pago de servicios básicos: {services_str}" 
 
                }
                new_movement_dest = {
                     "fecha_movimiento": fecha_movimiento,
                    "saldo_entra": amount,
                    "saldo_sale": 0.0,
                    "saldo_anterior": (search_account_dest.get("balance")),
                    "saldo_resultante": search_account_dest.get("balance") + amount,
                    "cuenta_origen": int(search_account_src.get("account_number")),
                    "cuenta_destino": int(search_account_dest.get("account_number")),
                    "Descripcion": f"Pago de servicios básicos: {services_str}" 
                }
                update_source={
                    "$set":{"balance":new_balance_src},
                    "$push":{"movements":new_movement_src}
                }
                update_destination={
                    "$set":{"balance":new_balance_dest},
                    "$push":{"movements":new_movement_dest}
                }
                result1 = await account_collection.update_one(filter_source, update_source)
                result2 = await account_collection.update_one(filter_destiny, update_destination)
                if result1.modified_count>0 and result2.modified_count>0:
                    checkPaidResult = await checkPaid(contract, params)
                    print (checkPaidResult)
                    if checkPaidResult == "Pago exitoso y factura registrada":    
                        return {"code": "PAY_TAX_SUCCESFUL"}
                    else: 
                        return {"code": "JUST_TRANSFER_MADE_CHECK_SYSTEM"}
                else:
                    return {"code": "DATABASE_ERROR"}
            else:
                return {"code": "NOT_FOUND_ACCOUNT"}

#Funciones que toma el end-point
async def payBill(request:payBillModel):
    contract = request.contract
    params = request.parameter
    #consigo el monto a Pagar
    amount = await getAmount(contract, params)
    #Realizar el pago
    account = request.account
    response = await DoPay(account, contract, amount, params)
    return 200, response