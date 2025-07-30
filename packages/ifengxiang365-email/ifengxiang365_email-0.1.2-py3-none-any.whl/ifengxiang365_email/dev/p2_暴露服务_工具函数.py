import requests 
import time
import datetime

# 禁止告警   
import warnings
warnings.filterwarnings("ignore")
from dateutil import parser
def timestamp_to_readable(timestamp):
    import datetime    
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    readable = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return readable

def _get_cookie(mxdomain):

    import requests
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://email.ifengxiang365.com',
        'Pragma': 'no-cache',
        'Referer': 'https://email.ifengxiang365.com/admin/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        # 'Cookie': 'PHPSESSID=c28rk20r3fdahq0sj9mt5k6963',
    }
    url = f'https://{mxdomain}/admin/login'
    res = requests.get(url, verify=False, headers=headers)
    old_cookies = requests.utils.dict_from_cookiejar(res.cookies)
    _csrf_token = res.text.split('_csrf_token" value="')[1].split('"')[0]
 
    data = {
        'email': 'admin@ifengxiang365.com',
        'password': '1213wzwz',
        '_csrf_token': _csrf_token,
        '_remember_me': 'on',

    }

    response = requests.post('https://email.ifengxiang365.com/admin/login', cookies=old_cookies, headers=headers, data=data, verify=False,allow_redirects=True)
    # cookies = requests.utils.dict_from_cookiejar(response.cookies)
    cookies = requests.utils.dict_from_cookiejar(response.history[0].cookies)
    old_PHPSESSID=old_cookies['PHPSESSID']
    new_PHPSESSID=cookies['PHPSESSID']
    print(old_PHPSESSID,'---->',new_PHPSESSID)
    return cookies
    cookies = {
        'roundcube_sessid': 'namt75hctamoltk8935bk5s9qr',
        'roundcube_sessauth': 'R1MuLjJKcUNnx6XYUcO6MunhRY-1747620000',
        'PHPSESSID': 'vhklu6aklfj9edb1a0jsdu6oil',
    }

def create_email(domain,mxdomain,mxdomain_ip,create_num=1):
    cookies = _get_cookie(mxdomain)
    headers = {}

    params = {
        'show': 'true',
    }
    new_emails = []
    for i in range(int(time.time()), int(time.time())+create_num):
        data = {
            'name': str(i),
            'user': str(i),
            'domain': domain,
            'passwordPlaintext': '1213wzwz',
        }
        response = requests.post(
            f'https://{mxdomain_ip}/admin/box/new',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )
        new_emails.append(f'{i}@{domain} === 1213wzwz')
    return new_emails

def change_email_password(mxdomain_ip,email_account,email_new_password):
    try:
        cookies = _get_cookie(mxdomain_ip)
        headers = {}
   
        data = {
            'passwordPlaintext': email_new_password,
        }

        response = requests.post(
            f'https://{mxdomain_ip}/admin/box/{email_account}/password',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )
        print(response.status_code)
        return True,f'{email_account} === {email_new_password} 修改密码成功'
    except Exception as e:
        return False, str(e)

def _find_email_have_created(mxdomain_ip,email_accout,cookies):

    headers = {
    }

    params = {
        'query': email_accout,
        'ajax': 'true',
    }

    response = requests.get(f'https://{mxdomain_ip}/admin/box/', params=params, cookies=cookies, headers=headers, verify=False)
    if 'No email found, please create one' in response.text:
        return True
    return False

def create_email_accout_password(domain,mxdomain,mxdomain_ip,email_account,email_password):
    try:
        email_account = email_account.split('@')[0]
        cookies = _get_cookie(mxdomain_ip)
        headers = {}

        params = {
            'show': 'true',
        }
        data = {
            'name': email_account,
            'user': email_account,
            'domain': domain,
            'passwordPlaintext': email_password,
        }
        can_create = _find_email_have_created(mxdomain_ip,email_account,cookies)
        if not can_create:
            return False,f'{email_account}@{domain} 已经创建 无法继续创建'

        response = requests.post(
            f'https://{mxdomain_ip}/admin/box/new',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )
        print(response.status_code)
        return True,f'{email_account}@{domain}==={email_password} 创建成功'
    except Exception as e:
        return False, str(e)

def get_email(mxdomain,mxdomain_ip,email_account,email_password):
    import imaplib
    import email
    from email.header import decode_header

    # IMAP 服务器信息
    imap_server = mxdomain_ip
    username = email_account            # 替换为您的邮箱地址
    password = email_password           # 替换为您的邮箱密码

    # 连接到 IMAP 服务器
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
    res_emails = []
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
                # print(f"发件人: {from_}")
                # print('\n\n\n\n')
                if msg.is_multipart():
                    body = ""
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body+= part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                else:
                    body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
                # print(f"邮件正文: {body}")
                # 获取邮件的接收时间
                date = msg.get("Date")
                # 'Wed, 11 Jun 2025 11:26:41 +0800' 转成 可读格式  还有这种格式 date 'Wed, 11 Jun 2025 15:00:35 +0800 (CST)' 

                # 示例日期字符串（包含时区名称）
                dt = parser.parse(date)  # 自动识别时区并解析
                email_timestamp = dt.timestamp()
                # print("可读时间:", readable_time)
                # print(f"接收时间: {date}")
                res_emails.append([subject,from_,body,email_timestamp])
    mail.logout()
    now = int(time.time())

    # 过滤邮件 就是超过 30 分钟
    fliter_res_emails = [i for i in res_emails if (now-i[3])<20*60]
    
    # 修改为可读时间
    for i in fliter_res_emails:
        i[3] = timestamp_to_readable(i[3])
    
    info = f"该邮箱总共收到 {len(res_emails)}个邮件;  过滤出最近 20 分钟的邮件后,数量还剩余 {len(fliter_res_emails)}"
    count = len(res_emails)
    filter_count = len(fliter_res_emails)
    data_res = {
        "emails"  : fliter_res_emails,
        "filter_count":filter_count,
        "count":count,
        "info":info,
    }
    return data_res


def send_mail(mxdomain,mxdomain_ip,email_account,email_password,to_email, title,content):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtp_server = mxdomain_ip
    smtp_port = 587  # 或者是465，取决于你的邮件服务器配置
    smtp_username = email_account  # 替换为您的邮箱地址
    smtp_password = email_password  # 替换为您的邮箱密码

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email  # 替换为收件人的邮箱地址
    msg['Subject'] =title

    body = content
    msg.attach(MIMEText(body, 'plain'))

    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username,to_email, text)
        print("邮件发送成功")
        return True,'邮件发送成功'
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False,f"邮件发送失败: {e}"
    finally:
        server.quit()

if __name__ == '__main__':
    res = create_email_accout_password('ifengxiang365.com', 'email.ifengxiang365.com','47.83.16.21','wyj12','1213wzwz')
    print(res)

    # print(create_email('ifengxiang365.com', 'email.ifengxiang365.com','47.83.16.21'))

    # res = get_email('ifengxiang365.com', 'email.ifengxiang365.com','47.83.16.21','1749612127@ifengxiang365.com','1213wzwz')
    # print(res)

    res = send_mail('email.ifengxiang365.com','47.83.16.21','wyj12@ifengxiang365.com','1213wzwz','1781591279@qq.com','测试邮件','测试邮件')
    print(res)