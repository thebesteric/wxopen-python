"""
微信验证
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/24 22:05
@info: 
"""
import hashlib

import constants
import task
from cache.cache import get_cache_instance
from client.messages import parse_message
from client.replies import SuccessReply, TextReply
from exceptions import *
from settings import WX_OPEN_CONFIG, WX_OPEN_THIRD_CONFIG
from utils.WXBizMsgCrypt import WXBizMsgCrypt
from third.router import WeChatThirdPlatformRouter

memory_cache = get_cache_instance('default')

funcs = {}


def register_msg(msg_type=None):
    """
    消息处理
    :param msg_type: 消息类型
    :return:
    """

    def decorator(func):
        _msg = type(msg_type)
        if _msg is list or _msg is tuple:
            for _msg_type in msg_type:
                funcs[_msg_type.lower()] = func
        elif _msg is str:
            funcs[msg_type.lower()] = func
        else:
            raise UnsupportedParameterTypesException(param_type=_msg)

    return decorator


def register_event(event_type=None):
    """
    消息处理
    :param event_type: 事件类型
    :return:
    """

    def decorator(func):
        _event = type(event_type)
        if _event is list or _event is tuple:
            for _msg_type in event_type:
                funcs[_msg_type.lower()] = func
        elif _event is str:
            funcs[event_type.lower()] = func
        else:
            raise UnsupportedParameterTypesException(param_type=_event)

    return decorator


def whole_network_publish_test(func):
    """
    全网发布检测
    :return:
    """

    def wrapper(message):
        msg_type = message.msg_type
        to_user_name = message.to_user_name

        if to_user_name == constants.TEST_WHOLE_NETWORK_PUBLISH_USERNAME:
            content = message.content
            if msg_type == 'text':
                # 发送普通文本信息测试
                if content == 'TESTCOMPONENT_MSG_TYPE_TEXT':
                    content += '_callback'
                    return TextReply(message, content).render()
                elif content.startswith('QUERY_AUTH_CODE:'):
                    query_auth_code = content.split(":")[1]
                    pass
            elif msg_type == 'event':
                # 发送事件推送测试
                event_type = message.event
                content = event_type + 'from_callback'
                return TextReply(message, content).render()
        else:
            func(message)

    return wrapper


class WeChatClient:
    """
    微信公众号
    """

    def __init__(self, app_id, app_secret, token, encoding_aes_key=None):
        self.app_id = app_id if app_id else WX_OPEN_CONFIG['APP_ID']
        self.app_secret = app_secret if app_secret else WX_OPEN_CONFIG['APP_SECRET']
        self.token = token if token else WX_OPEN_CONFIG['TOKEN']
        self.encoding_aes_key = encoding_aes_key if encoding_aes_key else WX_OPEN_CONFIG['ENCODING_AES_KEY']

        # 加解密能力
        if self.encoding_aes_key:
            self.crypt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.app_id)

        # 会在 check_signature 方法中赋值
        self.signature = None
        self.timestamp = None
        self.nonce = None

        WX_OPEN_CONFIG['APP_ID'] = self.app_id
        WX_OPEN_CONFIG['APP_SECRET'] = self.app_secret
        WX_OPEN_CONFIG['TOKEN'] = self.token
        WX_OPEN_CONFIG['ENCODING_AES_KEY'] = self.encoding_aes_key

        # 启动计划任务
        task.task_client_start()

    def process(self, raw_data):
        """
        消息处理
        :param raw_data: 原生微信返回的数据格式
        :return:
        """
        # 解密消息
        if self.encoding_aes_key:
            ret, raw_data = self.crypt.DecryptMsg(raw_data, self.signature, self.timestamp, self.nonce)

        message = parse_message(raw_data)
        if message.msg_type == 'event':
            if funcs.get(message.event.lower()):
                return funcs.get(message.event.lower())(message)
        else:
            if funcs.get(message.msg_type.lower()):
                return funcs.get(message.msg_type.lower())(message)
        print(UnimplementedMsgMethodException(method=message.msg_type))
        return SuccessReply().render()

    def check_signature(self, signature, timestamp, nonce):
        """
        签名校验
        :param signature: 微信加密签名
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return:
        """
        # 校验参数
        if not all([signature, timestamp, nonce]):
            raise MissingParametersException()

        # 计算签名
        li = [self.token, timestamp, nonce]
        li.sort()  # 字典排序
        tmp_str = ''.join(li)  # 拼接字符串
        _signature = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

        # 与微信服务器进行签名对比
        if _signature != signature:
            raise InvalidSignatureException()

        self.signature = signature
        self.timestamp = timestamp
        self.nonce = nonce

        return True

    @property
    def access_token(self):
        return memory_cache.get(constants.ACCESS_TOKEN)


