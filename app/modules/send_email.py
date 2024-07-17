import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr
import dns.resolver


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
    
  
    


