from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('EO+pnRbs1XN+p0yVa8YEeHLCdWy8mSDEdnftyr2O57uAOIFAMhuoJJX7xDs2ovgJRtMmJrzj5QETYdZgGH5KfduqwKR2dMVdLGyaUtR3LYFwsn3L2Jbe+dc2sUlJ8foI02Bk/0nig2sFk/QbOLbGGQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('39c4f58819ba669fcd3b7e385ce98579')


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
    msg = event.message.text
    r = '很抱歉 我看不太懂你說什麼:<'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002742'
        )

    if msg in ['嗨', 'HI', 'hi', 'Hi', '哈囉', '你好']:
        r = '安妞~ 我是聊天機器人'
    elif '愛你' in msg:
        r = 'love you <3'
    elif '想你' in msg:
        r = '>///<'
    elif '你是誰' in msg:
        r = '我是機器人!'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()