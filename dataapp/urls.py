from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^table/', display_table, name='display_table'),
	]