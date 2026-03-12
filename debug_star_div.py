import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection': 'keep-alive',
    'Referer': 'https://movie.douban.com/'
}

url = 'https://movie.douban.com/top250?start=0&filter='

print('Fetching page...')
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

content = response.text
soup = BeautifulSoup(content, 'html.parser')

# 找到第一个电影项
movie_items = soup.find_all('div', class_='item')
if movie_items:
    first_movie = movie_items[0]
    print('First movie item:')
    print(first_movie)
    
    # 找到star_div
    star_div = first_movie.find('div', class_='star')
    if star_div:
        print('\nStar div:')
        print(star_div)
        
        # 找到所有span
        span_list = star_div.find_all('span')
        print(f'\nFound {len(span_list)} spans:')
        for i, span in enumerate(span_list):
            print(f'Span {i}: {span}')
            print(f'Text: {span.text.strip()}')
            print(f'Class: {span.get("class")}')
            print()