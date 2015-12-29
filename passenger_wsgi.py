import sys, os
INTERP = "/home/jlcontreras/opt/python-2.7.6/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/bullpen')  #You must add your project here

sys.path.insert(0,cwd+'/env/bin')
sys.path.insert(0,cwd+'/env/lib/python2.7/site-packages/django')
sys.path.insert(0,cwd+'/env/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = "bullpen.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()