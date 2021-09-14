import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',
                    headers=headers)  # headers=headers 브라우저에서 검색한 것 마냥 만들어주는 속성

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for tr in trs:
    rank = tr.select_one('td.number').text.split('\n')[0]
    title = tr.select_one('td.info > a.title.ellipsis').text.split('\n')[8].lstrip()
    artist = tr.select_one('td.info > a.artist.ellipsis').text

    print(rank, title, artist)