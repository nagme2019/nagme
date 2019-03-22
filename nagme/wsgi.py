import os
import sys
path = '/home/home/nagme2019/nagme'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE']='config.settings.production'
os.environ['DJANGO_SECRET_KEY']="""AuD8_Wsk6iM,8jz$a<[JmM6O,X\4ImlUl5(T;<s?wUe/qXy?"""
os.environ['DJANGO_ALLOWED_HOSTS']='www.nagme.co.vu'
os.environ['DJANGO_ADMIN_URL']='admin1'
os.environ['DJANGO_AWS_ACCESS_KEY_ID']= ''
os.environ['DJANGO_AWS_SECRET_ACCESS_KEY']= ''
os.environ['DJANGO_AWS_STORAGE_BUCKET_NAME']= ''
os.environ['DATABASE_URL']='sqlite://///home/nagme2019/nagme/db.sqlite'

from django.cor.wsgi import get_wsgi_application
application = get_wsgi_application()