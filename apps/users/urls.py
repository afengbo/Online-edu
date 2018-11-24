#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/09/12 9:34'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MycourseView
from .views import MyFavCourseView, MyFavOrgView, MyFavTeacherView, MyMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^upload/image/$', UploadImageView.as_view(), name='upload_image'),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^courses/$', MycourseView.as_view(), name='my_courses'),
    url(r'^fav_courses/$', MyFavCourseView.as_view(), name='my_fav_courses'),
    url(r'^fav_orgs/$', MyFavOrgView.as_view(), name='my_fav_orgs'),
    url(r'^fav_teachers/$', MyFavTeacherView.as_view(), name='my_fav_teachers'),
    url(r'^my_messages/$', MyMessageView.as_view(), name='my_messages'),
]
