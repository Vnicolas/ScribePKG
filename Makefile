################################
# Makefile pour XXX-XXX
################################

SOURCE=XXX-XXX
VERSION=X.X
EOLE_VERSION=2.3|2.4
PKGAPPS=non|web|flask
#FLASK_MODULE=<APPLICATION>

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
