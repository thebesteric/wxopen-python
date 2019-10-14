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

from wxrequest import WeChatRequest


class TagRequest(WeChatRequest):
    """
    标签请求
    """

    def create(self, name):
        """
        创建标签
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s' % self.access_token
        data = {'tag': {'name': name}}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def get(self):
        """
        接口调用请求说明
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s' % self.access_token
        content = self.requests.get(url).content.decode('utf8')
        return self.render(content)

    def update(self, id, name):
        """
        编辑标签
        :param id: 标签ID
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/update?access_token=%s' % self.access_token
        data = {'tag': {'id': id, 'name': name}}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def delete(self, id):
        """
        删除标签
        :param id: 标签ID
        :param name: 标签名（30个字符以内）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=%s' % self.access_token
        data = {'tag': {'id': id}}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def users(self, tagid, next_openid=''):
        """
        获取标签下粉丝列表
        :param tagid: 标签ID
        :param next_openid: 第一个拉取的OPENID，不填默认从头开始拉取
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s' % self.access_token
        data = {"tagid": tagid, "next_openid": next_openid}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def batch_tagging(self, tagid, *openids):
        """
        批量为用户打标签
        :param tagid: 标签ID
        :param openids: 粉丝列表
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s' % self.access_token
        data = {"tagid": tagid, "openid_list": list(openids)}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def batch_untagging(self, tagid, *openids):
        """
        批量为用户取消标签
        :param tagid: 标签ID
        :param openids: 粉丝列表
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s' % self.access_token
        data = {"tagid": tagid, "openid_list": list(openids)}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def user_tags(self, openid):
        """
        获取用户身上的标签列表
        :param openid: 用户标识
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=%s' % self.access_token
        data = {"openid": openid}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)
