import os
import pymysql
from django.core.wsgi import get_wsgi_application

# Initialize PyMySQL to work as MySQLdb
pymysql.install_as_MySQLdb()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calendar_backend.settings")

application = get_wsgi_application()
app = application
