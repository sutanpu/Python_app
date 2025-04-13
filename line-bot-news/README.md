
最新ニュースをLINEボットに送ると、ChatGPT風に自動で日本語要約してくれるPythonアプリです。

※現在はAPI課金なしで動作確認をするため、ChatGPTの応答はダミー対応にしています。

---

## 🧠 主な機能

- ✅ LINEボットに送った文章をAIっぽく要約（ダミー）
- ✅ FlaskでWebhookサーバーを構築
- ✅ LINE Messaging APIでBot通知
- ✅ ngrokでローカルサーバーを外部公開
- ✅ `.env`でセキュアにAPIキー管理

---

## 🧰 使用技術

| 項目 | 内容 |
|------|------|
| 言語 | Python |
| ライブラリ | Flask, line-bot-sdk, dotenv |
| 外部連携 | LINE Messaging API |
| 開発補助 | ngrok, VSCode |

---

## 📦 フォルダ構成

```bash
line-bot-news/
├── app.py                 # Flask本体（LINE + OpenAI応答）
├── .env                  # 環境変数（APIキーなど）
├── requirements.txt       # ライブラリ定義
└── README.md              # ← このファイル
