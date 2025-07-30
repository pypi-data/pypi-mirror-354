


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件服务器信息
smtp_server = "mail.socks5ho.me"
smtp_server = "45.82.244.67"
smtp_port = 587  # 或者是465，取决于你的邮件服务器配置
smtp_username = "admin@socks5ho.me"  # 替换为您的邮箱地址
smtp_password = "1213wzwz"  # 替换为您的邮箱密码

to_email = '1781591279@qq.com'
# 创建一个MIMEMultipart对象来构建邮件
msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = to_email  # 替换为收件人的邮箱地址
msg['Subject'] = "你好这是测试邮件来自海外"

body = "This is a test email sent from Python."
msg.attach(MIMEText(body, 'plain'))

# 连接到SMTP服务器并发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # 启用TLS加密
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(smtp_username,to_email, text)
    print("邮件发送成功")
except Exception as e:
    print(f"邮件发送失败: {e}")
finally:
    server.quit()
