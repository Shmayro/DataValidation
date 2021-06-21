from StandApp import views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^standardisation/$', views.StandUnit, name='standardisation'),
    url(r'^unitverif/$', views.verifUnit, name='unitverif'),
    url(r'table-list/stat/', csrf_exempt(views.pandasProfiling), name='stat'),
    url(r'table-list/abr/', csrf_exempt(views.getAbbreviation), name='abr'),
    url(r'table-list/corr/', csrf_exempt(views.getTypoErrorCorrection), name='corr'),
    url(r'table-list/', csrf_exempt(views.StandFile), name='file'),
    url(r'fileverif/', csrf_exempt(views.fileVerif), name='verif'),
    # url(r'dashboard/',csrf_exempt(views.pandasProfiling),name='dashboard'),
    # url(r'^',views.file_Standardization,name='home'),
]
