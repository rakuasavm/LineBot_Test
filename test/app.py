from flask import Flask, request, abort
from flask.logging import create_logger

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi('C4QUATJVLl5vElH/4EWk2T9oPIlsdZQ7RtLKSGBa/LRqWMmofmuAM4+wS99BpM6UFQpxxoTrV6Hve26lwrSQs1M/xHFi5xIaSzv/RjHwAuQQQAdAhGn/55niOizTa0bugPk+ahoCIoVBXS2S5CsaCQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('95c71f834273bf27c874fdf811e5f37d')

@app.route("/")
def default():
    return "default page"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)