from .send_email import send_email,save
import random
from ..database import code_transfer_collection
import os

async def prepareEmailTransfer(email):
    code=random.randint(100000, 999999)
    save_flag=await save(code,email,code_transfer_collection,0)
    subject = "Código para realizar transferencia"
    html_body=f"""
        <html>
            <body>
                <h1>Código de transferencia</h1>
                <p>Ingrese el siguiente código en la página para realizar su transferencia</p>
                <br>
                <p><strong>{code}</strong></p>
            </body>
        </html>
        """
    sender = "buhobanco@gmail.com"
    recipients = [f"{email}"]
    password =os.getenv('SMTP_APP_PASSWORD_GOOGLE')
    if save_flag:
        status,response=send_email(subject, html_body, sender, recipients, password)
        return status,response
    else:
        status=200
        response={"code":"DONT_SAVE_CODE"}
        return status,response
    
    
    