from django.shortcuts import render
from django.views.generic.detail import DetailView
from connect_spotify.models import Node

import requests

API_TRACKS = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term"

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def index(request):
    last_node = Node.objects.last()
    obj_node = last_node.get_token_message()
    context = {}

    response = requests.get(API_TRACKS, auth=BearerAuth(obj_node["token"]))
    if not response.status_code == 200:
        context = {"message": "request error", "token": obj_node["token"]}
    else:
        items = response.json()["items"]
        context = {
            "names": [i["name"] +" - "+ i["artists"][0]["name"] for i in items],
            "count": len(items),
            "message": "OK",
            "token": obj_node["token"]
        }
        print(context["names"])

    return render(request, 'show_spotify_songs/index.html', context)