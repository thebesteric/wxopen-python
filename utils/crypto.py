"""
加密解密工具类
@project: wxopen
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/9 15:58
@info: 
"""

import hashlib


def md5(str_value):
    """
    md5 加密
    :param str_value: 要加密的字符串
    :return: md5
    """
    m = hashlib.md5()
    b = str_value.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()


if __name__ == '__main__':
    print(md5('admin'))
