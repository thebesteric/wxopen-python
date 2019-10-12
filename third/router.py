"""
微信第三方平台路由集合
@project: wxopen
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/12 12:08
@info: 
"""
import wxrequest


class WeChatThirdPlatformRouter(wxrequest.WeChatThirdRequest):

    def __init__(self, component_app_id, component_app_secret, component_access_token):
        super().__init__()
        self.component_app_id = component_app_id
        self.component_app_secret = component_app_secret
        self.component_access_token = component_access_token
