from django.http import response, HttpResponse
from django.shortcuts import redirect, render
import requests, urllib 

from django.conf import settings

CLIENT_ID = settings.CLIENT_ID
REDIRECT_URI = settings.REDIRECT_URI
CLIENT_SECRET = settings.CLIENT_SECRET

from .models import Node
from django.utils import timezone

def index(request):
    return render(request, 'connect_spotify/index.html', context=request.GET)

def login(request):
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-read-private user-read-email user-read-recently-played user-library-read user-top-read'
    }
    url = "{}{}".format("https://accounts.spotify.com/authorize?", urllib.parse.urlencode(payload))
    return redirect(url)

def callback(request):
    url = 'https://accounts.spotify.com/api/token',
    body_params = {
        'code': request.GET["code"],
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    res = requests.post(url[0], data= body_params ,auth=(CLIENT_ID, CLIENT_SECRET))
    if res.status_code == 200:
        body = res.json()
        access_token = body["access_token"]
        refresh_token = body["refresh_token"]

        # pass like a db
        
        q = Node(token=access_token, refresh_token=refresh_token, message="OK", pub_date=timezone.now())
        q.save()
        if q.id != None:
            return redirect("/app")
        # pass token to the browser to make request from there

        return redirect("/spotify?{}".format(urllib.parse.urlencode({
            'access_token': access_token,
            'refresh_token': refresh_token
        })))
    
    else:
        return redirect("/spotify?{}".format(urllib.parse.urlencode({'error': 'invalid_token'})))


