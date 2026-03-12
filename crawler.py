import requests
from bs4 import BeautifulSoup
import json
import time
import random

class DoubanMovieCrawler:
    def __init__(self):
        self.base_url = 'https://movie.douban.com/top250'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Connection': 'keep-alive',
            'Referer': 'https://movie.douban.com/'
        }
        self.movies = []
    
    def crawl(self):
        for page in range(10):
            start = page * 25
            url = f'{self.base_url}?start={start}&filter='
            print(f'Crawling page {page + 1}...')
            
            try:
                # 添加随机延迟，模拟人类行为
                time.sleep(random.uniform(1, 3))
                
                # 让requests自动处理压缩
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # 使用response.text，它会自动处理编码
                content = response.text
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # 检查是否有电影项目
                movie_items = soup.find_all('div', class_='item')
                
                if not movie_items:
                    # 尝试查找其他可能的容器
                    list_container = soup.find('ol', class_='grid_view')
                    if list_container:
                        movie_items = list_container.find_all('li')
                
                if not movie_items:
                    print(f'No movie items found on page {page + 1}')
                    # 打印页面的前500个字符，以便调试
                    print(f'Page content preview: {content[:500]}...')
                    continue
                
                print(f'Found {len(movie_items)} movie items on page {page + 1}')
                
                for item in movie_items:
                    movie = self.parse_movie(item)
                    if movie:
                        self.movies.append(movie)
                
            except Exception as e:
                print(f'Error crawling page {page + 1}: {e}')
                time.sleep(5)
    
    def parse_movie(self, item):
        try:
            # 检查item是否是li元素，如果是，找到内部的div.item
            if item.name == 'li':
                item = item.find('div', class_='item')
                if not item:
                    return None
            
            # 排名
            rank = item.find('em').text.strip() if item.find('em') else ''
            
            # 标题
            title = item.find('span', class_='title').text.strip() if item.find('span', class_='title') else ''
            
            # 评分
            rating = ''
            votes = ''
            
            # 找到评分和评价人数的容器
            bd_div = item.find('div', class_='bd')
            if bd_div:
                # 提取评分
                rating_span = bd_div.find('span', class_='rating_num')
                if rating_span:
                    rating = rating_span.text.strip()
                
                # 提取评价人数
                for span in bd_div.find_all('span'):
                    text = span.text.strip()
                    if '人评价' in text:
                        votes = ''.join(filter(str.isdigit, text))
                        break
            
            # 上映年份、导演、主演和类型
            bd_div = item.find('div', class_='bd')
            year = ''
            director_actors = ''
            genre = ''
            if bd_div:
                info_p = bd_div.find('p', class_='')
                if info_p:
                    info = info_p.text.strip()
                    info_lines = [line.strip() for line in info.split('\n') if line.strip()]
                    if info_lines:
                        # 导演和主演
                        director_actors = info_lines[0]
                        # 提取年份
                        if len(info_lines) > 1:
                            # 第二行通常包含年份、国家、类型
                            second_line = info_lines[1]
                            # 提取年份
                            year_part = second_line.split('/')[0].strip()
                            year = ''.join(filter(str.isdigit, year_part))
                            # 提取类型
                            if len(second_line.split('/')) > 2:
                                genre = second_line.split('/')[-1].strip()
            
            # 电影链接
            link = item.find('a')['href'] if item.find('a') else ''
            
            # 电影海报
            poster = item.find('img')['src'] if item.find('img') else ''
            
            # 只有当标题和评分都存在时才返回电影信息
            if title and rating:
                return {
                    'rank': rank,
                    'title': title,
                    'rating': rating,
                    'votes': votes,
                    'year': year,
                    'director_actors': director_actors,
                    'genre': genre,
                    'link': link,
                    'poster': poster
                }
            return None
        except Exception as e:
            print(f'Error parsing movie: {e}')
            return None
    
    def save_to_json(self, filename='movies.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
        print(f'Saved {len(self.movies)} movies to {filename}')
    
    def run(self):
        print('Starting to crawl Douban Top 250 movies...')
        self.crawl()
        self.save_to_json()
        print('Crawling completed!')

if __name__ == '__main__':
    crawler = DoubanMovieCrawler()
    crawler.run()