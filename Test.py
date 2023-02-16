# @Author: Gelcon.
# @Date: 2023/2/16 14:39

raw = """POST /minio/webrpc HTTP/1.1
Host: 139.224.49.113:9000
Content-Length: 97
x-amz-date: 20221128T032543Z
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://139.224.49.113:9000
Referer: http://139.224.49.113:9000/minio/login
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

{"id":1,"jsonrpc":"2.0","params":{"username":"minio","password":"minio123"},"method":"web.Login"}"""

raws = raw.splitlines()
print('raw: ')
print(raws)
