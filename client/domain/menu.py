"""
菜单
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/26 17:33
@info: 
"""
import json
from enum import Enum, unique
from client.request.menu import MenuRequest

"""
1、自定义菜单最多包括3个一级菜单，每个一级菜单最多包含5个二级菜单。
2、一级菜单最多4个汉字，二级菜单最多7个汉字，多出来的部分将会以“...”代替。
3、创建自定义菜单后，菜单的刷新策略是：
    a、在用户进入公众号会话页或公众号profile页时，如果发现上一次拉取菜单的请求在5分钟以前，就会拉取一下菜单，如果菜单有更新，就会刷新客户端的菜单。
    b、测试时可以尝试取消关注公众账号后再次关注，则可以看到创建后的效果。
"""


class Menu:
    """
    公众号菜单
    菜单下必须要有按钮
    """

    button = None  # 包含的按钮

    def __init__(self, *buttons, matchrule=None):
        self.button = list(buttons)
        if matchrule is not None:
            self.matchrule = matchrule.__dict__

    def create(self):
        """
        创建/更新公众号菜单
        :return:
        """
        return MenuRequest().create(self)

    def to_dict(self):
        _dict = {'button': [btn.to_dict() for btn in self.button]}
        if self.matchrule is not None:
            _dict['matchrule'] = self.matchrule
        return _dict

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @staticmethod
    def keys():
        return {'button'}

    def __getitem__(self, item):
        return getattr(self, item)


class Button:
    """
    公众号按钮
    按钮必须属于菜单
    """

    @unique
    class TYPE(Enum):
        """按钮类型"""

        """
        请注意，3到8的所有事件，仅支持微信iPhone5.4.1以上版本，和Android5.4以上版本的微信用户，
        旧版本微信用户点击后将没有回应，开发者也不能正常接收到事件推送。
        MEDIA_ID 和 VIEW_LIMITED，是专门给第三方平台旗下未微信认证（具体而言，是资质认证未通过）的订阅号准备的事件类型，
        它们是没有事件推送的，能力相对受限，其他类型的公众号不必使用。
        
        name: 菜单标题，不超过16个字节，子菜单不超过60个字节
        type: 菜单的响应动作类型，view表示网页类型，click表示点击类型，miniprogram表示小程序类型
        key: 菜单KEY值，用于消息接口推送，不超过128字节
        url: view、miniprogram类型必填，网页 链接，用户点击菜单可打开链接，不超过1024字节。 type为miniprogram时，不支持小程序的老版本客户端将打开本url。
        appid: 小程序的appid（仅认证公众号可配置）
        pagepath: 小程序的页面路径
        media_id: media_id类型和view_limited类型必须，调用新增永久素材接口返回的合法media_id
        sub_button: 二级菜单数组，个数应为1~5个
        """
        CLICK = 'click'  # 点击推事件用户点击click类型按钮后，微信服务器会通过消息接口推送消息类型为event的结构给开发者（参考消息接口指南），并且带上按钮中开发者填写的key值，开发者可以通过自定义的key值与用户进行交互
        VIEW = 'view'  # 跳转URL用户点击view类型按钮后，微信客户端将会打开开发者在按钮中填写的网页URL，可与网页授权获取用户基本信息接口结合，获得用户基本信息
        SCANCODE_PUSH = 'scancode_push'  # 扫码推事件用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后显示扫描结果（如果是URL，将进入URL），且会将扫码的结果传给开发者，开发者可以下发消息
        SCANCODE_WAITMSG = 'scancode_waitmsg'  # 扫码推事件且弹出“消息接收中”提示框用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后，将扫码的结果传给开发者，同时收起扫一扫工具，然后弹出“消息接收中”提示框，随后可能会收到开发者下发的消息
        PIC_SYSPHOTO = 'pic_sysphoto'  # 弹出系统拍照发图用户点击按钮后，微信客户端将调起系统相机，完成拍照操作后，会将拍摄的相片发送给开发者，并推送事件给开发者，同时收起系统相机，随后可能会收到开发者下发的消息
        PIC_PHOTO_OR_ALBUM = 'pic_photo_or_album'  # 弹出拍照或者相册发图用户点击按钮后，微信客户端将弹出选择器供用户选择“拍照”或者“从手机相册选择”。用户选择后即走其他两种流程
        PIC_WEIXIN = 'pic_weixin'  # 弹出微信相册发图器用户点击按钮后，微信客户端将调起微信相册，完成选择操作后，将选择的相片发送给开发者的服务器，并推送事件给开发者，同时收起相册，随后可能会收到开发者下发的消息
        LOCATION_SELECT = 'location_select'  # 弹出地理位置选择器用户点击按钮后，微信客户端将调起地理位置选择工具，完成选择操作后，将选择的地理位置发送给开发者的服务器，同时收起位置选择工具，随后可能会收到开发者下发的消息
        MEDIA_ID = 'media_id'  # 下发消息（除文本消息）用户点击media_id类型按钮后，微信服务器会将开发者填写的永久素材id对应的素材下发给用户，永久素材类型可以是图片、音频、视频、图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id
        VIEW_LIMITED = 'view_limited'  # 跳转图文消息URL用户点击view_limited类型按钮后，微信客户端将打开开发者在按钮中填写的永久素材id对应的图文消息URL，永久素材类型只支持图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id

    def __init__(self, name=None, type=None, key=None, url=None, appid=None, pagepath=None, media_id=None,
                 sub_button=None):
        if name is not None:
            self.name = name
        if type is not None:
            if isinstance(type, Enum):
                self.type = type.value
            elif isinstance(type, str):
                self.type = type
            else:
                raise TypeError('Wrong types, must be Enum or str')
        if key is not None:
            self.key = key
        if url is not None:
            self.url = url
        if appid is not None:
            self.appid = appid
        if pagepath is not None:
            self.pagepath = pagepath
        if media_id is not None:
            self.media_id = media_id
        if sub_button is not None:
            self.sub_button = [btn.__dict__ for btn in sub_button]

    def to_dict(self):
        return json.loads(self.to_json())

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    @staticmethod
    def keys():
        return {'name', 'type', 'key', 'url', 'appid', 'pagepath', 'media_id', 'sub_button'}

    def __getitem__(self, item):
        return getattr(self, item)