class WeChatThirdClient:
    """
    微信第三方平台
    """

    def __init__(self, component_app_id, component_app_secret, component_token, component_encoding_aes_key):
        self.component_app_id = component_app_id if component_app_id else WX_OPEN_THIRD_CONFIG['COMPONENT_APP_ID']
        self.component_app_secret = component_app_secret if component_app_secret else WX_OPEN_THIRD_CONFIG['COMPONENT_APP_SECRET']
        self.component_token = component_token if component_token else WX_OPEN_THIRD_CONFIG['COMPONENT_TOKEN']
        self.component_encoding_aes_key = component_encoding_aes_key if component_encoding_aes_key else WX_OPEN_THIRD_CONFIG['COMPONENT_ENCODING_AES_KEY']

        # 加解密能力
        self.crypt = WXBizMsgCrypt(self.component_token, self.component_encoding_aes_key, self.component_app_id)

        # API 路由能力
        self.router = WeChatThirdPlatformRouter(self.component_app_id, self.component_app_secret, self.component_access_token)

        # 会在 check_signature 方法中赋值
        self.signature = None
        self.timestamp = None
        self.nonce = None

        WX_OPEN_THIRD_CONFIG['COMPONENT_APP_ID'] = self.component_app_id
        WX_OPEN_THIRD_CONFIG['COMPONENT_APP_SECRET'] = self.component_app_secret
        WX_OPEN_THIRD_CONFIG['COMPONENT_TOKEN'] = self.component_token
        WX_OPEN_THIRD_CONFIG['COMPONENT_ENCODING_AES_KEY'] = self.component_encoding_aes_key

        # 启动计划任务
        task.task_third_start()

    def process(self, raw_data):
        """
        消息处理
        :param raw_data: 原生微信返回的数据格式
        :return:
        """
        # 解密消息
        ret, raw_data = self.crypt.DecryptMsg(raw_data, self.signature, self.timestamp, self.nonce)

        # 存储 ComponentVerifyTicket
        if raw_data['InfoType'] == 'component_verify_ticket':
            memory_cache.set(constants.COMPONENT_VERIFY_TICKET, raw_data['ComponentVerifyTicket'])
            return SuccessReply().render()

        message = parse_message(raw_data)
        to_user_name = message.to_user_name
        content = message.content

        if message.msg_type == 'event':
            # 全网发布检测（事件级别）
            if to_user_name == constants.TEST_WHOLE_NETWORK_PUBLISH_USERNAME:
                event_type = message.event
                content = event_type + 'from_callback'
                return TextReply(message, content).render()

            # 事件消息注册
            if funcs.get(message.event.lower()):
                return funcs.get(message.event.lower())(message)
        else:
            # 全网发布检测（消息级别）
            if to_user_name == constants.TEST_WHOLE_NETWORK_PUBLISH_USERNAME:
                if message.msg_type.lower() == 'text':

                    # 测试公众号处理用户消息
                    if content == 'TESTCOMPONENT_MSG_TYPE_TEXT':
                        content += '_callback'
                        return TextReply(message, content).render()

                    # 测试公众号使用客服消息接口处理用户消息
                    elif content.startswith('QUERY_AUTH_CODE:'):
                        query_auth_code = content.split(":")[1]
                        result = self.router.api_query_auth(query_auth_code)
                        authorizer_access_token = result['authorization_info']['authorizer_access_token']
                        from_user_name = message.from_user_name
                        content = query_auth_code + '_from_api'
                        from client.request import CustomerRequest
                        return CustomerRequest(authorizer_access_token).send_text(from_user_name, content)

            # 常规消息注册
            if funcs.get(message.msg_type.lower()):
                return funcs.get(message.msg_type.lower())(message)

        print(UnimplementedMsgMethodException(method=message.msg_type))
        return SuccessReply().render()

    def check_signature(self, signature, timestamp, nonce):
        """
        签名校验
        :param signature: 微信加密签名
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return:
        """
        # 校验参数
        if not all([signature, timestamp, nonce]):
            raise MissingParametersException()

        # 计算签名
        li = [self.component_token, timestamp, nonce]
        li.sort()  # 字典排序
        tmp_str = ''.join(li)  # 拼接字符串
        _signature = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

        # 与微信服务器进行签名对比
        if _signature != signature:
            raise InvalidSignatureException()

        self.signature = signature
        self.timestamp = timestamp
        self.nonce = nonce

        return True

    @property
    def component_access_token(self):
        return memory_cache.get(constants.COMPONENT_ACCESS_TOKEN)
