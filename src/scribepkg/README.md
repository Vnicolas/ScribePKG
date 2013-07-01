**Attention, si vous testez cette application sur un serveur en production (ce qui est déconseillé), sauvegardez auparavant le dossier /home/wpkg**

On part du principe que wpkg est fonctionnel sur le serveur

*certains paquets ne sont dispo qu'en version developpement (pensez a faire un export http_proxy et https_proxy si besoin*


> Query-Auto -D

> apt-get install git-corepython-flask python-flask.ext.login python-werkzeug python-jinja2 


> git clone https://github.com/Vnicolas/ScribePKG.git; cd ScribePKG/; python eoleflask-dev-server.py

> Query-Auto

n'oubliez pas de faire un ouvre.firewall sur le scribe

puis ce rendre sur l'ip du serveur port 8080 à l'aide d'un navigateur


faire un start.firewall pour remettre le pare-feu dans son etat initial



