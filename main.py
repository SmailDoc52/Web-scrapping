from datetime import datetime

import requests
import bs4


URL = "https://habr.com/ru/all/"
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
    }

if __name__ == '__main__':
    response = requests.get(URL, headers=HEADERS)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    news_section = soup.select('article.tm-articles-list__item')
    
    for section in news_section:
        news_text = section.select_one(
            'div.article-formatted-body'
            )
        news_text = news_text.get_text().lower() if news_text else ''
        title_block = section.select_one('a.tm-title__link')
        if not title_block:
            continue
        news_title = title_block.text     
        
        for word in KEYWORDS:
            word_low = word.lower()
            if word_low in news_text or word_low in news_title.lower():
                news_time = (
                    section.select_one('time').get(
                        'title', section.select_one('time').get('datetime')
                    )
                )
                format_str = "%Y-%m-%d, %H:%M"
                time_object = datetime.strptime(news_time, format_str)
                news_time_format = time_object.strftime("%d.%m.%Y")
                news_link = (
                    'https://habr.com' 
                    + section.select_one('a.tm-title__link').get('href')
                )
                print(f"{news_time_format} - {news_title} - {news_link}")
                break
