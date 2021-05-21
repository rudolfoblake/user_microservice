from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import config

class MailControl:
    def send_mail(self, receiver:str, title:str, message:str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = config.SENDER
            msg['To'] = receiver
            msg['Subject'] = title
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('SMTP.office365.com: 587')
            server.starttls()
            server.login(msg['From'], config.PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
        except:
            return False
        return True