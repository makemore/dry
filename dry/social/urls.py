# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload-spot-av$', views.upload_spot_av, name='upload_spot_av'),
]