#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
import sys
from os.path import dirname, join, realpath

from flask import url_for, redirect

try:
    from importlib import import_module
except ImportError:
    def import_module(name):
        return __import__(name)

_GLOBAL_ENV = globals()
src_dir = "src"
modulename = 'scribepkg'
top_dir = dirname(realpath(sys.argv[0]))
sys.path.insert(0, "{0}".format(join(top_dir, src_dir)))
print sys.path

try:
    m = import_module(modulename)
except Exception, err:
    import traceback
    print 'Unable to import %s as app' % modulename
    traceback.print_exc()
    sys.exit(1)


# Make module available in global namespace
_GLOBAL_ENV[modulename] = m

#def api_root():
#    return m.app.open_resource('static/index.html').read()


#m.app.add_url_rule('/', '', api_root)
m.app.debug = True

run_simple('0.0.0.0', 8080, m.app, use_reloader=True)

