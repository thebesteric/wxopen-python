"""

@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/8 14:47
@info: 
"""
from cache.cache import MemoryCache
from client.constants import ACCESS_TOKEN

cache = MemoryCache()


class WeChatRequest:
    """
    微信请求基类
    """

    def __init__(self):
        self.__cache = cache
        self.access_token = self.__cache.get(ACCESS_TOKEN)

    def get_cache(self):
        """获取缓存"""
        return self.__cache
