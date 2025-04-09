import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 1. CSV読み込み
df = pd.read_csv('sales_data.csv', parse_dates=['日付'])

# 2. 商品ごとの日別売上を集計
grouped = df.groupby(['日付', '商品名'])['売上'].sum().unstack().fillna(0)

# 3. グラフ作成
plt.figure(figsize=(10, 6))
grouped.plot(kind='bar', stacked=True)
plt.title('日別売上（商品別）')
plt.xlabel('日付')
plt.ylabel('売上')
plt.xticks(rotation=45)
plt.tight_layout()

# グラフ保存
report_folder = "reports"
os.makedirs(report_folder, exist_ok=True)
today = datetime.now().strftime('%Y%m%d')
graph_path = f"{report_folder}/sales_graph_{today}.png"
plt.savefig(graph_path)
plt.close()

# 4. Excelファイルとして保存
excel_path = f"{report_folder}/sales_report_{today}.xlsx"
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='元データ')
    grouped.to_excel(writer, sheet_name='日別集計')

print(f"✅ レポートを作成しました: {excel_path}")
print(f"🖼 グラフ画像も保存しました: {graph_path}")
