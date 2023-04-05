# @Author: Gelcon.
# @Date: 2023/4/4 16:52

import socket
import threading
import time
import json
import numpy as np


def get_data(data):  # 转为json
    data = str(data)
    # print(data)
    json_data = data.split('Content-Length', 1)
    # print(json_data[1])
    jd = json_data[1].split("{", 1)
    jd1 = "{" + jd[1]
    # jd1 = jd1[:-1]
    # print("信息为")
    # print(str(jd1))
    # print(repr(jd1))

    js2 = json.loads(str(jd1))
    # print(js2)
    return js2


def get_area(data1):  # 计算面积
    length = 24
    up = max(data1)
    print("up: %d" % up)
    down = min(data1)
    print("down: %d" % down)
    area_up = length * up
    data = np.array(data1)
    x = np.arange(0, 24, 24 / len(data1))
    area_under = np.trapz(data, x)  # 0-24  而不是0-249

    print(area_up)
    print(area_under)

    result = area_up - area_under
    print(result)
    return result


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send(b'Welcome!')
    while True:
        data1 = sock.recv(4096)
        data = data1.decode('utf-8')

        time.sleep(1)
        if not data1 or data1.decode('utf-8') == 'exit':
            break

        json_data = get_data(data)  # 从监听到的消息中提取信息
        list_y = json_data['item']
        area = get_area(list_y)

        msg = 'HTTP/1.1 200 OK\r\n\r\n ' + str(area)
        print(msg)
        sock.sendall(msg.encode('utf-8'))
        time.sleep(1)
        sock.close()

        print('Connection from %s:%s closed.' % addr)
        break


def listen_interface(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个基于IPV4和TCP协议的socket
    s.bind((address, port))

    # 开监听， 半连接池， 最大等待用户为5
    s.listen(5)
    while True:  # 接受一个新连接:
        sock, addr = s.accept()  # sock 连接通道 和 ip地址
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


if __name__ == '__main__':
    address = '127.0.0.1'
    port = 80
    listen_interface(address, port)
