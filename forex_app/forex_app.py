import streamlit as st 
import pandas as pd
import requests
from datetime import date, timedelta
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from io import BytesIO
import os


# ---------------------
# 📄 PDF生成関数
# ---------------------
def generate_pdf(df, title, graph_path):
    pdf = FPDF()
    pdf.add_page()

    # ✅ 日本語フォントを追加
    font_path = os.path.join(os.path.dirname(__file__), "NotoSansJP-Regular.ttf")
    pdf.add_font("Noto", "", font_path, uni=True)
    pdf.set_font("Noto", "", 14)
    pdf.cell(0, 10, "為替レートレポート", ln=True)

    pdf.set_font("Noto", "", 12)
    pdf.cell(0, 10, title, ln=True)

    pdf.image(graph_path, x=10, w=180)

    pdf.set_font("Noto", "", 10)
    pdf.ln(5)
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        pdf.cell(60, 10, str(row["日付"].date()))
        pdf.cell(40, 10, f"{row['為替レート']:.4f}")
        pdf.ln()

    return pdf.output(dest='S').encode('latin1')


# ---------------------
# 🌐 アプリ本体
# ---------------------
st.set_page_config(page_title="為替レート可視化アプリ", page_icon="💱")
st.title("💱 為替レート可視化アプリ（Frankfurter API版）")

# 通貨名の日本語辞書
currency_dict = {
    "USD": "アメリカドル",
    "EUR": "ユーロ",
    "JPY": "日本円",
    "GBP": "イギリスポンド"
}

# 通貨選択
base = st.selectbox("基準通貨（FROM）", list(currency_dict.keys()))
available_targets = [c for c in currency_dict.keys() if c != base]
target = st.selectbox("対象通貨（TO）", available_targets)

# 日付範囲選択
today = date.today()
default_start = today - timedelta(days=30)
start_date, end_date = st.date_input("表示する期間", [default_start, today])

# API呼び出し
url = f"https://api.frankfurter.app/{start_date}..{end_date}"
params = {"from": base, "to": target}
response = requests.get(url, params=params)
data = response.json()

if "rates" in data:
    rates = data["rates"]
    df = pd.DataFrame({
        "日付": pd.to_datetime(list(rates.keys())),
        "為替レート": [rate[target] for rate in rates.values()]
    }).sort_values("日付")

    # 日本語ラベル
    base_name = currency_dict.get(base, base)
    target_name = currency_dict.get(target, target)
    title = f"{base_name}（{base}） → {target_name}（{target}）の為替レート"

    # グラフ表示
    st.subheader(title)
    st.line_chart(df.set_index("日付"))

    # 最新レート
    latest = df.iloc[-1]
    delta = latest["為替レート"] - df.iloc[-2]["為替レート"]
    st.metric(label="📌 最新レート", value=f"{latest['為替レート']:.4f}", delta=f"{delta:.4f}")

    # 表示
    st.dataframe(df)

    # CSV出力
    st.download_button(
        label="📥 CSVでダウンロード",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{base}_{target}_rate_{start_date}_to_{end_date}.csv",
        mime="text/csv"
    )
    # グラフ保存 → PDF生成
    jp_font_path = os.path.join(os.path.dirname(__file__), "NotoSansJP-Regular.ttf")
    jp_font = fm.FontProperties(fname=jp_font_path)
    plt.rcParams["font.family"] = jp_font.get_name()

    fig, ax = plt.subplots()
    ax.plot(df["日付"], df["為替レート"])
    ax.set_title(title)
    ax.set_ylabel("為替レート")
    ax.set_xlabel("日付")
    fig.tight_layout()


    graph_path = "temp_graph.png"
    fig.savefig(graph_path)
    plt.close(fig)

    pdf_bytes = generate_pdf(df, title, graph_path)
    st.download_button(
        label="📄 PDFレポートをダウンロード",
        data=pdf_bytes,
        file_name=f"{base}_{target}_report_{start_date}_to_{end_date}.pdf",
        mime="application/pdf"
    )
    st.subheader("📰 関連ニュース")
    st.write("🔑 Secrets: ", st.secrets)  # ← 一時的なデバッグ用

    news_api_key = st.secrets["NEWS_API_KEY"]
    query = f"{base} {target} forex"
    news_url = f"https://newsdata.io/api/1/news?apikey={news_api_key}&q={query}&language=ja"


    try:
        news_res = requests.get(news_url).json()

        # 👇 レスポンス全体を出力（デバッグ用）
        st.write("🪵 APIレスポンス：", news_res)

        articles = news_res.get("results", [])

        if isinstance(articles, list) and articles:
            for article in articles[:5]:
                st.markdown(f"### [{article['title']}]({article['link']})")
                st.caption(article.get("pubDate", ""))
                st.write(article.get("description", ""))
                st.markdown("---")
        else:
            st.info("ニュースが見つかりませんでした。")
    except Exception as e:
        st.error(f"ニュース取得中にエラーが発生しました: {e}")


else:
    st.error("為替データの取得に失敗しました。APIエラーか、日付範囲が正しくない可能性があります。")