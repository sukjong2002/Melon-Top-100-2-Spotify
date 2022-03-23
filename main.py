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
    authData1 = requests.post(spotifyAuthUrl, headers=spotifyAuthHeader, data=spotifyAuthData)
    print(authData1.content)
    authData = authData1.json()
    return authData['access_token']

def getMelonChart():
    #멜론 모바일 앱 일간 차트 json
    #JSON안에 장르별 코드 들어가 있음. ex)GN000 - 장르종합
    #daily - 일간차트, weekly - 주간차트, monthly - 월간차트
    res = requests.get('https://m2.melon.com/m5/chart/daily/songChartList.json', params={'v': 5.0, 'gnrCode': 'GN0000', 'pageSize': 100, 'startIndex': 1}, headers=headers)
    obj = res.json()
    chartDict = {}

    for item in obj['response']['CHARTLIST']:
        title = item['SONGNAME']
        artist = item['ARTISTLIST'][0]['ARTISTNAME']
        #print(title)
        chartDict[title] = artist
    return chartDict

spotifyUrl = 'https://api.spotify.com/v1/search'
spotifyHeader = {'Authorization': 'Bearer '+getSpotifyAuth(), 'Content-Type': 'application/json'}
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36 Edg/99.0.1150.36'}

i = 1
myDict = getMelonChart()
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


