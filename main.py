#必用なものをインポート
from flask import Flask, request, abort
import os
import scrape as sc

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#LINEでのイベントを取得
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["y5bUVlwAsWLFdTDRMc3l/+PR92GUZymNnzFLWZg5oj6ESdpaK00Za2zFO+eqcc2uO+Y4kKUvoGuIVV8zAmUad9wmrK8Y+y8dNEK76wnIQEWmzkfOktPHve93GCI9+SeCpsPLleLlRjij9QbGK3UyrwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["0d1a4eba93553b37d583273475d449ad"]

line_bot_api = LineBotApi("y5bUVlwAsWLFdTDRMc3l/+PR92GUZymNnzFLWZg5oj6ESdpaK00Za2zFO+eqcc2uO+Y4kKUvoGuIVV8zAmUad9wmrK8Y+y8dNEK76wnIQEWmzkfOktPHve93GCI9+SeCpsPLleLlRjij9QbGK3UyrwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("0d1a4eba93553b37d583273475d449ad")

#アプリケーション本体をopenすると実行される
@app.route("/")
def hello_world():
    return "hello world!"

#/callback　のリンクにアクセスしたときの処理。webhook用。
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

#メッセージ受信時のイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    #line_bot_apiのreply_messageメソッドでevent.message.text(ユーザのメッセージ)を返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sc.getWeather))
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
