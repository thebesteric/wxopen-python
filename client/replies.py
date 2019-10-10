"""
微信消息响应
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/25 17:07
@info: 
"""
import time

import xmltodict

from client.constants import MsgType
from utils.WXBizMsgCrypt import WXBizMsgCrypt
from settings import WX_OPEN_CONFIG
import random


class BaseReply:
    """ 消息回复（基类） """

    ToUserName = None  # 开发者微信号
    FromUserName = None  # 发送方帐号（一个OpenID）
    CreateTime = None  # 消息创建时间 （整型）

    def __init__(self, message=None):
        """
        初始化
        :param message: 接收到微信的消息对象
        """
        self.ToUserName = message.from_user_name if message else None
        self.FromUserName = message.to_user_name if message else None
        self.CreateTime = int(time.time())

    def dict(self):
        return {'xml': self.__dict__}

    def render(self):
        xml_response = xmltodict.unparse(self.dict())
        if WX_OPEN_CONFIG['ENCODING_AES_KEY']:
            encrypt = WXBizMsgCrypt(WX_OPEN_CONFIG['token'], WX_OPEN_CONFIG['ENCODING_AES_KEY'], WX_OPEN_CONFIG['APP_ID'])
            ret, xml_response = encrypt.EncryptMsg(xml_response, self._get_nonce())
        return xml_response

    def _get_nonce(self):
        return ''.join([str(random.randint(0, 9)) for i in range(10)])


class SuccessReply(BaseReply):
    """
    回复空串
    微信服务器不会对此作任何处理，并且不会发起重试
    """

    def render(self):
        return 'success'


class TextReply(BaseReply):
    """
    文本消息
    (*) content：回复的消息内容（换行：在content中能够换行，微信客户端就支持换行显示）
    """

    def __init__(self, message, content=None, to_user_name=None):
        super().__init__(message)
        self.MsgType = MsgType.TEXT.value
        if to_user_name:
            self.ToUserName = to_user_name
        self.Content = content if content else message.content


class ImageReply(BaseReply):
    """
    图片消息
    (*) media_id：通过素材管理中的接口上传多媒体文件，得到的id
    """

    def __init__(self, message, media_id):
        super().__init__(message)
        self.MsgType = MsgType.IMAGE.value
        self.Image = {'MediaId': media_id}


class VoiceReply(BaseReply):
    """
    音频消息
    (*) media_id：通过素材管理中的接口上传多媒体文件，得到的id
    """

    def __init__(self, message, media_id):
        super().__init__(message)
        self.MsgType = MsgType.VOICE.value
        self.Voice = {'MediaId': media_id}


class VideoReply(BaseReply):
    """
    视频消息
    (*) media_id：通过素材管理中的接口上传多媒体文件，得到的id
    title：视频消息的标题
    description：视频消息的描述
    """

    def __init__(self, message, media_id, title, description):
        super().__init__(message)
        self.MsgType = MsgType.VIDEO.value
        self.Video = {'MediaId': media_id}
        self.Video.update({'Title': title}) if title else None
        self.Video.update({'Description': description}) if description else None


class MusicReply(BaseReply):
    """
    音乐消息
    (*) thumb_media_id：缩略图的媒体id，通过素材管理中的接口上传多媒体文件，得到的id
    Title：音乐标题
    title：音乐描述
    music_url：音乐链接
    hq_music_url：高质量音乐链接，WIFI环境优先使用该链接播放音乐
    """

    def __init__(self, message, thumb_media_id, title=None, description=None, music_url=None, hq_music_url=None):
        super().__init__(message)
        self.MsgType = MsgType.MUSIC.value
        self.Music = {'ThumbMediaId': thumb_media_id}
        self.Music.update({'Title': title}) if title else None
        self.Music.update({'Description': description}) if description else None
        self.Music.update({'MusicURL': music_url}) if music_url else None
        self.Music.update({'HQMusicUrl': hq_music_url}) if hq_music_url else None


class NewsReply:
    """
    图文消息
    (*) ArticleCount：图文消息个数；当用户发送文本、图片、视频、图文、地理位置这五种消息时，开发者只能回复1条图文消息；其余场景最多可回复8条图文消息
    (*) Articles：图文消息信息，注意，如果图文数超过限制，则将只发限制内的条数
    (*) Title：图文消息标题
    (*) Description：图文消息描述
    (*) PicUrl：图片链接，支持JPG、PNG格式，较好的效果为大图360*200，小图200*200
    (*) Url：点击图文消息跳转链接
    """

    class NewsItem:
        def __init__(self, title, description, pic_url, url):
            self.Title = title
            self.Description = description
            self.PicUrl = pic_url
            self.Url = url

    def __init__(self, message, news_items=None):
        items_str = ''
        for item in news_items:
            item_str = """
                <item>
                    <Title><![CDATA[{Title}]]></Title>
                    <Description><![CDATA[{Description}]]></Description>
                    <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
                    <Url><![CDATA[{Url}]]></Url>
                </item>
                """.format(Title=item.Title, Description=item.Description, PicUrl=item.PicUrl, Url=item.Url)
            items_str += item_str

        self.xml_str = """
            <xml>
                <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
                <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>{ArticleCount}</ArticleCount>
                <Articles>{items}</Articles>
            </xml>
            """.format(FromUserName=message.from_user_name, ToUserName=message.to_user_name,
                       CreateTime=int(time.time()), ArticleCount=len(news_items), items=items_str)

    def render(self):
        return self.xml_str.replace(' ', '')
