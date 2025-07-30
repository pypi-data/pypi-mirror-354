import imaplib
import email
from email.header import decode_header

# IMAP 服务器信息
imap_server = "mail.zqhot.top"
username = "9527@zqhot.top"  # 替换为您的邮箱地址
password = "1213wzwz"  # 替换为您的邮箱密码

# 连接到 IMAP 服务器
# mail = imaplib.IMAP4_SSL(imap_server, 143)
mail = imaplib.IMAP4_SSL(imap_server, 993)
mail.login(username, password)

# 选择收件箱
mail.select("inbox")

# 搜索所有邮件
status, messages = mail.search(None, "ALL")
if status != "OK":
    print("无法搜索邮件")
    exit()

# 获取邮件 ID 列表
messages = messages[0].split()

# 遍历邮件
for mail_id in messages:
    res, msg = mail.fetch(mail_id, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # 解析邮件内容
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            from_ = msg.get("From")
            print(f"邮件主题: {subject}")
            print(f"发件人: {from_}")

            print('\n\n\n\n')
            # 打印邮件正文
            # if msg.is_multipart():
            #     for part in msg.walk():
            #         content_type = part.get_content_type()
            #         content_disposition = str(part.get("Content-Disposition"))
            #         if content_type == "text/plain" and "attachment" not in content_disposition:
            #             body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
            #             print(f"邮件正文: {body}")
            # else:
            #     body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
            #     print(f"邮件正文: {body}")

# 登出
mail.logout()
