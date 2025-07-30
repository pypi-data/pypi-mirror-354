import requests
# 忽略告警
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {
    'colorMode': 'dark',
    'roundcube_sessid': 'le0fikjknht1c9u0n23si25mi5',
    'PHPSESSID': '9030nf5nu93vule87pc1pcek7r',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://47.57.245.253',
    'Referer': 'https://47.57.245.253/admin/box/new?domain=',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'colorMode=dark; roundcube_sessid=vppj8d0c38hgnbka4j1dqb49bd; roundcube_sessauth=pCyCaMtC0vPR0n52Fq5xGt3VCM-1746009000; PHPSESSID=sts82kb2v4ur4jhu0asba7hguh',
}
params = {
    'show': 'true',
}


import random
import requests

# 常见英文名字
first_names = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Elijah', 'Charlotte', 'James', 'Amelia', 'Oliver',
               'Sophia', 'Lucas', 'Isabella', 'Mason', 'Mia', 'Logan', 'Harper', 'Ethan', 'Luna', 'Jackson']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

# 常见昵称或简写组合
nicknames = ['alex', 'chris', 'david', 'mike', 'jess', 'sam', 'tom', 'lisa', 'anna', 'nina', 'ben', 'kate']

# 用于拼接的后缀
suffixes = ['', '1', '12', '01', '07', '2000', '99', '_', '_x', '__', '.', '.cool', '.official']

# 构建一个生成器函数
def generate_username():
    choice = random.random()
    if choice < 0.4:
        # 姓+名首字母+数字：e.g. SmithJ12
        return f"{random.choice(last_names)}{random.choice([name[0] for name in first_names])}{random.choice(suffixes)}"
    elif choice < 0.7:
        # 小写昵称+数字：e.g. chris_07
        return f"{random.choice(nicknames)}{random.choice(suffixes)}"
    else:
        # 名.姓：e.g. olivia.smith 或 jackson.martin1
        return f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}{random.choice(suffixes[:5])}"

# 生成 100 个唯一用户名
used_users = set()
users = []

while len(users) < 100:
    user = generate_username()
    if user not in used_users:
        user=str(user).lower()
        users.append(user)
        used_users.add(user)
for i in range(1, 10):
    data = {
        'name': users[i],
        'user': users[i],
        'domain': 'zqhot.top',
        'passwordPlaintext': '1213wzwz',
    }
#  InsecureRequestWarning: Unverified HTTPS request is being made to host '47.57.245.253'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
#   warnings.warn(
# /Users/wzq/miniforge3/lib/python3.9/site-packages/urllib3/connectionpool.py:1097: Insecur
    
    response = requests.post(
        'https://47.57.245.253/admin/box/new',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    print(f"{users[i]}@zqhot.top")

"""





"""
