# @Author: Gelcon.
# @Date: 2023/2/16 14:39


import string
from random import *


# import unittest
#
#
# class TestCase(unittest.TestCase):
#
#     def test(self):
#         pass

# 在所有字母、所有数字、
def RANDOM_TEXT_SPEC():
    min_char = 12
    max_char = 16
    # string.ascii_letters 所有字母
    # string.digits 所有数字
    chars = string.ascii_letters + string.digits + "!$%^&*()<>;:,.|\~`"
    return "".join(choice(chars) for x in range(randint(min_char, max_char)))


# print(RANDOM_TEXT_SPEC())


# # https://www.cnblogs.com/crazyguo/p/15782300.html
def colored_print():
    """
    第一部分是设置要打印内容的颜色等样式
    第二部分是要打印的内容
    第三部分是设置新一轮的颜色字体样式，此处是恢复到默认样式

    \x1b调用函数，也可以使用\033达到同样的目的
    1;32;40这3部分以;分割，其中第一部分是命令，用来设置对应的属性,
    这里的1表示高亮显示；第二部分32，这里表示的是字体的颜色，33表示黄色；
    第三部分40这里表示的是字体的背景色，40为黑色。
    m是函数名称，这里表示的是SGR(Select Graphics Rendition)函数
    """
    # \x1b: 16进制的27
    val1 = '\x1b[1;33;40m' + 'yellow color print' + '\x1b[0m'
    print(val1)

    print('normal print')

    # \033: 8进制的27
    val3 = '\033[0;32;40m' + 'green color print' + '\033[0m'
    print(val3)


#
#
# if __name__ == '__main__':
#     colored_print()

# 需要加上;号
red = '\x1b[0;31;40m'
green = '\x1b[0;32;40m'
yellow = '\x1b[0;33;40m'
blue = '\x1b[0;36;40m'
reset_color = '\x1b[0m'

print(green,
      '=========================================================================================================================================',
      reset_color, sep='')
