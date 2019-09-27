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
    """Invalid Signature Exception"""

    def __init__(self, errcode=-40001, errmsg='Invalid Signature'):
        super().__init__(errcode, errmsg)


class MissingParametersException(WeChatException):
    """Missing Parameters Exception"""

    def __init__(self, errcode=-60000, errmsg='Missing Parameters'):
        super().__init__(errcode, errmsg)


class UnimplementedMsgMethodException(WeChatException):
    """Unimplemented Message Method  Exception"""

    def __init__(self, errcode=-60001, errmsg='Unimplemented Message Method', method=None):
        super().__init__(errcode, errmsg + ': ' + method if method else errmsg)


class UnsupportedParameterTypesException(WeChatException):
    """Unsupported Parameter Types Exception"""

    def __init__(self, errcode=-60002, errmsg='Unsupported Parameter Types', param_type=None):
        super().__init__(errcode, errmsg + ': ' + param_type if param_type else errmsg)
