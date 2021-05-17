from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SENDER = "livroparatodxs@outlook.com"
PASSWORD = "zFD9L2Y@bRt5"
 
class MailControl:
    def send_mail(self, receiver:str, title:str, message:str) -> bool:
        try:
            msg = MIMEMultipart()
            message = message
            msg['From'] = SENDER
            msg['To'] = receiver
            msg['Subject'] = title
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('SMTP.office365.com: 587')
            server.starttls()
            server.login(msg['From'], PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
        except:
            return False
        return True