class MatchRule:
    """
    菜单匹配规则
    tag_id: 用户标签的id，可通过用户标签管理接口获取
    sex: 性别：男（1）女（2），不填则不做匹配
    client_platform_type: 客户端版本，当前只具体到系统型号：IOS(1), Android(2),Others(3)，不填则不做匹配
    country: 国家信息，是用户在微信中设置的地区，具体请参考地区信息表
    province: 省份信息，是用户在微信中设置的地区，具体请参考地区信息表
    city: 城市信息，是用户在微信中设置的地区，具体请参考地区信息表
    language: 语言信息，是用户在微信中设置的语言，具体请参考语言表：
        1、简体中文 "zh_CN" 2、繁体中文TW "zh_TW" 3、繁体中文HK "zh_HK" 4、英文 "en" 5、印尼 "id" 6、马来 "ms"
        7、西班牙 "es" 8、韩国 "ko" 9、意大利 "it" 10、日本 "ja" 11、波兰 "pl" 12、葡萄牙 "pt" 13、俄国 "ru" 14、泰文 "th"
        15、越南 "vi" 16、阿拉伯语 "ar" 17、北印度 "hi" 18、希伯来 "he" 19、土耳其 "tr" 20、德语 "de" 21、法语 "fr"
    """

    def __init__(self, tag_id=None, sex=None, client_platform_type=None, country=None, province=None, city=None, language='zh_CN'):
        if tag_id is not None:
            self.tag_id = tag_id
        if sex is not None:
            self.sex = sex
        if client_platform_type is not None:
            self.client_platform_type = client_platform_type
        if country is not None:
            self.country = country
        if province is not None:
            self.province = province
        if city is not None:
            self.city = city
        if language is not None:
            self.language = language

    def to_dict(self):
        return json.loads(self.to_json())

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


if __name__ == '__main__':
    sub_btn_1_1 = Button(name='扫码带提示', type=Button.TYPE.SCANCODE_WAITMSG, key='SCANCODE_WAITMSG')
    sub_btn_1_2 = Button(name='扫码推事件', type=Button.TYPE.SCANCODE_PUSH, key='SCANCODE_PUSH')
    btn1 = Button(name='扫码查询', sub_button=[sub_btn_1_1, sub_btn_1_2])
    btn2 = Button(name='百度搜索', type=Button.TYPE.VIEW, url='https://www.baidu.com')
    btn3 = Button(name='拍照发图', type=Button.TYPE.PIC_PHOTO_OR_ALBUM, key='PIC_PHOTO_OR_ALBUM')
    menu = Menu(btn1, btn2, btn3)
    print(menu.to_dict())
    print(menu.to_dict())
    print(menu.create())
