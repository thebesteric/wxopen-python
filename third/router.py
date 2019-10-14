"""
微信第三方平台路由集合
@project: wxopen
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/12 12:08
@info: 
"""
import wxrequest


class WeChatThirdPlatformRouter(wxrequest.WeChatThirdRequest):

    def __init__(self, component_app_id, component_app_secret, component_access_token):
        super().__init__()
        self.component_app_id = component_app_id
        self.component_app_secret = component_app_secret
        self.component_access_token = component_access_token

    def create_component_login_page_qr_code(self, redirect_uri, auth_type=3):
        """
        生成二维码授权页面
        :param redirect_uri: 回调 URI
        :param auth_type: 要授权的帐号类型：1 则商户点击链接后，手机端仅展示公众号、2 表示仅展示小程序，3 表示公众号和小程序都展示
        :return:
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/componentloginpage' \
              '?component_appid={component_app_id}&pre_auth_code={pre_auth_code}&redirect_uri={redirect_uri}&auth_type={auth_type}' \
            .format(component_app_id=self.component_app_id, pre_auth_code=self.api_create_pre_auth_code()['pre_auth_code'], redirect_uri=redirect_uri, auth_type=auth_type)
        return url

    def create_component_login_page_by_url(self, redirect_uri, auth_type=3):
        """
        生成 URL 授权链接
        :param redirect_uri:
        :param auth_type:
        :return:
        """
        url = 'https://mp.weixin.qq.com/safe/bindcomponent' \
              '?action=bindcomponent&auth_type={auth_type}&no_scan=1&component_appid={component_app_id}&pre_auth_code={pre_auth_code}&redirect_uri={redirect_uri}#wechat_redirect' \
            .format(component_app_id=self.component_app_id, pre_auth_code=self.api_create_pre_auth_code()['pre_auth_code'], redirect_uri=redirect_uri, auth_type=auth_type)
        return url

    def api_component_token(self):
        """
        令牌
        定时任务会每 5400 秒获取令牌存储到缓存中
        :return:
        """
        return self.component_access_token

    def api_create_pre_auth_code(self):
        """
        预授权码
        预授权码（pre_auth_code）是第三方平台方实现授权托管的必备信息，每个预授权码有效期为 10 分钟。需要先获取令牌才能调用
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token=%s' % self.component_access_token
        data = {'component_appid': self.component_app_id}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def api_query_auth(self, auth_code):
        """
        使用授权码获取授权信息
        :param auth_code: 授权码，当用户在第三方平台授权页中完成授权流程后，第三方平台开发者可以在回调 URI 中通过 URL 参数获取授权码
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=%s' % self.component_access_token
        data = {'component_appid': self.component_app_id, 'authorization_code': auth_code}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def api_authorizer_token(self, authorizer_app_id, authorizer_refresh_token):
        """
        获取/刷新接口调用令牌
        :param authorizer_app_id: 授权方 appid，获取授权信息时得到
        :param authorizer_refresh_token: 刷新令牌，获取授权信息时得到

        在公众号/小程序接口调用令牌（authorizer_access_token）失效时，可以使用刷新令牌（authorizer_refresh_token）获取新的接口调用令牌。
        注意： authorizer_access_token 有效期为 2 小时，开发者需要缓存 authorizer_access_token，避免获取/刷新接口调用令牌的 API 调用触发每日限额。
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?component_access_token=%s' % self.component_access_token
        data = {"component_appid": self.component_app_id, "authorizer_appid": authorizer_app_id, "authorizer_refresh_token": authorizer_refresh_token}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def api_get_authorizer_info(self, authorizer_app_id):
        """
        获取授权方的帐号基本信息
        :param authorizer_app_id: 授权方 appid，获取授权信息时得到
        该 API 用于获取授权方的基本信息，包括头像、昵称、帐号类型、认证类型、微信号、原始ID和二维码图片URL
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?component_access_token=%s' % self.component_access_token
        data = {"component_appid": self.component_app_id, "authorizer_appid": authorizer_app_id}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def api_get_authorizer_option(self, authorizer_app_id, option_name):
        """
        获取授权方选项信息
        本 API 用于获取授权方的公众号/小程序的选项设置信息，如：地理位置上报，语音识别开关，多客服开关
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :param option_name: 选项名称，location_report，voice_recognize，customer_service
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_option?component_access_token=%s' % self.component_access_token
        data = {"component_appid": self.component_app_id, "authorizer_appid": authorizer_app_id, 'option_name': option_name}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def api_get_authorizer_option_location_report(self, authorizer_app_id):
        """
        获取授权方选项信息（地理位置上报选项）
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :return: 0: 无上报, 1: 进入会话时上报, 2: 每 5s 上报
        """
        return self.api_get_authorizer_option(authorizer_app_id, 'location_report')

    def api_get_authorizer_option_voice_recognize(self, authorizer_app_id):
        """
        获取授权方选项信息（语音识别开关选项）
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :return: 0: 关闭语音识别, 1: 开启语音识别
        """
        return self.api_get_authorizer_option(authorizer_app_id, 'voice_recognize')

    def api_get_authorizer_option_customer_service(self, authorizer_app_id):
        """
        获取授权方选项信息（多客服开关选项）
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :return: 0: 关闭多客服, 1: 开启多客服
        """
        return self.api_get_authorizer_option(authorizer_app_id, 'customer_service')

    def api_set_authorizer_option(self, authorizer_app_id, option_name, option_value):
        """
        设置授权方选项信息
        本 API 用于设置授权方的公众号/小程序的选项信息，如：地理位置上报，语音识别开关，多客服开关
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :param option_name: 选项名称
        :param option_value: 设置的选项值
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_set_authorizer_option?component_access_token=%s' % self.component_access_token
        data = {"component_appid": self.component_app_id, "authorizer_appid": authorizer_app_id, "option_name": option_name, "option_value": option_value}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)

    def api_set_authorizer_option_location_report(self, authorizer_app_id, option_value):
        """
        设置授权方选项信息（地理位置上报选项）
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :param option_value: 0: 无上报, 1: 进入会话时上报, 2: 每 5s 上报
        :return:
        """
        return self.api_set_authorizer_option(authorizer_app_id, 'location_report', option_value)

    def api_set_authorizer_option_voice_recognize(self, authorizer_app_id, option_value):
        """
        设置授权方选项信息（语音识别开关选项）
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :param option_value: 0: 关闭语音识别, 1: 开启语音识别
        :return:
        """
        return self.api_set_authorizer_option(authorizer_app_id, 'voice_recognize', option_value)

    def api_set_authorizer_option_customer_service(self, authorizer_app_id, option_value):
        """
        设置授权方选项信息（多客服开关选项）
        :param authorizer_app_id: 授权公众号或小程序的 appid
        :param option_value: 0: 关闭多客服, 1: 开启多客服
        :return:
        """
        return self.api_set_authorizer_option(authorizer_app_id, 'customer_service', option_value)

    def api_get_authorizer_list(self, offset, count=500):
        """
        拉取所有已授权的帐号信息
        使用本 API 拉取当前所有已授权的帐号基本信息
        :param offset: 偏移位置/起始位置
        :param count: 拉取数量，最大为 500
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_list?component_access_token=%s' % self.component_access_token
        data = {"component_appid": self.component_app_id, "offset": offset, "count": count}
        content = self.requests.post(url, json=data).content.decode('utf8')
        return self.render(content)
