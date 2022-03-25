from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException
from spotifyModPlaylist import create
from spotifyAuth import getSpotifyUserAuth


app = Flask(__name__)
app.debug = False
app.secret_key = 'development'

#Flask 저장소에 저장. TODO) 더 효율적인 variable pass 방법
def run(chartDict, cId, cSec, userName, PLNameOrCode):
    app.config['chart'] = chartDict
    app.config['cId'] = cId
    app.config['cSec'] = cSec
    app.config['userName'] = userName
    app.config['PLNOC'] = PLNameOrCode
    app.run()

def passAuthAndShutdown(auth):
    chart = app.config['chart']
    authToken = getSpotifyUserAuth(app.config['cId'], app.config['cSec'], auth)
    userName = app.config['userName']
    PLNameOrCode = app.config['PLNOC']
    #서버 close
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    create(authToken, chart, userName, PLNameOrCode)

    
@app.route('/callback', methods=['GET', 'POST'])
def index():
    code = request.args.get('code')
    print(code)
    passAuthAndShutdown(code)
    return code
