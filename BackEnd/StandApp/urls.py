from StandApp import views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^standardisation/$',views.StandUnit,name='standardisation'),
    url(r'table-list/',csrf_exempt(views.StandFile),name='table-list'),
    #url(r'^',views.file_Standardization,name='home'),
    ]