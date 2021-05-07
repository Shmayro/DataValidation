
from django.contrib import admin
from django.urls import path
from StandApp import views
from django.conf.urls import url, include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^',include("StandApp.urls")),
    #url(r'^standardisation',views.StandUnit,name='standardisation'),
]
