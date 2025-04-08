import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

headers = {'User-Agent': 'Mozilla/5.0'}

# カテゴリとURLの辞書
categories = {
    '国内': 'https://news.yahoo.co.jp/categories/domestic',
    '国際': 'https://news.yahoo.co.jp/categories/world',
    '経済': 'https://news.yahoo.co.jp/categories/business',
    'エンタメ': 'https://news.yahoo.co.jp/categories/entertainment'
}

news_all = []

for category_name, category_url in categories.items():
    print(f'--- {category_name} ---')

    response = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 各カテゴリの記事リンク（pickupでない記事一覧）
    links = soup.select('a[href^="https://news.yahoo.co.jp/articles/"]')

    # 重複削除
    seen = set()
    for a in links:
        article_url = a['href']
        if article_url in seen:
            continue
        seen.add(article_url)

        title = a.get_text(strip=True)

        # 本文取得
        article_response = requests.get(article_url, headers=headers)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        article_body = article_soup.select_one('div[class*="article_body"]')
        content = article_body.get_text(strip=True) if article_body else '本文取得失敗'

        news_all.append({
            'カテゴリ': category_name,
            'タイトル': title,
            'URL': article_url,
            '本文': content
        })

        time.sleep(1)

# DataFrame化＆保存
today = datetime.now().strftime('%Y%m%d')
df = pd.DataFrame(news_all)
df.to_csv(f'news_all_カテゴリ付き_{today}.csv', index=False, encoding='utf-8-sig')

print(f"カテゴリ別ニュースをまとめて保存しました → news_all_カテゴリ付き_{today}.csv")
