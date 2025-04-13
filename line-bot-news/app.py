from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests, openai, os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 環境変数から読み込み
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 実行環境
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ダミーのOpenAIレスポンス
class DummyResponse:
    def __init__(self, content):
        self.choices = [{"message": {"content": content}}]

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 通常はここで OpenAI API を呼ぶ
    response = DummyResponse("これはダミーの応答です。")

    reply_text = response.choices[0]["message"]["content"].strip()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# Flask起動
if __name__ == "__main__":
    app.run()

app = Flask(__name__)

# Webhookエンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# ユーザーからのメッセージ受信時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text

    # 本来のOpenAI API呼び出し（コメントアウト）
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": user_message}],
    # )

    # ダミー応答
    class DummyResponse:
        def __init__(self, content):
            self.choices = [{"message": {"content": content}}]
    response = DummyResponse("これはダミーの返信です（ChatGPT API未使用）")

    # ダミー用にエラーが出ないよう変更
    reply_text = response.choices[0]["message"]["content"].strip()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# ローカルテスト用（任意）
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running."

if __name__ == "__main__":
    app.run(port=5000)
