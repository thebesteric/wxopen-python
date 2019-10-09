"""
账号管理请求服务
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/8 14:43
@info: 
"""

from client.request.base.wxrequest import WeChatRequest
import json
import requests
import exceptions


class AccountRequest(WeChatRequest):
    """
    账号管理请求
    """

    def __create_qr_code(self, action_name, action_info, expire_seconds=None):
        """
        创建二维码
        :param action_name: 二维码类型，QR_SCENE为临时的整型参数值，QR_STR_SCENE为临时的字符串参数值，QR_LIMIT_SCENE为永久的整型参数值，QR_LIMIT_STR_SCENE为永久的字符串参数值
        :param action_info: 二维码详细信息
        :param expire_seconds: 单位秒，最大不超过 2592000
        :return ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
        """
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % self.access_token
        data = {'action_name': action_name, 'action_info': {'scene': action_info}}
        if expire_seconds:
            if expire_seconds < 30:
                expire_seconds = 30
            elif expire_seconds > 2592000:
                expire_seconds = 2592000
            data.update({'expire_seconds': expire_seconds})
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')

    def create_qr_scene(self, scene_id, expire_seconds=2592000):
        """
        创建含整型参数值的临时二维码
        :param scene_id: 场景值ID，临时二维码时为32位非0整型
        :param expire_seconds: 单位秒，最大不超过 2592000
        :return ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
        """
        try:
            scene_id = int(scene_id)
        except Exception:
            raise exceptions.UnsupportedParameterTypesException()

        if scene_id == 0:
            raise exceptions.ValidationException('scene_id must not be 0')

        action_info = {'scene_id': scene_id}
        return self.__create_qr_code('QR_SCENE', action_info, expire_seconds)

    def create_qr_str_scene(self, scene_str, expire_seconds=2592000):
        """
        创建含字符串参数值的临时二维码
        :param scene_str: 场景值ID（字符串形式的ID），字符串类型，长度限制为1到64
        :param expire_seconds: 单位秒，最大不超过 2592000
        :return ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
        """
        if scene_str and len(scene_str) > 64:
            raise exceptions.ValidationException('scene_str length must in {} between {}'.format(1, 64))

        action_info = {'scene_str': scene_str}
        return self.__create_qr_code('QR_STR_SCENE', action_info, expire_seconds)

    def create_limit_qr_scene(self, scene_id):
        """
        创建含整型参数值的永久二维码
        :param scene_id: 场景值ID，二维码时最大值为100000（目前参数只支持1--100000）
        :return ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
        """
        try:
            scene_id = int(scene_id)
        except Exception:
            raise exceptions.UnsupportedParameterTypesException()

        if scene_id < 1 or scene_id > 100000:
            raise exceptions.ValidationException('scene_id must in {} between {}'.format(1, 100000))

        action_info = {'scene_id': scene_id}
        return self.__create_qr_code('QR_LIMIT_SCENE', action_info)

    def create_limit_qr_str_scene(self, scene_str):
        """
        创建含字符串参数值的永久二维码
        :param scene_str: 场景值ID（字符串形式的ID），字符串类型，长度限制为1到64
        :return ticket: 获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码
        """
        if scene_str and len(scene_str) > 64:
            raise exceptions.ValidationException('scene_str length must in {} between {}'.format(1, 64))

        action_info = {'scene_str': scene_str}
        return self.__create_qr_code('QR_LIMIT_STR_SCENE', action_info)

    def load_qr_code(self, ticket):
        """
        通过ticket换取二维码，显示二维码图片
        :param ticket: 获取的二维码ticket
        :return: 流
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s' % ticket
        content = requests.get(url).content
        return content

    def short_url(self, long_url):
        """
        长链接转成短链接
        :param long_url: 长链接
        :return: 短链接
        """
        url = 'https://api.weixin.qq.com/cgi-bin/shorturl?access_token=%s' % self.access_token
        data = {'action': 'long2short', 'long_url': long_url}
        content = requests.post(url, json=data).content.decode('utf8')
        return json.loads(content, encoding='utf8')
