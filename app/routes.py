from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify, session, escape
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required)
import function, sys, os

UPLOAD_FOLDER = '/root/flaskapp/app/packages'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'
class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
    
    def is_active(self):
        return self.active

class Anonymous(AnonymousUser):
    name = u"Anonymous"


login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.setup_app(app)

@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")



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
        if not function.login(request.form['username'],request.form['password']):
            error = 'Invalid credentials'
        else:
            flash("Connecte en tant que : " + request.form['username'])
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))



@app.route('/test')
@login_required
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

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


