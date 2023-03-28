# @Author: Gelcon.
# @Date: 2023/2/16 10:13

"""
本文件功能：检测SSRF漏洞
"""
import copy
import datetime
import json
import logging
import lxml
import requests
import concurrent.futures

from ip import all_payload
from lxml import etree


class SSRFDetection(object):

    def __init__(self, raw: str):
        self.raw = raw
        self.request_info = None
        self.payload = []
        # 处理raw，将其解析得到请求信息
        self.get_request_info()
        # 生成self.payload
        self.generate_payload()
        # 发送请求
        self.send_request()

    # 将BurpSuite格式的请求转换为字典等信息
    def get_request_info(self, **kwargs):
        raw = self.raw.strip()
        # Key值不存在则返回None
        proxies = kwargs.get("proxies", None)
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
        print('method: {}'.format(method))
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
                                        method=method,
                                        scheme=scheme,
                                        host=host,
                                        port=int(port),
                                        path=path,
                                        proxies=proxies)

    # 利用get_url_info解析得到的请求信息变异生成Payloads
    def generate_payload(self):
        # 生成各种Payloads
        self.payload = Payload(self.request_info).payload()
        logging.info('生成Payload如下：')
        for p in self.payload:
            logging.info(p)
        filename = "./result/payload/payload_info/request_payload_" + "_" + str(
            datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')) + '.txt'
        # 将当前的Payload写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            for p in self.payload:
                f.write(str(p) + '\n\n')

    # 发送请求
    def send_request(self):
        """
        利用requests库发送请求
        """
        info_list = self.payload
        filename = "./result/request_log/request_log_" + "_" + str(
            datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')) + '.txt'
        f = open(filename, 'w', encoding='utf-8')
        # 并发编程，创建一个具有8个工作线程的线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # 对info_list中的每一个info都调用fetch_response方法
            results = executor.map(fetch_response, info_list)
        for r, info in results:
            if r.status_code == 200:
                logging.info(f"当前Payload:\n{str(info)}\n请求成功\n")
                # 如果一个类实现了__str__方法
                # 当我们将类的实例传递给str()方法时，Python会调用__str__方法
                f.write(f"当前Payload:\n{str(info)}\n请求成功\n\n")
            else:
                logging.error(f"当前Payload:\n{str(info)}\n请求失败\n")
                f.write(f"当前Payload:\n{str(info)}\n请求失败\n\n")
        # 手动关闭
        f.close()


# 封装各种信息
class RequestInfo:
    def __init__(self,
                 headers=None,
                 body='',
                 method='',
                 scheme=None,
                 host='',
                 port=80,
                 path='',
                 timeout=3,
                 proxies=None):
        self.headers = headers
        self.body = body
        self.method = method
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path
        # 超时时间，默认是3秒
        self.timeout = timeout
        # 代理
        self.proxies = proxies

    def __str__(self):
        # http的80或者https的443端口省略不写
        if self.port == 80 or self.port == 443:
            return "以下是RequestInfo的内容：\nheaders:\n{}\nbody:\n{}\nmethod: {}\nURL: {}" \
                .format(self.headers,
                        self.body,
                        self.method,
                        self.scheme + '://' + self.host + self.path)
        else:
            return "以下是RequestInfo的内容：\nheaders:\n{}\nbody:\n{}\nmethod: {}\nURL: {}" \
                .format(self.headers,
                        self.body,
                        self.method,
                        self.scheme + '://' + self.host + ':' + str(self.port) + self.path)


class Payload:
    def __init__(self, request_info: RequestInfo):
        self.request_info = request_info
        print(request_info)

    # 生成所有Payloads的主入口
    def payload(self):
        info = self.request_info
        # 所有payload
        payload = []

        # POST请求，在请求体中进行变异，根据Content-Type进行区分
        if info.method == 'POST':
            """
            json格式：
            1. 找到所有的key
            2. 逐个将其val值修改为payload，其余的不变
            3. 修改info.body
            4. 将info放入Payload
            """
            if info.headers['Content-Type'] and "application/json" in info.headers['Content-Type']:
                # 将body转换为dict类型
                json_dict = json.loads(info.body)
                # 生成访问127.0.0.1的payload
                temp = all_payload(ip='127.0.0.1', port='80', site='www.google.com')
                # 每一个payload，都插入可以作为值的地方
                for p in temp:
                    # 返回的是字典类型
                    result = traverse_json_dict(json_dict, p)
                    for r in result:
                        # json.dumps(r)将字典转换为json字符串
                        info.body = json.dumps(r)
                        # 此处需要使用深拷贝
                        payload.append(copy.deepcopy(info))

            # XML格式
            elif info.headers['Content-Type'] and "application/xml" in info.headers['Content-Type']:
                # 将body转换为XML类型
                tree = etree.XML(info.body)
                # 生成访问127.0.0.1的payload
                temp = all_payload(ip='127.0.0.1', port='80', site='www.google.com')
                # 每一个payload，都插入可以作为值的地方
                for p in temp:
                    result = traverse_xml(tree, p)
                    for r in result:
                        # toString方法将_Element对象转换为str
                        info.body = etree.tostring(r).decode('utf-8')
                        payload.append(copy.deepcopy(info))

            # x-www-form-urlencoded，参数格式：key1=value1&key2=value2
            elif info.headers['Content-Type'] and "application/x-www-form-urlencoded" in info.headers['Content-Type']:
                param_dict = split_post_urlencoded_str(info.body)
                # 如果字典为空
                if not param_dict:
                    logging.info(f"{info.path} don't have any param to inject.")
                # 生成访问127.0.0.1的payload
                temp = all_payload(ip='127.0.0.1', port='80', site='www.google.com')
                for p in temp:
                    for key in param_dict.keys():
                        # 保存value
                        val = param_dict[key]
                        param_dict[key] = p
                        # 放入请求体
                        info.body = concat_post_urlencoded_str(param_dict)
                        # 放入payload列表
                        payload.append(copy.deepcopy(info))
                        # 还原value值
                        param_dict[key] = val
            else:
                logging.error('Unsupported Content-Type.')

        # GET请求，在请求参数值上进行变异
        elif info.method == 'GET':
            """
            GET请求：
            1. 将?wd=Test&ie=UTF-8切分，生成字典{'wd': 'Test', 'ie': 'UTF-8'}
            2. 将其替换为{'wd': payload, 'ie': 'UTF-8'}或者{'wd': 'Test', 'ie': payload}
            3. 转换为?wd=payload&ie=UTF-8和?wd=payload&ie=payload
            4. 将其放入payload列表
            """
            # 对请求路径进行分割，得到key为请求参数，val为请求值的字典param_dict
            param_dict = split_get_str(info.path)
            for k in param_dict.keys():
                print(f"key: {k}, value: {param_dict[k]}")
            # 如果字典为空
            if not param_dict:
                logging.info(f"{info.path} don't have any param to inject.")
            # 生成访问127.0.0.1的payload
            temp = all_payload(ip='127.0.0.1', port='80', site='www.google.com')
            for p in temp:
                for key in param_dict.keys():
                    # 保存value
                    val = param_dict[key]
                    param_dict[key] = p
                    # 拼接为path
                    info.path = concat_get_str(param_dict)
                    # 放入payload列表
                    payload.append(info)
                    # 还原value值
                    param_dict[key] = val
        else:
            logging.error('Unsupported Request Method')
        return payload


# 分割GET请求路径的参数
def split_get_str(path: str):
    if path.count('?') == 0:
        return {}
    # 仅有1个参数
    if path.count('=') == 1:
        param = path.split('?')[1].split('=')
        return {param[0]: param[1]}
    # 得到?之后的内容，然后按照&分割
    params = path.split('?')[1].split('&')
    result = {}
    for param in params:
        temp = param.split('=')
        result[temp[0]] = temp[1]
    return result


# 合并GET请求路径的参数
def concat_get_str(param_dict: dict):
    result = '?'
    length = len(param_dict.keys())
    for index, key in enumerate(param_dict.keys()):
        # 最后1个不加&
        if index == length - 1:
            result += key + '=' + param_dict[key]
        else:
            result += key + '=' + param_dict[key] + '&'
    return result


# 分解格式为key1=value1&key2=value2的post请求参数
def split_post_urlencoded_str(body: str):
    # 判断是否为空
    if body == '':
        return {}
    # 仅有1个，例如url=xxx
    if body.count('=') == 1:
        temp = body.split('=')
        return {temp[0]: temp[1]}
    # 大于1个
    params = body.split('&')
    result = {}
    for param in params:
        param = param.split('=')
        result[param[0]] = param[1]
    return result


# 合并格式为key1=value1&key2=value2的post请求参数
def concat_post_urlencoded_str(param_dict: dict):
    result = ''
    for key in param_dict.keys():
        result += key + '=' + param_dict[key]
    return result


# 遍历json，将payload放置在可能的位置
def traverse_json_dict(str_dict: dict, payload):
    # 里面存放字典
    result = []
    for key in str_dict:
        """
        判断当前的str_dict[key]是值还是dict
        ① 如果是值，直接将其修改为payload，放入result
        ② 如果是dict，保存当前的val值用于还原，递归调用traverse_json_dict
        将所有可能的结果都用于修改str_dict[key]，并放入result
        同时递归调用traverse_dict
        """
        # 如果value还是字典
        if isinstance(str_dict[key], dict):
            # 递归调用
            res = traverse_json_dict(str_dict[key], payload)
            # 保存一份用于还原
            val = str_dict[key]
            # 循环设置当前的key依次等于递归调用traverse_json_dict后所有可能的值
            for r in res:
                str_dict[key] = r
                result.append(str_dict.copy())
            # 还原
            str_dict[key] = val
        # value为值
        else:
            # 保存一份用于还原
            val = str_dict[key]
            str_dict[key] = payload
            result.append(str_dict.copy())
            # 还原
            str_dict[key] = val
    # 返回所有的可能
    return result


# 遍历xml，将payload放置在可能的位置
def traverse_xml(root: lxml.etree._Element, payload: str):
    """
    遍历xml的每一个结点，步骤如下：
    判断当前标签是否含有子节点，
    如果有，则在循环中递归调用traverse_xml
    如果没有子节点，则将其text设为payload
    """
    result = []
    children = root.getchildren()
    """
    xml和json算法的区别在于：
    xml的大的父标签相当于json中的花括号，没有具体的作用
    但是在xml中这是标签，而json中直接遍历了除了花括号以外的key
    """
    # 如果没有节点了
    if not root.getchildren():
        # 保存用于还原
        val = root.text
        root.text = payload
        result.append(copy.deepcopy(root))
        # 还原
        root.text = val
    # 有子节点
    else:
        for child in children:
            print(f'当前正在处理: \ntag: {child.tag}, text: {child.text}')
            # 如果有孙结点
            if child.getchildren():
                # 对child进行递归
                res = traverse_xml(child, payload)
                # 当前的child将其所有的子节点全都删除
                val = child.getchildren()
                for grandson in child.getchildren():
                    child.remove(grandson)
                for r in res:
                    # 每一个r都是以和child相同的标签开头，因此child将r的children复制
                    for grandson in r.getchildren():
                        child.append(grandson)
                    # 复制完后，使用深拷贝将当前的root放入result
                    result.append(copy.deepcopy(root))
                    # 随后，child将其所有的子元素删除
                    for grandson in child.getchildren():
                        child.remove(grandson)
                # 还原child
                for v in val:
                    child.append(v)
            # 没有其他子节点了
            else:
                # 保存用于还原
                val = child.text
                child.text = payload
                result.append(copy.deepcopy(root))
                child.text = val
    return result


# 发送requests请求
def fetch_response(info: RequestInfo) -> tuple:
    # 完整的请求路径
    full_path = info.scheme + '://' + info.host + ':' + str(info.port) + info.path
    r = None
    if info.method == "GET":
        r = requests.get(full_path,
                         headers=info.headers,
                         timeout=info.timeout,
                         proxies=info.proxies)
    elif info.method == "POST":
        if info.headers['Content-Type'] and "application/json" in info.headers['Content-Type']:
            r = requests.post(full_path,
                              headers=info.headers,
                              json=info.body,
                              timeout=info.timeout,
                              proxies=info.proxies)
        elif info.headers['Content-Type'] and "application/xml" in info.headers['Content-Type']:
            r = requests.post(full_path,
                              headers=info.headers,
                              data=info.body,
                              timeout=info.timeout,
                              proxies=info.proxies)
        # "application/x-www-form-urlencoded"
        else:
            r = requests.post(full_path,
                              headers=info.headers,
                              data=info.body,
                              timeout=info.timeout,
                              proxies=info.proxies)
    return r, info


if __name__ == '__main__':
    raw_str = """POST /ssrf2 HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1:5000/
Content-Type: application/json
Content-Length: 43
Connection: close
Upgrade-Insecure-Requests: 1

{"userId":"1", "url": "http://example.com"}"""
    SSRFDetection(raw_str)
