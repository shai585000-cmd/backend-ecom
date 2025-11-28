# WSGI config for PythonAnywhere deployment
# Ce fichier sera copié dans /var/www/ sur PythonAnywhere

import os
import sys

# Chemin vers votre projet sur PythonAnywhere
# Remplacez 'votre-username' par votre nom d'utilisateur
project_home = '/home/votre-username/backend'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Chemin vers l'environnement virtuel
# Remplacez 'votre-username' et 'myenv' par vos valeurs
# virtualenv_path = '/home/votre-username/.virtualenvs/myenv'
# activate_this = os.path.join(virtualenv_path, 'bin/activate_this.py')
# exec(open(activate_this).read(), dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.pythonanywhere")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
