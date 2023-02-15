class Payload:
    def __init__(self, domain='www.baidu.com', ip='127.0.0.1'):
        self.ip, self.domain = ip, domain

    """
    点分割符号替换
    """
    def symbol_substitution(self):
        domain_list = list()
        domain_list.append(self.domain.replace('.', '。'))
        domain_list.append(self.domain.replace('.', '｡'))
        domain_list.append(self.domain.replace('.', '．'))
        return domain_list


if __name__ == '__main__':
    # ip 要进行扫描的ip
    ip = '139.224.49.113'
    # 要添加的域名特征，通常为目标域名的白名单
    domain = 'www.baidu.com'
    for payload in Payload(domain, ip).symbol_substitution():
        print('http://' + payload)
