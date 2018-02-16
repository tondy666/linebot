import os
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

line_bot_api = LineBotApi('e8sk0QIVONRI8yrqyl3b0rAAbH2BkYcnCV4NtcMYx5zwGQdvLrl8g/zcWbkuQcHe5oQqeVx5c8VX9kSJusbmGr42JcupsKYdwyTCFPll3Xw8DDgZ/DSEmIal/M+2Z3HzWAzR8zlRoKpyDWgmVk5/CwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('320dfde923fb6608b92c29903cb023a7')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
