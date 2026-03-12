import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://movie.douban.com/'
}

url = 'https://movie.douban.com/top250'

print('Fetching page...')
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
response.encoding = response.apparent_encoding

print(f'Status code: {response.status_code}')
print(f'Page length: {len(response.text)}')
print('\nFirst 1000 characters:')
print(response.text[:1000])

# 检查是否有电影项目
soup = BeautifulSoup(response.text, 'html.parser')
movie_items = soup.find_all('div', class_='item')
print(f'\nFound {len(movie_items)} movie items')

# 检查是否有其他可能的电影项目容器
if not movie_items:
    print('\nChecking for other possible containers:')
    # 检查是否有列表容器
    list_container = soup.find('ol', class_='grid_view')
    if list_container:
        print('Found grid_view container')
        items = list_container.find_all('li')
        print(f'Found {len(items)} items in grid_view')
    else:
        print('No grid_view container found')

    # 打印页面的主要结构
    print('\nPage structure:')
    for child in soup.body.children:
        if child.name:
            print(f'- {child.name}')
            for grandchild in child.children:
                if grandchild.name:
                    print(f'  - {grandchild.name}')
                    # 只打印两层，避免输出过多
                    break