import smtplib
from email.mime.text import MIMEText

def send_email(subject, content):
     passwd = 'PASSWORD'
     host = 'smtp.exmail.qq.com'
     username = 'sender'
     send_to = ['reciver',]
     msg = MIMEText(content, _subtype = 'html', _charset = 'utf8')
     msg['From'] = username
     msg['Subject'] = subject
     msg['To'] = ",".join(send_to)
     try:
         s = smtplib.SMTP_SSL(host,465)
         s.login(username, passwd )
         s.sendmail(username, send_to,msg.as_string())
         s.close()
     except Exception as e:
         print('Exception: send email failed', e)

if __name__ == "__main__":
    send_email("title", "<h1>content</h1><a href='baidu.com'>link</a>")
