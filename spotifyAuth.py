import requests, base64

spotifyAuthUrl = 'https://accounts.spotify.com/api/token'

def str2base64(msg):
    msg_bytes = msg.encode('ascii')
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode('ascii')

def getHeader(spotifyCId, spotifyCSec):
    return {'Authorization': 'Basic '+str2base64(spotifyCId+':'+spotifyCSec), 'Content-Type': 'application/x-www-form-urlencoded'}

#See https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
def getSpotifyAuth(spotifyCId, spotifyCSec):
    spotifyAuthData = {'grant_type': 'client_credentials'}
    authData1 = requests.post(spotifyAuthUrl, headers=getHeader(spotifyCId, spotifyCSec), data=spotifyAuthData)
    # print(authData1.content)
    authData = authData1.json()
    return authData['access_token']

def getSpotifyUserAuth(spotifyCId, spotifyCSec, authCode):
    spotifyAuthData = {'grant_type': 'authorization_code', 'code': authCode, 'redirect_uri': 'http://127.0.0.1:5000/callback'}
    authData1 = requests.post(spotifyAuthUrl, headers=getHeader(spotifyCId, spotifyCSec), data=spotifyAuthData)
    # print(authData1.content)
    authData = authData1.json()
    return authData['access_token']
