"""
客服消息服务
@project: wxopen
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/9 14:11
@info: 
"""
from client.request.base.wxrequest import WeChatRequest
import requests
from client.replies import WeChatResponse
import json


class CustomerRequest(WeChatRequest):
    """
    客服消息服务
    """

    def add_customer(self, kf_account, nickname, password):
        """
        添加客服帐号
        :param kf_account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码，格式为密码明文的32位加密MD5值。该密码仅用于在公众平台官网的多客服功能中使用，若不使用多客服功能，则不必设置密码
        :return:
        """
        url = 'https://api.weixin.qq.com/customservice/kfaccount/add?access_token=%s' % self.access_token
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def update_customer(self, kf_account, nickname, password):
        """
        修改客服帐号
        :param kf_account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码，格式为密码明文的32位加密MD5值。该密码仅用于在公众平台官网的多客服功能中使用，若不使用多客服功能，则不必设置密码
        :return:
        """
        url = 'https://api.weixin.qq.com/customservice/kfaccount/update?access_token=%s' % self.access_token
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def delete_customer(self, kf_account, nickname, password):
        """
        删除客服帐号
        :param kf_account: 完整客服账号，格式为：账号前缀@公众号微信号
        :param nickname: 客服昵称，最长6个汉字或12个英文字符
        :param password: 客服账号登录密码，格式为密码明文的32位加密MD5值。该密码仅用于在公众平台官网的多客服功能中使用，若不使用多客服功能，则不必设置密码
        :return:
        """
        url = 'https://api.weixin.qq.com/customservice/kfaccount/del?access_token=%s' % self.access_token
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def upload_head_img(self, kf_account, img_path):
        """
        设置客服帐号的头像
        eg. curl -F media=@test.jpg "https://api.weixin.qq.com/customservice/kfaccount/uploadheadimg?access_token=ACCESS_TOKEN&kf_account=KFACCOUNT"
        :return:
        """
        url = 'http://api.weixin.qq.com/customservice/kfaccount/uploadheadimg?access_token=%s&kf_account=%s' % (self.access_token, kf_account)
        curl, fp = self.get_curl()
        curl.setopt(self.pycurl.POST, 1)
        curl.setopt(self.pycurl.URL, url)
        curl.setopt(self.pycurl.HTTPPOST, [('media', (self.pycurl.FILE, img_path))])
        curl.perform()
        body = fp.getvalue()
        fp.close()
        curl.close()

        return body

    def list_customers(self):
        """
        获取所有客服账号
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=%s' % self.access_token
        content = requests.get(url).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def send(self, touser, msg_type, msg, kf_account=None):
        """
        发送客服消息
        :param touser: 消息接收人的 openid
        :param msg_type:
            消息类型，文本为text，图片为image，语音为voice，视频消息为video，音乐消息为music，图文消息（点击跳转到外链）为news，
            图文消息（点击跳转到图文消息页面）为mpnews，卡券为wxcard，小程序为miniprogrampage
        :param msg: 消息体，dict
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % self.access_token
        data = {'touser': touser, 'msg_type': msg_type}
        data.update(msg)
        if kf_account:
            data.update({'customservice': {'kf_account': kf_account}})
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def send_text(self, touser, content, customer_account=None):
        """
        发送文本消息
        :param touser: 消息接收人的OPENID
        :param content: 消息内容
        :param customer_account: 以某个客服帐号来发消息

        支持插入跳小程序的文字链：<a href="http://www.qq.com" data-miniprogram-appid="appid" data-miniprogram-path="pages/index/index">点击跳小程序</a>
        1.data-miniprogram-appid 项，填写小程序appid，则表示该链接跳小程序；
        2.data-miniprogram-path项，填写小程序路径，路径与app.json中保持一致，可带参数；
        3.对于不支持data-miniprogram-appid 项的客户端版本，如果有herf项，则仍然保持跳href中的网页链接；
        4.data-miniprogram-appid对应的小程序必须与公众号有绑定关系

        :return:
        """
        msg = {'text': {'content': content}}
        self.send(touser, 'text', msg, customer_account)

    def send_image(self, touser, media_id, kf_account=None):
        """
        发送图片消息
        :param touser: 消息接收人的OPENID
        :param media_id: 素材ID
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'image': {'media_id': media_id}}
        self.send(touser, 'image', msg, kf_account)

    def send_voice(self, touser, media_id, kf_account=None):
        """
        发送语音消息
        :param touser: 消息接收人的OPENID
        :param media_id: 素材ID
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'voice': {'media_id': media_id}}
        self.send(touser, 'voice', msg, kf_account)

    def send_video(self, touser, media_id, title, description='', kf_account=None):
        """
        发送语音消息
        :param touser: 消息接收人的OPENID
        :param media_id: 素材ID
        :param title: 标题
        :param description: 描述
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'video': {'media_id': media_id, 'thumb_media_id': media_id, 'title': title, 'description': description}}
        self.send(touser, 'video', msg, kf_account)

    def send_music(self, touser, title, description, musicurl, hqmusicurl, thumb_media_id, kf_account=None):
        """
        发送音乐消息
        :param touser: 消息接收人的OPENID
        :param title: 标题
        :param description: 描述
        :param musicurl: 音乐链接
        :param hqmusicurl: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图素材ID
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'music': {'title': title, 'description': description, 'musicurl': musicurl, 'hqmusicurl': hqmusicurl, 'thumb_media_id': thumb_media_id}}
        self.send(touser, 'music', msg, kf_account)

    def send_news(self, touser, media_id, kf_account=None):
        """
        发送图文消息（点击跳转到图文消息页面）
        :param touser: 消息接收人的OPENID
        :param media_id: 素材ID
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'mpnews': {'media_id': media_id}}
        self.send(touser, 'mpnews', msg, kf_account)

    def send_news_outer(self, touser, title, description, url, picurl, kf_account=None):
        """
        发送图文消息（点击跳转到外链）
        :param touser: 消息接收人的OPENID
        :param title: 标题
        :param description: 描述
        :param url: 图文消息被点击后跳转的链接
        :param picurl: 图文消息的图片链接
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'news': {'articles': [{'title': title, 'description': description, 'url': url, 'picurl': picurl}]}}
        self.send(touser, 'news', msg, kf_account)

    def send_msg_menu(self, touser, head_content, tail_content, menus, kf_account=None):
        """
        发送发送菜单消息
        :param touser: 消息接收人的OPENID
        :param head_content: 标题头
        :param tail_content: 标题尾
        :param menus: 菜单选项，列表形式，[{'id': id, 'content': content}, ...]
        :param kf_account: 以某个客服帐号来发消息

        用户点击后，微信会发送一条XML消息到开发者服务器，格式如下：
        <xml>
            <ToUserName><![CDATA[ToUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>1500000000</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[满意]]></Content>
            <MsgId>1234567890123456</MsgId>
            <bizmsgmenuid>101</bizmsgmenuid>
        </xml>

        :return:
        """
        msg = {'msgmenu': {'head_content': head_content, 'tail_content': tail_content, 'list': menus}}
        self.send(touser, 'msgmenu', msg, kf_account)

    def send_wx_card(self, touser, card_id, kf_account=None):
        """
        发送卡券消息
        :param touser: 消息接收人的OPENID
        :param card_id: 卡券ID
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'wxcard': {'card_id': card_id}}
        self.send(touser, 'wxcard', msg, kf_account)

    def send_mini_programpage(self, touser, title, appid, pagepath, thumb_media_id, kf_account=None):
        """
        发送小程序卡片（要求小程序与公众号已关联）
        :param touser: 消息接收人的OPENID
        :param title: 小程序卡片的标题
        :param appid: 小程序的appid，要求小程序的appid需要与公众号有关联关系
        :param pagepath: 小程序的页面路径，跟app.json对齐，支持参数，比如pages/index/index?foo=barO
        :param thumb_media_id: 小程序卡片图片
        :param kf_account: 以某个客服帐号来发消息
        :return:
        """
        msg = {'miniprogrampage': {'title': title, 'appid': appid, 'pagepath': pagepath, 'thumb_media_id': thumb_media_id}}
        self.send(touser, 'miniprogrampage', msg, kf_account)

    def send_typing(self, touser):
        """
        客服输入状态: 正在输入
        :param touser: 消息接收人的OPENID

        此接口需要客服消息接口权限
        1、如果不满足发送客服消息的触发条件，则无法下发输入状态。
        2、下发输入状态，需要客服之前30秒内跟用户有过消息交互。
        3、在输入状态中（持续15s），不可重复下发输入态。
        4、在输入状态中，如果向用户下发消息，会同时取消输入状态。

        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/typing?access_token=%s' % self.access_token
        data = {'touser': touser, 'command': 'Typing'}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()

    def send_typing_cancel(self, touser):
        """
        客服输入状态: 取消对用户的"正在输入"状态
        :param touser: 消息接收人的OPENID
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/typing?access_token=%s' % self.access_token
        data = {'touser': touser, 'command': 'CancelTyping'}
        content = requests.post(url, json=data).content.decode('utf8')
        return WeChatResponse(content).render()
