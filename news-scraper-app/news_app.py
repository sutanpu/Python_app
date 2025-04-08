import streamlit as st
import pandas as pd

# CSV読み込み
df = pd.read_csv('news_all_カテゴリ付き_20250408.csv')

# タイトル
st.title("📄 Yahooニュースビューア（カテゴリ別）")

# カテゴリ選択
category = st.selectbox("カテゴリを選んでください", df["カテゴリ"].unique())

# 選択したカテゴリの記事だけ表示
filtered_df = df[df["カテゴリ"] == category]

# 見出し一覧
selected_title = st.selectbox("記事を選んでください", filtered_df["タイトル"])

# 選ばれた記事の本文表示
article = filtered_df[filtered_df["タイトル"] == selected_title].iloc[0]

st.subheader("📰 本文")
st.write(article["本文"])

st.markdown(f"[🔗 記事URLを開く]({article['URL']})")
