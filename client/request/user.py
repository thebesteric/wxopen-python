"""
微信用户请求服务
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/29 15:08
@info: 
"""
import requests
import json
from cache.cache import MemoryCache
from client.constants import ACCESS_TOKEN
from client.replies import WeChatResponse

cache = MemoryCache()


class UserRequest:
    """
    用户请求
    """

    def __init__(self):
        self.access_token = cache.get(ACCESS_TOKEN)

    def update_remark(self, openid, remark):
        """
        指定用户设置备注名
        PS: 该接口暂时开放给微信认证的服务号
        :param openid: 用户标识
        :param remark: 新的备注名，长度必须小于30字符
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token=%s' % self.access_token
        data = {'openid': openid, 'remark': remark}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()
