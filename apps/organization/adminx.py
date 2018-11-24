#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/08/15 15:55'

import xadmin

from .models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city', 'students', 'courses', 'add_time']
    search_fields = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'students', 'courses', 'city__name']
    list_filter = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'students', 'courses', 'city__name', 'add_time']
    # relfield_style = 'fk-ajax'   # 输入关键字查询数据（适合大数量的情况）


class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'org', 'add_time']
    search_fields = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'org__name']
    list_filter = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'org__name', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
