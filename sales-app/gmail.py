import yagmail

# Gmailログイン（アプリパスワード使用）
yag = yagmail.SMTP(user="sutannpu11@gmail.com", password="cojnxmkwzkbqixqr",local_hostname='localhost')

# メール送信内容
to = "scientificmenscare@gmail.com"
subject = "Sales Report"
body = "Please find the attached sales report."
filename = "reports/sales_report_by_month_20250409.xlsx"

# メール送信
yag.send(to=to, subject=subject, contents=body, attachments=filename)

print("📩 メールを送信しました！")
