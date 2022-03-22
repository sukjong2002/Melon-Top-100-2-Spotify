import requests
from bs4 import BeautifulSoup
import re
import time
import base64

#https://developer.spotify.com/dashboard
spotifyCId = 'INSERT_YOUR_SPOTIFY_API_CLIENT_ID'
spotifyCSec = 'INSERT_YOUR_SPOTIFY_API_CLIENT_SECRET_KEY'

def str2base64(msg):
    msg_bytes = msg.encode('ascii')
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode('ascii')

#See https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
def getSpotifyAuth():
    spotifyAuthUrl = 'https://accounts.spotify.com/api/token'
    spotifyAuthHeader = {'Authorization': 'Basic '+str2base64(spotifyCId+':'+spotifyCSec), 'Content-Type': 'application/x-www-form-urlencoded'}
    spotifyAuthData = {'grant_type': 'client_credentials'}
    authData = requests.post(spotifyAuthUrl, headers=spotifyAuthHeader, data=spotifyAuthData).json()
    return authData['access_token']

spotifyUrl = 'https://api.spotify.com/v1/search'
spotifyHeader = {'Authorization': 'Bearer '+getSpotifyAuth(), 'Content-Type': 'application/json'}
#모바일 페이지 차트는 user-agent가 모바일로 되어 있어야 함
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36 Edg/99.0.1150.36'}

#멜론 모바일 페이지 차트 get링크
res = requests.get('https://m2.melon.com/cds/main/mobile4web/main_chartPaging.htm', headers=headers, params={'startIndex': 1, 'pageSize': 100, 'rowsCnt': 100})
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
    #print(title)
    myDict[title] = artist

i = 1
for item in myDict:
    print(str(i)+' '+item+' '+myDict[item])
    i = i+1
    spotifyRes = requests.get(spotifyUrl, params={'q':myDict[item]+' '+item, 'type':'track', 'market':'kr', 'limit':2}, headers=spotifyHeader)
    # print(spotifyRes.content)
    resData = spotifyRes.json()
    #가수+노래제목이 모두 맞는 검색결과가 있는 경우에만 실행
    if len(resData['tracks']['items']) > 0:
        trackData = resData['tracks']['items'][0]
    else:
        #가수+제목이 없는 경우 제목으로만 검색
        spotifyRes = requests.get(spotifyUrl, params={'q':item, 'type':'track', 'market':'kr', 'limit':2}, headers=spotifyHeader)
        resData = spotifyRes.json()
        if len(resData['tracks']['items']) > 0:
            trackData = resData['tracks']['items'][0]
            #곡명으로만 찾을 경우 다른 외국 가수의 노래가 등록되는 경우가 많아서 한국 노래인 경우에만 넣게 코딩. KR, KS = 한국 ISRC국가코드
            if "KR" not in trackData['external_ids']['isrc'] and "KS" not in trackData['external_ids']['isrc']:
                print(item+" Not Match!")
                continue
        else:
            print(item+" Not Found!")
            continue
    print(trackData['external_urls']['spotify'])
    time.sleep(0.5)
# print(myDict)


