import requests, json

def create(auth, chart, userName, PLNameOrCode):
    print(auth)
    #See https://developer.spotify.com/console/post-playlists/
    spotifyUrl = 'https://api.spotify.com/v1/users/'+userName+'/playlists'
    spotifyData = {'name': PLNameOrCode, "public": True}
    spotifyCreateRes = requests.post(spotifyUrl, data=json.dumps(spotifyData), headers={'Authorization': 'Bearer '+auth})
    # print(spotifyCreateRes.content)
    spotifyPlaylistId = spotifyCreateRes.json()['id']

    #See https://developer.spotify.com/console/post-playlist-tracks/
    spotifyAddUrl = 'https://api.spotify.com/v1/playlists/'+spotifyPlaylistId+'/tracks'
    spotifyAddData = {'uris': chart}
    spotifyAddRes = requests.post(spotifyAddUrl, data=json.dumps(spotifyAddData), headers={'Authorization': 'Bearer '+auth})
    # print(spotifyAddRes.content)
