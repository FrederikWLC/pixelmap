from app.funcs import *
from flask import request

def redirectIfHeroku():
	if request.headers['Host'] == 'pixelmap.herokuapp.com':
		pass
		#return abort(301)
