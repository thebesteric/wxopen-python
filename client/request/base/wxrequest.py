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
from io import StringIO

import pycurl
import requests

from cache.cache import MemoryCache
from client.constants import ACCESS_TOKEN
from client.domain import wxerror

cache = MemoryCache()


class WeChatRequest:
    """
    微信请求基类
    """

    def __init__(self):
        self.__cache = cache
        self.requests = requests
        self.pycurl = pycurl
        self.access_token = self.__cache.get(ACCESS_TOKEN)

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

    def get_curl(self):
        """
        获取curl
        :return: (curl, fp)
        """
        curl = self.pycurl.Curl()
        fp = StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, fp.write)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        curl.setopt(pycurl.CONNECTTIMEOUT, 60)
        curl.setopt(pycurl.TIMEOUT, 300)
        curl.setopt(pycurl.HEADER, 1)
        return curl, fp
