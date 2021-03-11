from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()