from django.http import HttpResponse

def index(request):
    res = ("""<div><h2>paths: </h2>"""
          """<ul><li><a href="/admin">admin</a></li>"""
          """<li><a href="/spotify">spotify</a></li>"""
          """<li><a href="/app">app</a></li></ul></div>""")
    return HttpResponse(res)