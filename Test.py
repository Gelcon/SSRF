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


def RANDOM_TEXT_SPEC():
    min_char = 12
    max_char = 16
    chars = string.ascii_letters + string.digits + "!$%^&*()<>;:,.|\~`"
    return "".join(choice(chars) for x in range(randint(min_char, max_char)))


print(RANDOM_TEXT_SPEC())
