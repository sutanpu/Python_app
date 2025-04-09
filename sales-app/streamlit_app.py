import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("📊 売上データ可視化アプリ")

uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=["csv", "xlsx"])

if uploaded_file is not None:
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[-1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(uploaded_file, encoding="utf-8-sig", parse_dates=["日付"])
        elif ext == ".xlsx":
            df = pd.read_excel(uploaded_file, parse_dates=["日付"])
        else:
            st.error("対応していないファイル形式です。")
            st.stop()
    except Exception as e:
        st.error(f"ファイルの読み込みエラー：{e}")
        st.stop()

    # ✅ ここからは再読み込み不要！そのまま df を使う
    st.success("✅ ファイルを読み込みました！")
    st.dataframe(df.head())

    df["月"] = df["日付"].dt.to_period("M")

    selected_products = st.multiselect("表示する商品を選んでください", df["商品名"].unique(), default=df["商品名"].unique())

    filtered_df = df[df["商品名"].isin(selected_products)]

    st.subheader("📈 月別売上グラフ（商品別）")
    grouped = filtered_df.groupby(["月", "商品名"])["売上"].sum().unstack().fillna(0)
    st.bar_chart(grouped)

    st.subheader("📋 月別売上集計データ")
    st.dataframe(grouped)

else:
    st.info("👈 左からCSVまたはExcelファイルをアップロードしてください。")
