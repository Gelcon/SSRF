# @Author: Gelcon.
# @Date: 2023/4/2 16:13

# import socket
# from datetime import datetime
# from time import sleep
#
# MAX_BYTES = 65535
#
#
# def send(hostname, port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.sendto("Start Sending Message".encode('ascii'), (hostname, port))
#     print(f"The OS assigned me the address {sock.getsockname()}")
#     while True:
#         text = f'Message, The time is {datetime.now()}'
#         data = text.encode('ascii')
#         sock.sendto(data, (hostname, port))
#         sleep(1)
#
#
# if __name__ == '__main__':
#     # send('127.0.0.1', 888)
#     send('192.168.32.128', 888)

import requests

# POST /minio/webrpc HTTP/1.1
# Host: 139.224.49.113:888
# Content-Length: 74
# x-amz-date: 20221128T032543Z
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36
# Content-Type: application/json
# Accept: */*
# Origin: http://192.168.32.128:9000
# Referer: http://192.168.32.128:9000/minio/login
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.9
# Connection: close
#
# {"id":1,"jsonrpc":"2.0","params":{"token":"test"},"method":"web.LoginSTS"}

# url = 'http://192.168.32.128:9000/minio/webrpc'
# headers = {
#     'Host': '139.224.49.113:888',
#     'Content-Length': '74',
#     'x-amz-date': '20221128T032543Z',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
#     'Content-Type': 'application/json',
#     'Accept': '*/*',
#     'Origin': 'http://192.168.32.128:9000',
#     'Referer': 'http://192.168.32.128:9000/minio/login',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'close',
# }
# data = '{"id":1,"jsonrpc":"2.0","params":{"token":"test"},"method":"web.LoginSTS"}'
# response = requests.post(url, headers=headers, data=data)
# print(response.content)

url = 'http://139.224.49.113:888'
res = requests.get(url)
print(res.content)
