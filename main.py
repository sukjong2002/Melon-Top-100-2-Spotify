import requests
from bs4 import BeautifulSoup
import re
import time

spotifyUrl = 'https://api.spotify.com/v1/search'
spotifyHeader = {'Authorization': 'INSERT_SPOTIFY_DEV_API_KEY_HERE_START_WITH_BEARER', 'Content-Type': 'application/json'}
#모바일 페이지 차트는 user-agent가 모바일로 되어 있어야 함
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36 Edg/99.0.1150.36'}

#멜론 모바일 페이지 차트 get링크
res = requests.get('https://m2.melon.com/cds/main/mobile4web/main_chartPaging.htm', headers=headers)
#print(res.content)
obj = BeautifulSoup(res.content, 'html.parser')


myDict = {}
items = obj.findAll('li', {'class':'list_item'})
for item in items:
    title = item.find('p', {'class': 'title'})
    #print(title)
    #응답에서 쓸모없는 스페이스가 많아서 모두 지워줘야함
    # ^: 줄 앞      \s: 스페이스       xx$: 끝          |: 양 옆의 regex를 동시에 확인
    title = re.sub('^\s+|\s+$', '', title.text)

    artist = item.find('span', {'class':'name'}).text

    print(title)
    myDict[title] = artist

# print(myDict)


