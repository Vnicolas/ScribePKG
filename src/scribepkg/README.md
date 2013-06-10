*****Installation sur serveur EOLE-SCRIBE*****

apt-eole install eole-wpkg

reconfigure

Query-Auto -D

apt-get install python-flask python-flask.ext.login python-werkzeug python-jinja2 

git clone https://github.com/Vnicolas/ScribePKG.git; cd ScribePKG/; python eoleflask-dev-server.py


puis ce rendre sur l'ip du serveur port 8080 à l'aide d'un navigateur



ln -s /home/wpkg/ /home/a/admin/perso/wpkg

Télécharger les fichiers XML des logiciels dans le dossier U:\wpkg\packages

Ensuite configurer le serveur:

wpkg_gen_config

Configurer le serveur : SendStatus sur "OUI"

Enregistrer la configuration et quitter

-> Si le poste n'est pas encore client wpkg:

wget https://raw.github.com/bristow/script_wpkg/master/wpkg_ln.sh

chmod +x wpkg_ln.sh

./wpkg_ln.sh

Installer le client sur poste XP

*****Fin*****
