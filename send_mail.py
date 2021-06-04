import smtplib
from email.mime.text import MIMEText

def send_mail():
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '6e9416bd5bcef0'
    password = 'bd0f440da17f03'
    message = f"<h6>Test Message</h6>"

    sender_email = 'email@example1.com'
    reciever_email = 'mr.adumatta@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'The Nefertiti Project'
    msg['From'] = sender_email
    msg['To'] = reciever_email

    #send Email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, reciever_email, msg.as_string())