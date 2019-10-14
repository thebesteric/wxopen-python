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

"""
验证票据（component_verify_ticket）
在第三方平台创建审核通过后，微信服务器会向其 ”授权事件接收URL” 每隔 10 分钟以 POST 的方式推送 component_verify_ticket
"""
COMPONENT_VERIFY_TICKET = 'component_verify_ticket'

"""
令牌（component_access_token）是第三方平台接口的调用凭据。
令牌的获取是有限制的，每个令牌的有效期为 2 小时，请自行做好令牌的管理，在令牌快过期时（比如1小时50分），重新调用接口获取。
如未特殊说明，令牌一般作为被调用接口的 GET 参数 component_access_token 的值使用
"""
COMPONENT_ACCESS_TOKEN = 'component_access_token'  # 接口的调用凭据

"""
接口调用令牌
在公众号/小程序接口调用令牌（authorizer_access_token）失效时，可以使用刷新令牌（authorizer_refresh_token）获取新的接口调用令牌
"""
AUTHORIZER_ACCESS_TOKEN = 'authorizer_access_token '  # 接口调用令牌

"""
自动化测试的专用测试公众号的信息（全网发布测试用）
"""
TEST_WHOLE_NETWORK_PUBLISH_APPID = 'wx570bc396a51b8ff8'
TEST_WHOLE_NETWORK_PUBLISH_USERNAME = 'gh_3c884a361561'

"""
自动化测试的专用测试小程序的信息（全网发布测试用）
"""
TEST_WHOLE_NETWORK_MINGROGRAM_APPID = 'wxd101a85aa106f53e'
TEST_WHOLE_NETWORK_MINGROGRAM_USERNAME = 'gh_8dad206e9538'


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
