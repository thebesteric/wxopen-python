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

    def info(self, openid, lang='zh_CN'):
        """
        获取用户基本信息（包括UnionID机制）
        :param openid: 用户标识
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/info'
        content = requests.get(url, params={'access_token': self.access_token, 'openid': openid, 'lang': lang}).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def infos(self, *openids, lang='zh_CN'):
        """
        批量获取用户基本信息。最多支持一次拉取100条
        :param openids: 用户标识list
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s' % self.access_token
        data = {'user_list': [{'openid': openid, 'lang': lang} for openid in openids]}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def subscribe_list(self, next_openid=''):
        """
        获取帐号的关注者列表
        一次拉取调用最多拉取10000个关注者的OpenID，可以通过多次拉取的方式来满足需求
        :param next_openid: 第一个拉取的OPENID，不填默认从头开始拉取
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (self.access_token, next_openid)
        content = requests.get(url).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def black_list(self, begin_openid=''):
        """
        获取公众号的黑名单列表
        :param begin_openid:
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/getblacklist?access_token=%s' % self.access_token
        data = {'begin_openid': begin_openid}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def batch_black_list(self, *openids):
        """
        拉黑用户
        :param openids: 需要拉入黑名单的用户的openid，一次拉黑最多允许20个
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchblacklist?access_token=%s' % self.access_token
        data = {"openid_list": [openid for openid in openids]}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def batch_un_black_list(self, *openids):
        """
        取消拉黑用户
        :param openids: 需要拉入黑名单的用户的openid，一次拉黑最多允许20个
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchunblacklist?access_token=%s' % self.access_token
        data = {"openid_list": [openid for openid in openids]}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')
