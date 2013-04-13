from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required)
import function

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.template_filter('get_xml')
def get_xml(ficxml):
	ofi = open(ficxml, 'r')
	ficxml = ofi.read()
	return ficxml

@app.route('/test')
def test():
	packs,shortname, i, pack = function.get_packages()
	grps = function.get_group()
	return render_template('test.html', grps=grps, packs=packs, shortname=shortname, i=i, pack=pack)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


