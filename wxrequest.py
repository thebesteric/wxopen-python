"""

@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/8 14:47
@info: 
"""
import json

import requests

from cache.cache import MemoryCache
from constants import ACCESS_TOKEN, COMPONENT_ACCESS_TOKEN
from client.domain import wxerror
import exceptions
import constants

cache = MemoryCache()


class WeChatRequest:
    """
    微信请求基类
    """

    def __init__(self):
        self.__cache = cache
        self.requests = requests
        self.access_token = self.__cache.get(ACCESS_TOKEN)
        self.exceptions = exceptions
        self.constants = constants

    @staticmethod
    def render(content):
        if not isinstance(content, dict):
            content = json.loads(content, encoding='utf8')
        errcode = content.get('errcode', 0)
        if errcode:
            content.update({'errmsg_desc': wxerror.ERROR_CODE.get(str(errcode), '')})
        return content

    def get_cache(self):
        """
        获取缓存
        :return: MemoryCache
        """
        return self.__cache

    def get_suffix(self, path):
        """
        获取文件后缀名
        :param path: 文件路径
        :return:
        """
        pos = path.rfind('.')
        return path[pos + 1:]

    def validate_suffix(self, path, suffix_arr):
        """
        校验文件后缀
        :param path: 文件路径
        :param suffix_arr: 支持的文件类型
        :return:
        """
        suffix_arr = [suffix.lower() for suffix in suffix_arr]
        suffix = self.get_suffix(path).lower()
        if suffix not in suffix_arr:
            raise self.exceptions.ValidationException('File types must be in: %s' % suffix_arr)


class WeChatThirdRequest(WeChatRequest):
    """
    微信第三方平台请求基类
    """

    def __init__(self):
        super().__init__()
        self.component_access_token = self.get_cache().get(COMPONENT_ACCESS_TOKEN)
