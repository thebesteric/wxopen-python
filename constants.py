"""
常量
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/25 14:49
@info: 
"""

from enum import Enum, unique

ACCESS_TOKEN = 'access_token'


@unique
class MsgType(Enum):
    """
    消息类型枚举
    """

    TEXT = 'text'  # 文本消息，可用于接收，可用于回复
    IMAGE = 'image'  # 图片消息，可用于接收，可用于回复
    VOICE = 'voice'  # 语音消息，可用于接收，可用于回复
    VIDEO = 'video'  # 视频消息，可用于接收，可用于回复
    MUSIC = 'music'  # 音乐消息，仅于回复
    NEWS = 'news'  # 图文消息，仅于回复
    SHORT_VIDEO = 'shortvideo'  # 小视频消息，仅用于接收，不可用于回复
    LOCATION = 'location'  # 地理位置消息，仅用于接收，不可用于回复
    LINK = 'link'  # 链接消息，仅用于接收，不可用于回复
    EVENT = 'event'  # 事件消息，仅用于接收，不可用于回复

    @unique
    class EventType(Enum):
        """
        事件类型枚举
        当消 MsgType = EVENT, 会产生如下事件
        """

        SUBSCRIBE = 'subscribe'  # 订阅
        UN_SUBSCRIBE = 'unsubscribe'  # 取消订阅
        SCAN = "SCAN"  # 扫描带参数二维码事件：用户已关注后继续扫码才会出现
        LOCATION = 'LOCATION'  # 上报地理位置事件
        CLICK = 'CLICK'  # 点击菜单：拉取消息时的事件
        VIEW = 'VIEW'  # 点击菜单：跳转链接时的事件
        SCANCODE_PUSH = 'scancode_push'  # 点击菜单：扫码推事件的事件推送
        SCANCODE_WAITMSG = 'scancode_waitmsg'  # 点击菜单：扫码推事件且弹出“消息接收中”提示框的事件推送
        PIC_SYSPHOTO = 'pic_sysphoto'  # 点击菜单：弹出系统拍照发图的事件推送
        PIC_PHOTO_OR_ALBUM = 'pic_photo_or_album'  # 点击菜单：弹出拍照或者相册发图的事件推送
        PIC_WEIXIN = 'pic_weixin'  # 点击菜单：弹出微信相册发图器的事件推送
        LOCATION_SELECT = 'location_select'  # 点击菜单：弹出地理位置选择器的事件推送
        VIEW_MINIPROGRAM = 'view_miniprogram'  # 点击菜单：跳转小程序的事件推送
