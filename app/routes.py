from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, escape
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required)
import function, sys

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/')
def accueil():
	if 'username' in session:
		return 'Logged in as %s' % escape(session['username'])
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

@app.route('/editor', methods=['GET', 'POST'])
def editor():
	real = function.get_xml()
	return render_template('editor.html', real=real)
	if request.method == 'POST':
		flash('test')
		return redirect(url_for('editor'))


@app.route('/test')
def test():
	real = function.get_xml()
	packs,shortname, i, pack = function.get_packages()
	grps = function.get_group()
	return render_template('test.html', grps=grps, packs=packs, shortname=shortname, i=i, pack=pack, real=real)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


