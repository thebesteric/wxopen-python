"""
微信标签请求服务
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/29 12:18
@info: 
"""
import json

import requests

from cache.DefaultCache import MemoryCache
from client.constants import ACCESS_TOKEN
from client.replies import WeChatResponse

cache = MemoryCache()


class TagRequest:
    """
    用户请求
    """

    def __init__(self):
        self.access_token = cache.get(ACCESS_TOKEN)

    def create(self, name):
        """
        创建标签
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s' % self.access_token
        data = {'tag': {'name': name}}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def get(self):
        """
        接口调用请求说明
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s' % self.access_token
        content = requests.get(url).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def update(self, id, name):
        """
        编辑标签
        :param id: 标签ID
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/update?access_token=%s' % self.access_token
        data = {'tag': {'id': id, 'name': name}}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def delete(self, id):
        """
        删除标签
        :param id: 标签ID
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=%s' % self.access_token
        data = {'tag': {'id': id}}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def users(self, tagid, next_openid=''):
        """
        获取标签下粉丝列表
        :param tagid: 标签ID
        :param next_openid: 第一个拉取的OPENID，不填默认从头开始拉取
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s' % self.access_token
        data = {"tagid": tagid, "next_openid": next_openid}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def batch_tagging(self, tagid, *openids):
        """
        批量为用户打标签
        :param tagid: 标签ID
        :param openids: 粉丝列表
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s' % self.access_token
        data = {"tagid": tagid, "openid_list": list(openids)}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def batch_untagging(self, tagid, *openids):
        """
        批量为用户取消标签
        :param tagid: 标签ID
        :param openids: 粉丝列表
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s' % self.access_token
        data = {"tagid": tagid, "openid_list": list(openids)}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def user_tags(self, openid):
        """
        获取用户身上的标签列表
        :param openid:
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=%s' % self.access_token
        data = {"openid": openid}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')
