"""
消息处理
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/24 23:11
@info: 
"""

import xmltodict
import json
from client.domain import wxerror


def parse_message(raw_message):
    """
    消息解析
    :param raw_message: 原始消息
    :return: dict
    """
    xml_dict = xmltodict.parse(raw_message).get('xml')
    msg_type = xml_dict.get('MsgType')
    message = BaseMessage(xml_dict)
    if msg_type == 'text':
        message = TextMessage(xml_dict)
    elif msg_type == 'image':
        message = ImageMessage(xml_dict)
    elif msg_type == 'voice':
        message = VoiceMessage(xml_dict)
    elif msg_type == 'video':
        message = VideoMessage(xml_dict)
    elif msg_type == 'shortvideo':
        message = ShortVideoMessage(xml_dict)
    elif msg_type == 'location':
        message = LocationMessage(xml_dict)
    elif msg_type == 'link':
        message = LinkMessage(xml_dict)
    elif msg_type == 'event':
        event = xml_dict.get('Event').lower()
        if event in ['subscribe', 'unsubscribe']:
            message = EventSubscribeMessage(xml_dict)
        elif event == 'scan':
            message = EventQrSceneMessage(xml_dict)
        elif event == 'location':
            message = EventLocationMessage(xml_dict)
        elif event == 'click':
            message = EventClickMessage(xml_dict)
        elif event in ['view', 'view_miniprogram']:
            message = EventViewMessage(xml_dict)
        elif event in ['scancode_push', 'scancode_waitmsg']:
            message = EventScanCodeMessage(xml_dict)
        elif event in ['pic_sysphoto', 'pic_photo_or_album', 'pic_weixin']:
            message = EventPicPhotoMessage(xml_dict)
    return message


class BaseMessage:
    """
    消息基类
    MsgId: 消息id，64位整型
    ToUserName: 开发者微信号
    FromUserName: 发送方帐号（一个OpenID）
    MsgType: 消息类型
    CreateTime: 消息创建时间 （整型）
    """

    def __init__(self, xml_dict):
        self.msg_id = xml_dict.get('MsgId', 0)
        self.to_user_name = xml_dict.get('ToUserName')
        self.from_user_name = xml_dict.get('FromUserName')
        self.msg_type = xml_dict.get('MsgType')
        self.create_time = xml_dict.get('CreateTime')
        self.raw_data = xml_dict

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class BaseEventMessage(BaseMessage):
    """
    事件消息基类
    Event: 事件类型
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event = xml_dict.get('Event')


class TextMessage(BaseMessage):
    """
    文本消息
    MsgType: text
    Content: 文本消息内容
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.content = xml_dict.get('Content')

    def __str__(self):
        return str(self.__dict__)


class ImageMessage(BaseMessage):
    """
    图片消息
    MsgType: image
    MediaId: 图片消息媒体id，可以调用获取临时素材接口拉取数据
    PicUrl: 图片链接（由系统生成）
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.media_id = xml_dict.get('MediaId')
        self.pic_url = xml_dict.get('PicUrl')

    def __str__(self):
        return str(self.__dict__)


class VoiceMessage(BaseMessage):
    """
    音频消息
    MsgType: voice
    请注意，开通语音识别后，用户每次发送语音给公众号时，微信会在推送的语音消息XML数据包中，增加一个Recognition字段
    注: 由于客户端缓存，开发者开启或者关闭语音识别功能，对新关注者立刻生效，对已关注用户需要24小时生效。开发者可以重新关注此帐号进行测试）Format格式固定为amr
    Recognition: 语音识别结果，UTF8编码
    Format: 语音格式，如amr，speex等
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.media_id = xml_dict.get('MediaId')
        self.format = xml_dict.get('Format')
        self.recognition = xml_dict.get('Recognition')

    def __str__(self):
        return str(self.__dict__)


class VideoMessage(BaseMessage):
    """
    视频消息
    MsgType: video
    MediaId: 视频消息媒体id，可以调用获取临时素材接口拉取数据
    ThumbMediaId: 视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.media_id = xml_dict.get('MediaId')
        self.thumb_media_id = xml_dict.get('ThumbMediaId')

    def __str__(self):
        return str(self.__dict__)


class ShortVideoMessage(BaseMessage):
    """
    小视频消息
    MsgType: shortvideo
    MediaId: 视频消息媒体id，可以调用获取临时素材接口拉取数据
    ThumbMediaId: 视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.media_id = xml_dict.get('MediaId')
        self.thumb_media_id = xml_dict.get('ThumbMediaId')

    def __str__(self):
        return str(self.__dict__)


class LocationMessage(BaseMessage):
    """
    地理位置消息
    MsgType: location
    Location_X: 地理位置维度
    Location_Y: 地理位置经度
    Scale: 地图缩放大小
    Label: 地理位置信息
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.location_x = xml_dict.get('Location_X')
        self.location_y = xml_dict.get('Location_Y')
        self.scale = xml_dict.get('Scale')
        self.label = xml_dict.get('Label')

    def __str__(self):
        return str(self.__dict__)


class LinkMessage(BaseMessage):
    """
    链接消息
    MsgType: link
    Title: 消息标题
    Description: 消息描述
    Url: 消息链接
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.title = xml_dict.get('Title')
        self.description = xml_dict.get('Description')
        self.url = xml_dict.get('Url')

    def __str__(self):
        return str(self.__dict__)


