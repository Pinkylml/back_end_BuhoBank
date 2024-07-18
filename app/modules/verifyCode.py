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

async def verifyCodeFunction (data:verifyCode)->dict:
    data_flag=await getData(data.email)
    if data_flag:
        save_code=data_flag['code']
        get_code=data.codigo
        get_code=int(get_code)
        if save_code==get_code:
            return 200, {"code":"SUCCESS"}
        else:
            return 200, {"code":"NO_SUCCESS"}