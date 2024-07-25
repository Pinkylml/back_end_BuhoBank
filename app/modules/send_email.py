import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr
import dns.resolver
from ..database import customer_collection,code_verify_collection, reset_verify_colletion
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from ..models import CustomerModel
from ..verifyData import verifyDataCI, verifyDataEmail,verifyDataUser
import random
import os
import datetime



def send_email(subject, html_body, sender, recipients, password):
    try:
        domain = parseaddr(recipients)[1].split('@')[-1]
        dns.resolver.resolve(domain, 'MX')
        print("DNS OK")
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                res=smtp_server.sendmail(sender, recipients, msg.as_string())
                print("Message sent!",res)
            return 200, {"code":"EMAIL_SEND"}
        except Exception as e:
            print(f"Error in sent email {e}")
            return 200, {"code":"EMAIL_DONT_SEND"}
    except  Exception as e: #(dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print (f"DOMAIN ERROR {e}")
        return 200, {"code":"DOMAIN_DONT_EXIST"}
    

async def save(code,email,collection, parametro):
    if parametro == 0:
        query = {
            "email": email,
            "code":code,
            "attempts":3,
             "time":datetime.datetime.utcnow(),
            "expiresAt": datetime.datetime.utcnow() + datetime.timedelta(minutes=1) 
        }
    elif parametro == 1:
        query = {
            "email": email,
            "code":code,
            "attempts":3,
            "time":datetime.datetime.utcnow(),
            "expiresAt": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # Hora de expiración
        }
    check,user = await CheckIsRegistered(code, email, collection)
    if not check:
        insert_result=await collection.insert_one(query)
        if insert_result.inserted_id:
            return True
        else:
            return False
    else: 
        update_result= await collection.update_one(
            {"email": email},
            {"$set":{
                "code":code,
            "attempts":3,
            "time":datetime.datetime.utcnow(),
            "expiresAt": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # Hora de expiración
            }}
        )
        if update_result.modified_count > 0:
            return True
        else: 
            return False 


async def prepare_email(email, parametro):
    #0 Para registro
    #1 para el reseteo
    code=random.randint(100000, 999999)
    save_flag = ""
    if parametro == 0:
        save_flag=await save(code,email, code_verify_collection, parametro)
        subject = "Código de verificación"
        html_body=f"""
            <html>
                <body>
                    <p>Su código de verificación es:</p>
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
    elif parametro==1:
        check,user_name = await CheckIsRegistered(code, email, customer_collection)
        if check:
            saveResult = await save(code, email, reset_verify_colletion, parametro)
            if saveResult:
                subject = "Código de verificación"
                html_body=f"""
                    <html>
                        <body>
                            <h1>Código para resetear contraseña</h1>
                            <p>Su código de verificación es:</p>
                            <p><strong>{code}</strong></p>
                        </body>
                    </html>
                    """
                sender = "buhobanco@gmail.com"
                recipients = [f"{email}"]
                password =os.getenv('SMTP_APP_PASSWORD_GOOGLE')
                status,response=send_email(subject, html_body, sender, recipients, password)
                response['id']=user_name
                return status, response
            else:
                status=200
                response={"code":"DONT_SAVE_CODE"}
                return status,response
        else:
            status = 200
            response={"code":"EMAIL_DONT_EXIST"}
            return status, response
        
    
async def preVerifyToSendEmail(customer: CustomerModel):
    ci,credentials=await verifyDataCI(customer)
    if ci:
        if credentials:
            response={"code":"CI_REPEAT"}
            return 200,response 
    else:        
        if await verifyDataUser(customer):
            response = {"code": "USER_REPEAT"}
            return 200,response
        else:
            if (await verifyDataEmail(customer)):
                response = {"code": "EMAIL_REPEAT"}
                return 200,response
            else:
                status,response=await prepare_email(customer.email, 0)
                return status,response

async def CheckIsRegistered(code, email, collection):
    result = await collection.find_one({"email": email})
    print(result, "CheckIsRegistered")
    if result:
        return True, str(result['_id'])
    else:
        print("No hay cuenta para agregar cod.")
        return False,None



    


    
  
    


