import requests
# 需要更新这里的 cookie
cookies = {
    'roundcube_sessid': 'namt75hctamoltk8935bk5s9qr',
    'roundcube_sessauth': 'R1MuLjJKcUNnx6XYUcO6MunhRY-1747620000',
    'PHPSESSID': 'vhklu6aklfj9edb1a0jsdu6oil',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://45.82.244.67',
    'Pragma': 'no-cache',
    'Referer': 'https://45.82.244.67/admin/box/new?domain=undefined',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'show': 'true',
}

for i in range(9531, 10000):
    data = {
        'name': str(i),
        'user': str(i),
        'domain': 'socks5ho.me',
        'passwordPlaintext': '1213wzwz',
    }

    response = requests.post(
        'https://45.82.244.67/admin/box/new',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    print(response.status_code)


    