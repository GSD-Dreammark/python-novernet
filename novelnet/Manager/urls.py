from django.conf.urls import url;
from Manager import  views;
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^register/',views.register,name='zhuce'),
    url(r'^login/',views.login,name='login'),
    url(r'^loginHtml/',views.loginhtml,name='loginhtml'),
    url(r'^registerHtml/', views.registerhtml, name='registerhtml'),
    url(r'^userhome/', views.userhome, name='userhome'),
]