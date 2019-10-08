"""
微信异常
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/24 23:26
@info: 
"""


class WeChatException(Exception):
    """
    Base WeChat Exception
    """

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return 'Error code: {code}, message: {msg}'.format(code=self.errcode, msg=self.errmsg)

    def __repr__(self):
        return 'Error class: {clazz}, code: {code}, message: {msg}'.format(clazz=self.__class__.__name__, code=self.errcode, msg=self.errmsg)


class InvalidSignatureException(WeChatException):
    """错误的签名"""

    def __init__(self, errcode=-40001, errmsg='Invalid Signature'):
        super().__init__(errcode, errmsg)


class MissingParametersException(WeChatException):
    """缺失参数"""

    def __init__(self, errcode=-60000, errmsg='Missing Parameters'):
        super().__init__(errcode, errmsg)


class UnimplementedMsgMethodException(WeChatException):
    """未实现的方法"""

    def __init__(self, errcode=-60001, errmsg='Unimplemented Message Method', method=None):
        super().__init__(errcode, errmsg + ': ' + method if method else errmsg)


class UnsupportedParameterTypesException(WeChatException):
    """不支持的参数类型"""

    def __init__(self, errcode=-60002, errmsg='Unsupported Parameter Types', param_type=None):
        super().__init__(errcode, errmsg + ': ' + param_type if param_type else errmsg)


class ValidationException(WeChatException):
    """校验错误"""

    def __init__(self, errcode=-60003, errmsg='Validation Exception'):
        super().__init__(errcode, errmsg)
