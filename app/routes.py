from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify, session, escape
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required)
import function, sys, os

UPLOAD_FOLDER = '/root/flaskapp/app/packages'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'


@app.route('/')
def accueil():
	if 'username' in session:
		return 'Logged in as %s' % escape(session['username'])
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash("Connecte en tant que : " + request.form['username'])
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/test')
def test():
	packs,shortname, i, pack = function.get_packages()
	grps = function.get_group()
	return render_template('test.html', grps=grps, packs=packs, shortname=shortname, i=i, pack=pack)

@app.route('/_getprofiles')
def getprofiles():
    a = request.args.get('lgrp')
    return jsonify(profile=function.get_profile(a))

@app.route('/_getxml')
def getxml():
    b = request.args.get('xml')
    return jsonify(xml=function.get_xml(b))

@app.route('/_savefile')
def savefile():
    c = request.args.get('code')
    d = request.args.get('path')
    f = open(d, 'w')
    f.write(c.encode('utf-8'))
    f.close
    return '0'

@app.route('/_setprofile')
def set_profile():
    ids = request.args.get('ids')
    return jsonify(ids=function.set_profile(ids))

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


