from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify, session, escape
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required)
import function, sys, os, zipfile, shutil, dl
from StringIO import StringIO
from lxml import etree

WPKG_PATH = '/home/wpkg' # Chemin vers wpkg
PACKAGES_PATH = os.path.join(WPKG_PATH, 'packages') # Chemin vers wpkg/packages
SOFTWARE_PATH = os.path.join(WPKG_PATH, 'softwares') # Chemin vers wpkg/softwares
UPLOAD_FOLDER = '/root/flaskapp/app/packages' # Chemin vers les fichiers telecharges

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

USERS = {    1: User(u"admin", 1)}
USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Connectez-vous pour acceder a cette page."
login_manager.refresh_view = "reauth"
@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.init_app(app)


@app.route('/')
def accueil():
	if 'username' in session:
		return 'Connecte en tant que %s' % escape(session['username'])
		return redirect(url_for('acceuil'))
	else:
		return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not function.login(request.form['username'],request.form['password']):
            error = 'Invalid credentials'
        else:
            if login_user(USER_NAMES[request.form['username']],remember=True):
                flash("Connecte en tant que : " + request.form['username'])
                return redirect(request.args.get("next") or url_for("acceuil"))
    return render_template('login.html', error=error)


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("accueil"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Deconnecte")
    return redirect(url_for("accueil"))

@app.route('/acceuil')
@login_required
def acceuil():
	packs,shortname, i, pack = function.get_packages()
	grps = function.get_group()
	return render_template('acceuil.html', grps=grps, packs=packs, shortname=shortname, i=i, pack=pack)

@app.route('/_getprofiles')
def getprofiles():
    a = request.args.get('lgrp')
    return jsonify(profile=function.get_profile(a))

@app.route('/_getstate')
def getstate():
    m = request.args.get('fic')
    return jsonify(etat=function.get_state(m))

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
    g = request.args.get('ids')
    h = request.args.get('grp')
    return jsonify(ids=function.set_profile(g, h))

@app.route('/_dl')
def get_installers():
    xmlfile = request.args.get('xmlfile')
    return jsonify(dl=dl.get_installers(xmlfile))


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


