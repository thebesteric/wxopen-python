from flask import Flask, request
from wechat import WeChatThirdClient, register_msg, register_event
from exceptions import InvalidSignatureException

app = Flask(__name__)

client = WeChatThirdClient('wx20877d0c688e71d3', 'cb680bf45dc0a93a8d3e733360da1bba', 'token', 'sEncodingAESKey')


@app.route('/auth_page', methods=['GET'])
def create_auth_page():
    return client.router.create_component_login_page_by_url('/callback')


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    if client.check_signature(signature, timestamp, nonce):
        if request.method == 'GET':
            return request.args.get('echostr')
        elif request.method == 'POST':
            return client.process(request.data)
    raise InvalidSignatureException()


if __name__ == "__main__":
    app.run(port=8000, debug=False)
