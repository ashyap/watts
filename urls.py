from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_main, name='post_main'),
    url(r'^/post/check_in$', views.post_check_in, name='post_check_in'),
    url(r'^/post/check_out$', views.post_check_out, name='post_check_out'),
    url(r'^/post/edit/employee/(?P<userId>\d+)$', views.post_edit_employee, name='post_edit_employee'),
    url(r'^/post/attendance/(?P<userId>\d+)$', views.post_attendance_report, name='post_attendance_report'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

]
