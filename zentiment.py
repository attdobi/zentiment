#import os
#base_dir=os.path.expanduser('~')
from __future__ import division
from flask import Flask, render_template, request, request, jsonify
import numpy as np
from zen_class import Zen

#initialize emoji class
Zen=Zen()

#Setup Authentication #########################################
from functools import wraps
from flask import request, Response

def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	return username == 'insight' and password == 'demo'

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated
############# End Authentication ############################

application = Flask(__name__)

####### Tall Labs Pages ######################

##### Make a homepage by setting one of the pages to index.html
#@ application.route("/")
#def index():
#	return render_template("index.html")

@application.route("/zen/force")
def force():
	return render_template("force.html")
@application.route("/zen/tree")
def tree():
	return render_template("tree.html")
	
#Functions for D3JS visualization
@application.route('/zen/_get_vis')
def _get_vis():
	word = request.args.get('word')
	#model = request.args.get('model')
	result=Zen.visual(word)
	return jsonify(result=result)
	
@application.route('/zen/_get_tree')
def _get_tree():
	word = request.args.get('word')
	#model = request.args.get('model')
	result=Zen.tree(word)
	return jsonify(result=result)
	
###### End Tall Labs ########################
if __name__ == "__main__":
	application.run(host='0.0.0.0')
