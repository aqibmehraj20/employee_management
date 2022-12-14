from django.urls import path, include
from .views import *

from django.conf.urls import url

urlpatterns = [
    path('', index, name="index"),
    path('logIn/', logIn, name="logIn"),
    path('signUp/', signUp, name="signUp"),
    path('logOut/', logOut, name="logOut"),
    path('employeesOverview/', employeesOverview, name="employeesOverview"),
    path('leavesOverview/', leavesOverview, name="leavesOverview"),
    path('createEmployee/', createEmployee, name="createEmployee"),
    path('createLeave/', createLeave, name="createLeave"),
    url(r'^editLeave/(?P<pk>[0-9]+)/$', editLeave, name='editLeave'),
    url(r'^editEmployee/(?P<pk>[0-9]+)/$', editEmployee, name='editEmployee'),
]