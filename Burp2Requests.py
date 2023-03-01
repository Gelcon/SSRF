# @Author: Gelcon.
# @Date: 2023/2/16 10:13

"""
本文件功能：
处理BurpSuite格式的请求
"""


class SSRFRequests(object):

    def __init__(self, raw: str):
        self.raw = raw
        self.request_info = None
        # 处理raw，将其解析得到请求信息
        self.get_request_info()

    # 将BurpSuite格式的请求转换为字典等信息
    def get_request_info(self, **kwargs):
        raw = self.raw.strip()
        # Key值不存在则返回None
        # proxy = kwargs.get("proxy", None)
        real_host = kwargs.get("real_host", None)
        ssl = kwargs.get("ssl", False)
        # location = kwargs.get("location", True)

        scheme = 'http'
        port = 80
        if ssl:
            scheme = 'https'
            port = 443

        try:
            # 查找子串第一次出现的位置，若找不到，则抛出异常
            index = raw.index('\n')
        except ValueError:
            raise Exception("ValueError")
        # log = {}
        try:
            # :index表示到换行为止，也就是第一行按空格分割
            # 得到请求方式，请求路径，协议
            method, path, protocol = raw[:index].split(" ")
        except:
            raise Exception("Protocol format error")
        # 除了第一行的其他内容
        raw = raw[index + 1:]

        try:
            host_start = raw.index("Host: ")
            # 从下标host_start开始找，得到host_end
            # str.index(str, beg=0 end=len(string))
            host_end = raw.index('\n', host_start)

        except ValueError:
            raise ValueError("Host headers not found")

        if real_host:
            host = real_host
            if ":" in real_host:
                # 分割得到主机、端口号
                host, port = real_host.split(":")
        else:
            # 否则，从字符串中读取到主机号host
            host = raw[host_start + len("Host: "):host_end]
            if ":" in host:
                host, port = host.split(":")
        # splitlines返回一个字符串的所有行
        raws = raw.splitlines()
        headers = {}

        index = 0
        for r in raws:
            # 请求头和请求体之间有空行，所以请求头遍历结束的标志是splitlines分割得到的''
            if r == "":
                break
            # 若不为空串
            try:
                # 有: 就对应k和v
                k, v = r.split(": ")
            except:
                # split方法，若字符串中没有分隔符，则把整个字符串作为列表的一个元素
                k = r
                v = ""
            # 设置到headers中
            headers[k] = v
            index += 1
        headers["Connection"] = "close"
        print('headers:')
        print(headers)
        # 如果长度匹配，则证明没有请求体，设置body为空
        if len(raws) < index + 1:
            body = ''
        # 否则，剩余的内容为请求体
        else:
            # 拼接好请求体，并去除左侧空格
            body = '\n'.join(raws[index + 1:]).lstrip()
        print('body:')
        print(body)
        url_info = scheme, host, int(port), path
        print('url_info:')
        print(url_info)
        # 封装成RequestInfo对象
        self.request_info = RequestInfo(headers=headers,
                                        body=body,
                                        scheme=scheme,
                                        port=int(port),
                                        path=path)

    # 利用get_url_info解析得到的请求信息变异生成Payloads
    def generate_payload(self):
        # 生成各种Payloads
        payloads = GeneratePayloads(self.request_info).payloads()


# 封装各种信息
class RequestInfo:
    def __init__(self,
                 headers=None,
                 body='',
                 scheme=None,
                 host=None,
                 port=None,
                 path=''):
        self.headers = headers
        self.body = body
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path


class GeneratePayloads:
    def __init__(self, request_info: RequestInfo):
        self.request_info = request_info

    # 生成所有Payloads的主入口
    def payloads(self):
        info = self.request_info
        # http的80或者https的443端口省略不写
        if info.port == 80 or info.port == 443:
            _url = "{scheme}://{host}{path}".format(scheme=info.scheme, host=info.host, path=info.path)
        else:
            _url = "{scheme}://{host}{path}".format(scheme=info.scheme, host=info.host + ":" + info.port, path=info.path)


    # 点分割符号替换
    # TODO: 需要考虑，如何利用请求信息生成Payloads，直接转换请求没有任何意义
    def symbol_substitution(self):
        pass



if __name__ == '__main__':
    raw_str = \
"""POST /minio/webrpc HTTP/1.1
Host: 139.224.49.113:888
Content-Length: 74
x-amz-date: 20221128T032543Z
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://192.168.32.128:9000
Referer: http://192.168.32.128:9000/minio/login
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

{"id":1,"jsonrpc":"2.0","params":{"token":"test"},"method":"web.LoginSTS"}"""
    SSRFRequests(raw=raw_str)