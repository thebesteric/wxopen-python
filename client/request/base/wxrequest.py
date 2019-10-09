"""

@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/8 14:47
@info: 
"""
from io import StringIO

import pycurl

from cache.cache import MemoryCache
from client.constants import ACCESS_TOKEN

cache = MemoryCache()


class WeChatRequest:
    """
    微信请求基类
    """

    def __init__(self):
        self.__cache = cache
        self.pycurl = pycurl
        self.access_token = self.__cache.get(ACCESS_TOKEN)

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
