# 💱 為替レート可視化アプリ

通貨ペアを選ぶと、過去30日間の為替推移グラフ、最新レート、CSV/PDFレポートが表示されるWebアプリです。

## 🔧 主な機能

- 通貨ペアの選択（USD, EUR, JPY, GBP）
- 過去の為替レート推移グラフ表示
- 最新レートと変動値の表示
- CSV / PDFレポートの出力
- 日本語PDFレポート対応
- 経済ニュース（関連API）表示← **準備中**

## 📸 スクリーンショット

![スクリーンショット_sample](https://github.com/user-attachments/assets/80dc6c6d-b30f-44d4-8212-1c039c5e2ccb)


## 🚀 公開URL
👉 [Streamlit Cloudで試す]https://pythonapp-fbodfu7dffgx52zzjyhs9m.streamlit.app/

## 💻 使用技術
- Python / Streamlit / matplotlib / pandas
- FPDF（PDF生成）
- Frankfurter API（為替データ）

## 📰 経済ニュース連携

選択した通貨ペア（例：USD→JPY）に関連する最新の英語ニュースを5件まで表示。  
NewsData.io APIを使用し、リアルタイムに情報を取得しています。
