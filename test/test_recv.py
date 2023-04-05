# @Author: Gelcon.
# @Date: 2023/4/2 16:13

import socket
import time

host = ''
port = 888
buf_size = 1024
addr = (host, port)


def udp_monitor():
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(addr)
    print('Waiting for connection...')
    while True:
        data, xxx = udp_server.recvfrom(buf_size)
        # data = data.decode(encoding='ascii')
        data = data.decode(encoding='utf-8')
        print(data)
        print(f'Time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')


if __name__ == '__main__':
    udp_monitor()

