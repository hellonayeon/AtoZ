import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',
                    headers=headers)  # headers=headers 브라우저에서 검색한 것 마냥 만들어주는 속성

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#old_content > table > tbody > tr')
for tr in trs:
    tag = tr.select_one('td.title > div > a')

    # 페이지에 '구분선' 이 있는 경우 값이 들어오지 않음
    if tag is not None:
        rank = tr.select_one('td.ac > img')['alt'] # ( td:nth-child(1) > img ) 도 가능
        title = tr.select_one('td.title > div > a').text
        star = tr.select_one('td.point').text

        doc = {
            'rank' : rank,
            'title' : title,
            'star' : star
        }

        db.movies.insert_one(doc)