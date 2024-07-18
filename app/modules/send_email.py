import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr
import dns.resolver
from ..database import customer_collection,account_collection,code_verify_collection
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from ..models import CustomerModel
from ..verifyData import verifyDataCI, verifyDataEmail,verifyDataUser
import random
import os


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
            return 500, {"code":"EMAIL_DONT_SEND"}
    except  Exception as e: #(dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print (f"DOMAIN ERROR {e}")
        return 400, {"code":"EMAIL_DONT_EXIST"}
    

async def save(code,email):
    query = {
        "email": email,
        "code":code
    }
    insert_result=code_verify_collection.insert_one(query)
    if insert_result.inserted_id:
        return True
    else:
        return False
    
async def prepare_email(email):
    code=random.randint(100000, 999999)
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
    #save_flag=await save(code,email)
    #if save_flag:
    status,response=send_email(subject, html_body, sender, recipients, password)
    #else:
      #  status=200
       # response={"code":"DONT_SAVE_CODE"}

    return status,response
    
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
                status,response=await prepare_email(customer.email)
                return status,response




    


    
  
    


