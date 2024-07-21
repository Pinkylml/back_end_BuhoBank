from ..database import code_verify_collection,reset_verify_colletion
from ..models import verifyCode


async def getData(email,collection):
    query={
        "email":email        
    }
    
    result_data=await collection.find_one(query)
    if result_data is None:
        return False
    else:
        return result_data
    

async def deleteData(email,collection):
    query={
        "email":email 
           
    }
    
    result_data=await collection.delete_one(query)
    if result_data.deleted_count == 1:
        return True
    else:
        return False
    
async def updateAttempts(email,attemps,collection):
    await collection.update_one(
        {"email":email },
        {"$set": {"attempts": attemps}}
        
    )

    

async def verifyCodeFunction (data:verifyCode,parametro)->dict:
    #parametro 0  para registro
    # parametro 1 para reseteo
    if parametro==0:
        data_flag=await getData(data.email,code_verify_collection)
        print("En verificar el codigo",data_flag)
        if data_flag:
            save_code=data_flag['code']
            get_code=data.codigo
            get_code=int(get_code)
            if save_code==get_code:
                delete_flag=await deleteData(data.email,code_verify_collection)
                if delete_flag:
                    return 200, {"code":"SUCCESS"}
                else:
                    return 200, {"code":"DELETE_NO_SUCCESS"}
            else:
                #attemps=data_flag['attempts']
                attempts = data_flag['attempts']
                attempts=attempts-1
                if attempts==0:
                    delete_flag=await deleteData(data.email,code_verify_collection)
                else:
                    await updateAttempts(data.email,attempts,code_verify_collection)
                return 200, {"code":"NO_SUCCESS"}
        else:
            return 200, {"code":"TIME_OUT"}
    elif parametro==1:
        data_flag=await getData(data.email,reset_verify_colletion)
        print("En verificar el codigo",data_flag)
        if data_flag:
            save_code=data_flag['code']
            get_code=data.codigo
            get_code=int(get_code)
            if save_code==get_code:
                delete_flag=await deleteData(data.email,reset_verify_colletion)
                if delete_flag:
                    return 200, {"code":"SUCCESS"}
                else:
                    return 200, {"code":"DELETE_NO_SUCCESS"}
            else:
                #attemps=data_flag['attempts']
                attempts = data_flag['attempts']
                attempts=attempts-1
                if attempts==0:
                    delete_flag=await deleteData(data.email,reset_verify_colletion)
                else:
                    await updateAttempts(data.email,attempts,reset_verify_colletion)
                return 200, {"code":"NO_SUCCESS"}
        else:
            return 200, {"code":"TIME_OUT"}
            