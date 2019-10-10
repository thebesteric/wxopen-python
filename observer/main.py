"""
程序主入口
@project: wxopen
@file: .py
@ide: PyCharm
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/9/24 21:28
@info: 
"""
from flask import Flask, request

from client.domain.menu import Menu, Button, MatchRule
from client.replies import *
from client.request import MenuRequest, UserRequest, TagRequest, AccountRequest, CustomerRequest
from client.wechat import WeChatClient, register_msg, register_event
from exceptions import InvalidSignatureException

app = Flask(__name__)

client = WeChatClient('wx6dbc04ce2e617787', '10907e76e8268395804ecd33de83da74', 'wesoft')


@app.route('/', methods=['GET'])
def index():
    return "index"


@app.route('/customer/<string:action>', methods=['GET'])
def customer(action):
    customer_request = CustomerRequest()
    if action == 'list':
        return customer_request.list_customers()
    return 'success'


@app.route('/account/<string:action>', methods=['GET'])
def account(action):
    account_request = AccountRequest()
    if action == 'create_qr_scene':  # 创建临时整型参数值的二维码
        return account_request.create_qr_scene(1234, 3600)
    elif action == 'create_qr_str_scene':  # 创建临时字符串参数值的二维码
        return account_request.create_qr_str_scene('test', 3600)
    elif action == 'create_limit_qr_scene':  # 创建永久整型参数值的二维码
        return account_request.create_limit_qr_scene(1234)
    elif action == 'create_limit_qr_str_scene':  # 创建永久字符串参数值的二维码
        return account_request.create_limit_qr_str_scene('test')
    elif action == 'short_url':  # 长连接转短链接
        return account_request.short_url('http://127.0.0.1:8000?id=1000&name=zhagnsan&age=18')

    return 'success'


@app.route('/menu/<string:action>', methods=['GET'])
def menu(action):
    """菜单测试案例"""
    menu_request = MenuRequest()
    if action == 'create':
        sub_btn_1_1 = Button(name='扫码带提示', type=Button.TYPE.SCANCODE_WAITMSG, key='SCANCODE_WAITMSG')
        sub_btn_1_2 = Button(name='扫码带事件', type=Button.TYPE.SCANCODE_PUSH, key='SCANCODE_PUSH')
        btn1 = Button(name='微信扫码', sub_button=[sub_btn_1_1, sub_btn_1_2])
        btn2 = Button(name='百度搜索', type=Button.TYPE.VIEW, url='https://www.baidu.com')
        btn3 = Button(name='拍照传图', type=Button.TYPE.PIC_WEIXIN, key='FROM_PIC_WEIXIN')
        menu = Menu(btn1, btn2, btn3)
        return menu_request.create(menu)
    elif action == 'create_conditional':
        btn1 = Button(name='百度搜索', type=Button.TYPE.VIEW, url='https://www.baidu.com')
        btn2 = Button(name='拍照传图', type=Button.TYPE.PIC_WEIXIN, key='FROM_PIC_WEIXIN')
        btn3 = Button(name='个性化', type=Button.TYPE.VIEW, url='https://cn.bing.com')
        matchrule = MatchRule(language='zh_CN')
        menu = Menu(btn1, btn2, btn3, matchrule=matchrule)
        return menu_request.create_conditional(menu)
    elif action == 'delete_conditional':
        menu_id = request.args.get('menu_id')
        return menu_request.delete_conditional(menu_id)
    elif action == 'try_match':
        user_id = request.args.get('user_id')
        return menu_request.try_match(user_id=user_id)
    elif action == 'info':
        return menu_request.info()
    elif action == 'get':
        return menu_request.get()
    elif action == 'delete':
        return menu_request.delete()

    return 'success'


@app.route('/tag/<string:action>', methods=['GET'])
def tag(action):
    """标签测试案例"""
    tag_request = TagRequest()
    if action == 'create':
        return tag_request.create('TEST TAG')
    elif action == 'delete':
        return tag_request.delete(100)
    elif action == 'get':
        return tag_request.get()
    elif action == 'update':
        return tag_request.update(100, 'TEST TAG UPDATE')
    elif action == 'users':
        return tag_request.users(100)
    elif action == 'batch_tagging':
        return tag_request.batch_tagging(100, 'omn8007rEC_xhRUSHvxyi7Y8pdlc', 'omn8001suYNRyOIRVt_6RmpfqfQs')
    elif action == 'batch_untagging':
        return tag_request.batch_untagging(100, 'omn8007rEC_xhRUSHvxyi7Y8pdlc', 'omn8001suYNRyOIRVt_6RmpfqfQs')
    elif action == 'user_tags':
        return tag_request.user_tags('omn8007rEC_xhRUSHvxyi7Y8pdlc')
    return 'success'


@app.route('/user/<string:action>', methods=['GET'])
def user(action):
    user_request = UserRequest()
    if action == 'info':
        return user_request.info('omn8007rEC_xhRUSHvxyi7Y8pdlc')
    elif action == 'infos':
        return user_request.infos('omn8007rEC_xhRUSHvxyi7Y8pdlc', 'omn8001suYNRyOIRVt_6RmpfqfQs')
    elif action == 'subscribe_list':
        return user_request.subscribe_list()
    elif action == 'black_list':
        return user_request.black_list()
    elif action == 'batch_black_list':
        return user_request.batch_black_list('omn8007rEC_xhRUSHvxyi7Y8pdlc')
    elif action == 'batch_un_black_list':
        return user_request.batch_un_black_list('omn8007rEC_xhRUSHvxyi7Y8pdlc')
    return 'success'


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    if client.check_signature(signature, timestamp, nonce):
        if request.method == 'GET':
            return request.args.get('echostr')
        elif request.method == 'POST':
            return client.process(request.data)
    raise InvalidSignatureException()


@register_msg(msg_type=['text', 'image'])
def process_text(message):
    print('text image')
    print(message)
    return SuccessReply().render()


@register_msg(msg_type='voice')
def process_voice(message):
    print('voice')
    print(message)
    return TextReply(message, 'got voice').render()


@register_msg(msg_type=['video', 'shortvideo'])
def process_video(message):
    print('video shortvideo')
    print(message)
    return TextReply(message, 'got shortvideo video').render()


@register_event(event_type=['subscribe', 'unsubscribe'])
def process_video(message):
    print('subscribe unsubscribe')
    print(message)
    return TextReply(message, 'got subscribe').render()


@register_event(event_type=['click', 'view'])
def process_video(message):
    print('click view')
    print(message)
    return TextReply(message, 'got click').render()


if __name__ == "__main__":
    app.run(port=8000, debug=False)
