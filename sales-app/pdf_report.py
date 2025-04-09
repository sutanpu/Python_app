from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

plt.rcParams["font.family"] = "MS Gothic"  # グラフに日本語表示

# データ準備
df = pd.read_csv("sales_data.csv", parse_dates=["日付"])
df["月"] = df["日付"].dt.to_period("M")
grouped = df.groupby(["月", "商品名"])["売上"].sum().unstack().fillna(0)

# グラフ出力
plt.figure(figsize=(10, 6))
grouped.plot(kind="bar", stacked=True)
plt.title("月別売上（商品別）")
plt.ylabel("売上")
plt.tight_layout()
graph_path = "sales_graph.png"
plt.savefig(graph_path)
plt.close()

# PDF出力
pdf = FPDF()
pdf.add_page()

# ✅ 日本語フォント登録（相対パス）
pdf.add_font("Noto", "", "NotoSansJP-Regular.ttf", uni=True)
pdf.set_font("Noto", "", 14)

pdf.cell(0, 10, "売上レポート", ln=True)
pdf.set_font("Noto", "", 12)
pdf.cell(0, 10, f"作成日: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
pdf.ln(5)

# テーブル見出し
pdf.set_font("Noto", "", 10)
pdf.cell(30, 10, "月", border=1)
for col in grouped.columns:
    pdf.cell(30, 10, col, border=1)
pdf.ln()

# テーブル中身
for idx, row in grouped.iterrows():
    pdf.cell(30, 10, str(idx), border=1)
    for val in row:
        pdf.cell(30, 10, str(int(val)), border=1)
    pdf.ln()

# グラフ画像
pdf.ln(10)
pdf.image(graph_path, x=10, w=180)

# 保存
pdf.output("sales_report.pdf")

pdf.add_font("Noto", "", "NotoSansJP-Regular.ttf")  # ← これでOK！

print("✅ 日本語対応のPDFが完成しました！")
