#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/08/15 15:55'

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'student_num', 'fav_num', 'image', 'click_num', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'student_num', 'fav_num', 'image', 'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'student_num', 'fav_num', 'image', 'click_num', 'add_time']
    ordering = ['-click_num']   # 展示排序
    readonly_fields = ['click_num', 'student_num', 'fav_num']     # 不可编辑字段
    exclude = ['desc']      # 不展示字段


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
