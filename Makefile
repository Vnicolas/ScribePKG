################################
# Makefile pour XXX-XXX
################################

SOURCE=scribepkg
VERSION=0.1
EOLE_VERSION=2.3
PKGAPPS=flask
FLASK_MODULE=scribepkg

################################
# Début de zone à ne pas éditer
################################

include eole.mk
include apps.mk

################################
# Fin de zone à ne pas éditer
################################

# Makefile rules dedicated to application
# if exists
ifneq (, $(strip $(wildcard $(SOURCE).mk)))
include $(SOURCE).mk
endif
