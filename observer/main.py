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

from client.replies import *
from client.wechat import WeChatClient, register_msg, register_event
from exceptions import InvalidSignatureException
from client.request.menu import MenuRequest
from client.domain.menu import Menu, Button, MatchRule

app = Flask(__name__)

client = WeChatClient('wx6dbc04ce2e617787', '10907e76e8268395804ecd33de83da74', 'wesoft')


@app.route('/', methods=['GET'])
def index():
    return "index"


@app.route('/menu/<string:action>', methods=['GET'])
def menu(action):
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
