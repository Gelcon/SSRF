# @Author: Gelcon.
# @Date: 2023/4/5 22:38

import re
import requests
import socket


def check_ssrff(url):
    # 使用正则表达式匹配URL中的参数
    params = re.findall(r"\?(.*?)=", url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    try:
        for param in params:
            # 将参数作为目标地址发起请求
            target_url = url.replace(param, 'http://example.com/')
            res = requests.get(target_url, headers=headers, timeout=5)
            if res.status_code == 200:
                # 检查返回的内容是否包含敏感信息
                if 'internal_server_error' in res.text.lower():
                    return True
        # 对URL中可能存在的协议头进行检测
        if url.startswith(('file://', 'ftp://', 'dict://', 'gopher://', 'telnet://')):
            return True
        # 对URL中可能存在的IP地址进行检测
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', url):
            return True
        # 对URL中可能存在的域名进行DNS解析
        else:
            domain = url.split('/')[2]
            try:
                ip = socket.gethostbyname(domain)
                if ip != domain:
                    return True
            except:
                pass
    except:
        pass
    return False
