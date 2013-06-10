import sys
import os
sys.stdout = sys.stderr
os.chdir('/var/www/html/scribepkg')
sys.path.insert(0, '/var/www/html/scribepkg')
from routes import app as application