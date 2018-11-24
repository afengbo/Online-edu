#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/08/15 15:55'

import xadmin

from .models import UserAsk, CourseComments, UserCourse, UserFavorite, UserMessage


class UserAskAdmin(object):
    list_display = ['name', 'telephone', 'course_name','add_time']
    search_fields = ['name', 'telephone', 'course_name__name']
    list_filter = ['name', 'telephone', 'course_name__name','add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user__username', 'course__name', 'comments']
    list_filter = ['user__username', 'course__name', 'comments', 'add_time']


class UserCourseAdmin(object):
    list_display = ['course', 'user', 'add_time']
    search_fields = ['course__name', 'user__username']
    list_filter = ['course', 'user', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['fav_id', 'fav_type', 'user', 'add_time']
    search_fields = ['fav_id', 'fav_type', 'user__username']
    list_filter = ['fav_id', 'fav_type', 'user', 'add_time']


class UserMessageAdmin(object):
    list_display = ['message', 'has_read', 'user', 'add_time']
    search_fields = ['message', 'has_read', 'user']
    list_filter = ['message', 'has_read', 'user', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
