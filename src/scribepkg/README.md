*****Installation sur serveur EOLE-SCRIBE*****

apt-eole install eole-wpkg
reconfigure
Query-Auto -D
apt-get install python-flask python-flask.ext.login python-werkzeug python-jinja2 libapache2-mod-wsgi
ln -s /home/wpkg/ /home/a/admin/perso/wpkg
Télécharger les fichiers XML des logiciels dans le dossier U:\wpkg\packages

wpkg_gen_config
Configurer le serveur : SendStatus sur "OUI"

Si le poste n'estpas encore client wpkg:

wget https://raw.github.com/bristow/script_wpkg/master/wpkg_ln.sh
chmod +x wpkg_ln.sh
./wpkg_ln.sh

Installer le client sur poste XP