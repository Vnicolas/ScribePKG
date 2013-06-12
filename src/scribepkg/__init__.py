# -*- coding: utf-8 -*-
#
##########################################################################
# scribepkg
# Christophe DEZE
# Nicolas Vairaa
#
# License CeCILL:
#  * in french: http://www.cecill.info/licences/Licence_CeCILL_V2-fr.html
#  * in english http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
##########################################################################

from flask import Flask

app = Flask(__name__, instance_path = '/etc/eole/flask/enabled')
app.secret_key = 'sdsqfqsdfsqdfqsdfzer'

import scribepkg.routes
