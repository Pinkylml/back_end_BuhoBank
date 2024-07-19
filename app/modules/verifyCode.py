from ..database import code_verify_collection
from ..models import verifyCode


async def getData(email):
    query={
        "email":email        
    }
    
    result_data=await code_verify_collection.find_one(query)
    if result_data is None:
        return False
    else:
        return result_data
    

async def deleteData(email):
    query={
        "email":email 
           
    }
    
    result_data=await code_verify_collection.delete_one(query)
    if result_data.deleted_count == 1:
        return True
    else:
        return False
    
async def updateAttempts(email,attemps):
    await code_verify_collection.update_one(
        {"email":email },
        {"$set": {"attempts": attemps}}
        
    )

    

async def verifyCodeFunction (data:verifyCode)->dict:
    data_flag=await getData(data.email)
    print("En verificar el codigo",data_flag)
    if data_flag:
        save_code=data_flag['code']
        get_code=data.codigo
        get_code=int(get_code)
        if save_code==get_code:
            delete_flag=await deleteData(data.email)
            if delete_flag:
                return 200, {"code":"SUCCESS"}
            else:
                return 200, {"code":"DELETE_NO_SUCCESS"}
        else:
            #attemps=data_flag['attempts']
            attempts = data_flag['attempts']
            attempts=attempts-1
            if attempts==0:
                delete_flag=await deleteData(data.email)
            else:
                await updateAttempts(data.email,attempts)
            return 200, {"code":"NO_SUCCESS"}