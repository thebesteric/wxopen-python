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

from cache.cache import get_cache_instance
from client.messages import parse_message
from client.replies import SuccessReply
from client.task import task_start
from exceptions import *
from client.constants import ACCESS_TOKEN
from settings import WX_OPEN_CONFIG
from utils.WXBizMsgCrypt import WXBizMsgCrypt

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


class WeChatClient:

    def __init__(self, app_id, app_secret, token, encoding_aes_key=None):
        self.app_id = app_id if app_id else WX_OPEN_CONFIG['APP_ID']
        self.app_secret = app_secret if app_secret else WX_OPEN_CONFIG['APP_SECRET']
        self.token = token if token else WX_OPEN_CONFIG['TOKEN']
        self.encoding_aes_key = encoding_aes_key if encoding_aes_key else WX_OPEN_CONFIG['ENCODING_AES_KEY']

        self.signature = None
        self.timestamp = None
        self.nonce = None

        WX_OPEN_CONFIG['APP_ID'] = self.app_id
        WX_OPEN_CONFIG['APP_SECRET'] = self.app_secret
        WX_OPEN_CONFIG['TOKEN'] = self.token
        WX_OPEN_CONFIG['ENCODING_AES_KEY'] = self.encoding_aes_key

        # 启动计划任务
        task_start()

    def process(self, raw_data):
        """
        消息处理
        :param raw_data: 原生微信返回的数据格式
        :return:
        """
        if self.encoding_aes_key:
            decrypt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.app_id)
            ret, raw_data = decrypt.DecryptMsg(raw_data, self.signature, self.timestamp, self.nonce)

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
        return memory_cache.get(ACCESS_TOKEN)
