import requests
from bs4 import BeautifulSoup
import re
import time
import base64
import webbrowser
from datetime import date, datetime
from spotifyUserCon import run
from spotifyAuth import getSpotifyAuth

#https://developer.spotify.com/dashboard
#Dashboard 설정에서 'Redirect URI'에 http://127.0.0.1:5000/callback 추가해야 실행 가능
spotifyCId = 'INSERT_YOUR_SPOTIFY_API_CLIENT_ID'
spotifyCSec = 'INSERT_YOUR_SPOTIFY_API_CLIENT_SECRET_KEY'

#Check username in https://www.spotify.com/us/account/overview/
spotifyUserName = 'INSERT_YOUR_SPOTIFY_USER_NAME'

chartTerm = 'daily'
spotifyPlaylistName = 'Melon Top 100 Chart ' + datetime.today().strftime('%m-%d')

def getMelonChart(chartType):
    #멜론 모바일 앱 일간 차트 json
    #JSON안에 장르별 코드 들어가 있음. ex)GN000 - 장르종합
    #daily - 일간차트, weekly - 주간차트, monthly - 월간차트
    res = requests.get('https://m2.melon.com/m5/chart/'+chartType+'/songChartList.json', params={'v': 5.0, 'gnrCode': 'GN0000', 'pageSize': 100, 'startIndex': 1}, headers=headers)
    obj = res.json()
    chartDict = {}

    for item in obj['response']['CHARTLIST']:
        title = item['SONGNAME']
        artist = item['ARTISTLIST'][0]['ARTISTNAME']
        #print(title)
        chartDict[title] = artist
    return chartDict


spotifyUrl = 'https://api.spotify.com/v1/search'
spotifyHeader = {'Authorization': 'Bearer '+getSpotifyAuth(spotifyCId, spotifyCSec), 'Content-Type': 'application/json'}
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36 Edg/99.0.1150.36'}

i = 1
myDict = getMelonChart(chartTerm)

#spotify 음악 코드(uri) 저장용
uriDict = []
#마지막에 수동 추가를 위한 실패 목록 저장용
failDict = []
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
                failDict.append(str(i)+' '+item+' '+myDict[item])
                continue
        else:
            print(item+" Not Found!")
            failDict.append(str(i)+' '+item+' '+myDict[item])
            continue
    print(trackData['external_urls']['spotify'])
    uriDict.append(trackData['uri'])
    time.sleep(0.1)
# print(myDict)

#권한 요청: playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private
webbrowser.open('https://accounts.spotify.com/authorize?response_type=code&client_id='+spotifyCId+'&scope=playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private&redirect_uri=http://127.0.0.1:5000/callback')
run(uriDict, spotifyCId, spotifyCSec, spotifyUserName, spotifyPlaylistName)
print('Failed to insert: '+str(failDict))
