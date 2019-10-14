"""
微信菜单请求服务
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/26 17:47
@info: 
"""

from wxrequest import WeChatRequest


class MenuRequest(WeChatRequest):
    """
    菜单请求
    """

    def create(self, menu):
        """
        创建/更新菜单
        :param menu: 菜单对象
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % self.access_token
        content = self.requests.post(url, data=menu.to_json().encode('utf8')).content.decode('utf8')
        return self.render(content)

    def delete(self):
        """
        删除当前使用的自定义菜单
        注意，在个性化菜单时，调用此接口会删除默认菜单及全部个性化菜单
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s' % self.access_token
        content = self.requests.get(url).content.decode('utf8')
        return self.render(content)

    def info(self):
        """
        返回公众号当前使用的自定义菜单的配置
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s' % self.access_token
        content = self.requests.get(url).content.decode('utf8')
        return self.render(content)

    def get(self):
        """
        使用接口创建自定义菜单后，开发者还可使用接口查询自定义菜单的结构。另外请注意，在设置了个性化菜单后，使用本自定义菜单查询接口可以获取默认菜单和全部个性化菜单信息。
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s' % self.access_token
        content = self.requests.get(url).content.decode('utf8')
        return self.render(content)

    def create_conditional(self, menu):
        """
        创建个性化菜单

        为了帮助公众号实现灵活的业务运营，微信公众平台新增了个性化菜单接口，开发者可以通过该接口，让公众号的不同用户群体看到不一样的自定义菜单。该接口开放给已认证订阅号和已认证服务号。

        开发者可以通过以下条件来设置用户看到的菜单：
            1、用户标签（开发者的业务需求可以借助用户标签来完成）
            2、性别
            3、手机操作系统
            4、地区（用户在微信客户端设置的地区）
            5、语言（用户在微信客户端设置的语言）

        个性化菜单接口说明：
            1、个性化菜单要求用户的微信客户端版本在iPhone6.2.2，Android 6.2.4以上，暂时不支持其他版本微信
            2、菜单的刷新策略是，在用户进入公众号会话页或公众号profile页时，如果发现上一次拉取菜单的请求在5分钟以前，就会拉取一下菜单，如果菜单有更新，就会刷新客户端的菜单。测试时可以尝试取消关注公众账号后再次关注，则可以看到创建后的效果
            3、普通公众号的个性化菜单的新增接口每日限制次数为2000次，删除接口也是2000次，测试个性化菜单匹配结果接口为20000次
            4、出于安全考虑，一个公众号的所有个性化菜单，最多只能设置为跳转到3个域名下的链接
            5、创建个性化菜单之前必须先创建默认菜单（默认菜单是指使用普通自定义菜单创建接口创建的菜单）。如果删除默认菜单，个性化菜单也会全部删除
            6、个性化菜单接口支持用户标签，请开发者注意，当用户身上的标签超过1个时，以最后打上的标签为匹配

        个性化菜单匹配规则说明：
            个性化菜单的更新是会被覆盖的。
            例如公众号先后发布了默认菜单，个性化菜单1，个性化菜单2，个性化菜单3。那么当用户进入公众号页面时，将从个性化菜单3开始匹配，如果个性化菜单3匹配成功，则直接返回个性化菜单3，否则继续尝试匹配个性化菜单2，直到成功匹配到一个菜单。
            根据上述匹配规则，为了避免菜单生效时间的混淆，决定不予提供个性化菜单编辑API，开发者需要更新菜单时，需将完整配置重新发布一轮。

        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token=%s' % self.access_token
        content = self.requests.post(url, data=menu.to_json().encode('utf8')).content.decode('utf8')
        return self.render(content)

    def delete_conditional(self, menu_id):
        """
        删除个性化菜单
        menu_id: 菜单ID
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delconditional?access_token=%s' % self.access_token
        content = self.requests.post(url, json={'menuid': menu_id}).content.decode('utf8')
        return self.render(content)

    def try_match(self, user_id):
        """
        测试个性化菜单匹配结果
        user_id: 可以是粉丝的OpenID，也可以是粉丝的微信号
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/trymatch?access_token=%s' % self.access_token
        content = self.requests.post(url, json={'user_id': user_id}).content.decode('utf8')
        return self.render(content)
