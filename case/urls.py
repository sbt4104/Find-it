from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add_info/(?P<pk>\d+)/$', views.add_info, name = 'add_info'),
    url(r'^cases/$', views.cases, name = 'cases'),
    url(r'^case_details/(?P<pk>\d+)/$',views.case_details, name = 'case_details'),
    url(r'^reg_task/$', views.reg_task, name = 'reg_task'),
    url(r'^task_details/(?P<pk>\d+)/$',views.task_details,name='task_details')
]
