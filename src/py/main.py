#encoding=utf-8
from bottle import route, run

@route("/")
def index():
	return "<h1>Hello world</h1><p> I'm at index</p><a href='/sample'>移動する</a>"

@route("/sample")
def sample():
	return "<h1>Hello world</h1><p> I'm at sample</p><a href='/'>移動する</a>"

run(host='localhost', port=8080, debug=True, reloader=True)