# @Author: Gelcon.
# @Date: 2023/2/16 14:39
import copy
import string
from random import *
import json

# import unittest
#
#
# class TestCase(unittest.TestCase):
#
#     def test(self):
#         pass

# 在所有字母、所有数字、
import lxml.etree


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
# red = '\x1b[0;31;40m'
# green = '\x1b[0;32;40m'
# yellow = '\x1b[0;33;40m'
# blue = '\x1b[0;36;40m'
# reset_color = '\x1b[0m'
#
# print(green,
#       '=========================================================================================================================================',
#       reset_color, sep='')

# str1 = '{"id": 1, "jsonrpc": "2.0", "params": {"token": "test"}, "method": "web.LoginSTS"}'
# # 转换为字典dict类型
# json1 = json.loads(str1)
# print(type(str1))
# print(type(json1))
# # 字典只查找1级标签
# print(json1['params'])

# str_json = '{"id": 1, "jsonrpc": "2.0", "params": {"token": "test"}, "method": "web.LoginSTS"}'
# traverse_dict(str_json)


# def traverse_json_dict(str_dict: dict, payload):
#     # 里面存放字典
#     result = []
#     for key in str_dict:
#         print(f'当前正在处理的key: {key}')
#         """
#         1. 判断当前的str_dict[key]是值还是dict
#         如果是值，直接将其修改为payload
#         如果是dict，保存当前的val值，用于还原
#         同时递归调用traverse_dict
#         """
#         # 如果value还是字典
#         if isinstance(str_dict[key], dict):
#             # 循环设置当前的key依次等于递归调用traverse_json_dict后所有可能的值
#             res = traverse_json_dict(str_dict[key], payload)
#             # 保存一份用于还原
#             val = str_dict[key]
#             for r in res:
#                 str_dict[key] = r
#                 result.append(str_dict.copy())
#             # 还原
#             str_dict[key] = val
#         # value为值
#         else:
#             # 保存一份用于还原
#             val = str_dict[key]
#             str_dict[key] = payload
#             result.append(str_dict.copy())
#             # 还原
#             str_dict[key] = val
#     # 返回所有的可能
#     return result


# if __name__ == '__main__':
#     str_test = '{"id":1, "jsonrpc":"2.0", "params":{"token":{"test": "hahaha"}, "password": "123"}, "method":"web.LoginSTS"}'
#     result_list = traverse_json_dict(json.loads(str_test), '127.0.0.1')
#     print('最终结果：')
#     for l in result_list:
#         print(l)

# """
# {"id":1, "jsonrpc":"2.0", "params":{"token":"test", "password": "123"}, "method":"web.LoginSTS"}
# """

from lxml import etree


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
        # 但是有text
        if root.text is not None:
            # 保存用于还原
            val = root.text
            root.text = payload
            result.append(copy.deepcopy(root))
            # 还原
            root.text = val
        # 直接返回空列表，没有地方可以放置payload，例如<run></run>
        else:
            return []
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


if __name__ == '__main__':
    # xml_str = """<run><log encoding="hexBinary">4142430A</log><result><log>4142430B</log><log>4142430C</log></result><url>*FUZZ*</url></run>"""
    xml_str = \
        """<run>
            <log encoding="hexBinary">4142430A</log>
            <result>
                <log>4142430B</log>
                <log>4142430C</log>
            </result>
            <url>*FUZZ*</url>
        </run>"""
    tree: lxml.etree._Element = etree.XML(xml_str)
    p = 'http://127.0.0.1'
    res = traverse_xml(tree, p)
    with open('test.txt', 'w') as f:
        for r in res:
            f.write(etree.tostring(r, method='xml').decode('utf-8') + '\n\n')
