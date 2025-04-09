import pandas as pd
from datetime import datetime
import os

# データ読み込み
df = pd.read_csv('sales_data.csv', parse_dates=['日付'])

# 月列を追加（例：2025-04）
df['月'] = df['日付'].dt.to_period('M')

# 保存用フォルダ・ファイル名
os.makedirs("reports", exist_ok=True)
today = datetime.now().strftime('%Y%m%d')
filename = f'reports/sales_report_by_month_{today}.xlsx'

# ExcelWriterで月ごとにシート出力
with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    for month, group in df.groupby('月'):
        month_str = str(month)
        group.to_excel(writer, index=False, sheet_name=month_str)

print(f"✅ 月別シート付きのExcelを作成しました：{filename}")