class EventSubscribeMessage(BaseEventMessage):
    """
    关注/取消关注事件
    MsgType: event
    Event: subscribe / unsubscribe
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        if xml_dict.get('EventKey'):
            self.event_key = xml_dict.get('EventKey')

    def __str__(self):
        return str(self.__dict__)


class EventQrSceneMessage(BaseEventMessage):
    """
    扫描带参数二维码事件
    MsgType: event
    用户扫描带场景值二维码时，可能推送以下两种事件：
    1、如果用户还未关注公众号，则用户可以关注公众号，关注后微信会将带场景值关注事件推送给开发者。
        Event: 事件类型，subscribe, 该事件会自动转为'关注事件'
        EventKey: 事件KEY值，qrscene_为前缀，后面为二维码的参数值
    2、如果用户已经关注公众号，则微信会将带场景值扫描事件推送给开发者。
        Event: 事件类型，SCAN
        EventKey: 事件KEY值，是一个32位无符号整数，即创建二维码时的二维码scene_id
    Ticket: 二维码的ticket，可用来换取二维码图片
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event_key = xml_dict.get('EventKey')
        self.ticket = xml_dict.get('Ticket')

    def __str__(self):
        return str(self.__dict__)


class EventLocationMessage(BaseEventMessage):
    """
    上报地理位置事件
    MsgType: event
    Event: LOCATION
    Latitude: 地理位置纬度
    Longitude: 地理位置经度
    Precision: 地理位置精度
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.latitude = xml_dict.get('Latitude')
        self.longitude = xml_dict.get('Longitude')
        self.precision = xml_dict.get('Precision')

    def __str__(self):
        return str(self.__dict__)


class EventClickMessage(BaseEventMessage):
    """
    菜单事件: 点击菜单拉取消息时的事件推送
    MsgType: event
    Event: CLICK
    EventKey: 事件KEY值，与自定义菜单接口中KEY值对应
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event_key = xml_dict.get('EventKey')

    def __str__(self):
        return str(self.__dict__)


class EventViewMessage(BaseEventMessage):
    """
    菜单事件: 菜单跳转事件
    1、点击菜单跳转链接时的事件推送
        Event: VIEW
        EventKey: 事件KEY值，设置的跳转URL
    2、跳转小程序的事件推送
        Event: view_miniprogram
        EventKey: 事件KEY值，跳转的小程序路径
    MsgType: event
    MenuId: 指菜单ID，如果是个性化菜单，则可以通过这个字段，知道是哪个规则的菜单被点击了
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event_key = xml_dict.get('EventKey')
        self.menu_id = xml_dict.get('MenuId')

    def __str__(self):
        return str(self.__dict__)


class EventScanCodeMessage(BaseEventMessage):
    """
    菜单事件: 扫码事件
    1、扫码推事件的事件推送
        Event: scancode_push
    2、扫码推事件且弹出“消息接收中”提示框的事件推送
        Event: scancode_waitmsg
    MsgType: event
    EventKey: 事件KEY值，由开发者在创建菜单时设定
    ScanCodeInfo: 扫描信息
    ScanType: 扫描类型，一般是qrcode
    ScanResult: 扫描结果，即二维码对应的字符串信息
    """

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event_key = xml_dict.get('EventKey')
        self.scan_code_info = xml_dict.get('ScanCodeInfo')
        self.scan_type = xml_dict.get('ScanType')
        self.scan_result = xml_dict.get('ScanResult')

    def __str__(self):
        return str(self.__dict__)


class EventPicPhotoMessage(BaseEventMessage):
    """
    菜单事件: 拍照事件
    1、弹出系统拍照发图的事件推送
        Event: pic_sysphoto
    2、弹出拍照或者相册发图的事件推送
        Event: pic_photo_or_album
    3、弹出微信相册发图器的事件推送
        Event: pic_weixin
    MsgType: event
    EventKey: 事件KEY值，设置的跳转URL
    SendPicsInfo: 发送的图片信息
        Count: 发送的图片数量
        PicList: 图片列表
            PicMd5Sum: 图片的MD5值，开发者若需要，可用于验证接收到图片
    """

    class ScanCodeInfo:
        def __init__(self, send_pics_info_dict):
            self.count = send_pics_info_dict.get('Count')
            self.pic_list = self.PicList(send_pics_info_dict.get('PicList')) if send_pics_info_dict else None

        class PicList:
            def __init__(self, pic_list_dict):
                self.item = self.Item(pic_list_dict.get('item')) if pic_list_dict else None

            class Item:
                def __init__(self, item_dict):
                    self.pic_md5_sum = item_dict.get('PicMd5Sum') if item_dict else None

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event_key = xml_dict.get('EventKey')
        self.scan_code_info = self.ScanCodeInfo(xml_dict.get('SendPicsInfo'))

    def __str__(self):
        return str(self.__dict__)


class EventLocationSelectMessage(BaseEventMessage):
    """
    菜单事件: 弹出地理位置选择器的事件推送
    MsgType: event
    Event: location_select
    EventKey: 事件KEY值，设置的跳转URL
    SendLocationInfo: 发送的位置信息
        Location_X: X坐标信息
        Location_Y: Y坐标信息
        Scale: 精度，可理解为精度或者比例尺、越精细的话 scale越高
        Label: 地理位置的字符串信息
        Poiname: 朋友圈POI的名字，可能为空
    """

    class SendLocationInfo:
        def __init__(self, send_location_info_dict):
            self.location_x = send_location_info_dict.get('Location_X')
            self.location_y = send_location_info_dict.get('Location_Y')
            self.scale = send_location_info_dict.get('Scale')
            self.label = send_location_info_dict.get('Label')
            self.poiname = send_location_info_dict.get('Poiname')

    def __init__(self, xml_dict):
        super().__init__(xml_dict)
        self.event_key = xml_dict.get('EventKey')
        self.send_location_info = self.SendLocationInfo(xml_dict.get('SendLocationInfo'))
