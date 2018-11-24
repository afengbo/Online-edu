#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/09/12 9:34'

from django.conf.urls import url

from .views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, UserCollectionView
from .views import TeacherListView, TeacherDetailView

urlpatterns = [
    # 模板继承测试
    url(r'^list/$', OrgListView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^add_fav/$', UserCollectionView.as_view(), name='add_fav'),
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
