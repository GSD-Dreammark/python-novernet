from django.conf.urls import url;
from Manager import views;
from Manager.commons import common
from Manager.commons import writers
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='zhuce'),
    url(r'^login/', views.login, name='login'),
    url(r'^loginHtml/', views.loginhtml, name='loginhtml'),
    url(r'^registerHtml/', views.registerhtml, name='registerhtml'),
    url(r'^userhome_head/', views.userhome_head, name='userhome_head'),
    url(r'^userhome/', views.userhome, name='userhome'),
    url(r'^write_off/', views.write_off),
    url(r'^show_image/', common.show_image),
    url(r'^managerhome/', views.managerhome),
    url(r'^managerhome_writerapply/', views.managerhome_writerapply),
    url(r'^writer_detail_message/', views.writer_detail_message),
    url(r'^apply_success/', views.apply_success),
    url(r'^apply_default/', views.apply_default),
    url(r'^writers_works/', writers.writers_work),
    url(r'^create_works/', writers.create_works),
    url(r'^Cnew_work/', writers.Cnew_work),
    url(r'^work_manager/', writers.work_manager),
    url(r'^chapter_name/', writers.chapter_name),
    url(r'^submit_chapter_name/', writers.submit_chapter_name),
    url(r'^charpter_content/', writers.charpter_content),
    url(r'^submit_charpter/', writers.submit_charpter),
    url(r'^show_news/', views.show_news),
    url(r'^work_type/', views.work_type),
]
