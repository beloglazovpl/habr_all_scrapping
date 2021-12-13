import requests
import bs4
import re


# ключевые слова
KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.1931241552.1631448402; hl=ru; fl=ru; _ym_uid=1631448402277179136; _ym_d=1631448402; _gid=GA1.2.2139750520.1639136620; _ym_isad=1; habr_web_home=ARTICLES_LIST_ALL; visited_articles=444338:301436:531472:272711:50147:482464:483400:260129:447322:323202',
    'Host': 'habr.com',
    'If-None-Match': 'W/"363fe-jqViPkCpMf3eaYgcy9CJe1kuzQY"',
    'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
    'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'macOS',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

dic = {}

response = requests.get(url='https://habr.com/ru/all/', headers=headers)
response.raise_for_status()
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    previews = article.find_all('div', class_='tm-article-snippet')
    title = article.find('a', 'tm-article-snippet__title-link')
    title_name = title.find('span').text
    href = title['href']
    url = 'https://habr.com' + href
    date_time = article.find('span', class_='tm-article-snippet__datetime-published')
    date = date_time.find('time')['title'][:10]

    for preview in previews:
        preview_lower = preview.text.lower()
        preview_split = re.split('[^a-zа-яё]+', preview_lower, flags=re.IGNORECASE)
        preview_set = set(preview_split)
        if KEYWORDS & preview_set:
            dic[url] = [f'{date} - {title_name} - {url}']

    text2 = requests.get(url=url).text
    soup2 = bs4.BeautifulSoup(text2, features='html.parser')
    page = soup2.find('div', id='post-content-body').text
    page_lower = page.lower()
    page_split = re.split('[^a-zа-яё]+', page_lower, flags=re.IGNORECASE)
    page_set = set(page_split)
    if KEYWORDS & page_set:
        dic[url] = [f'{date} - {title_name} - {url}']
for key, value in dic.items():
    print(value)
