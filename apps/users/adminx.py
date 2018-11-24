#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/08/15 15:00'
import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile


class BaseSetting(object):
    enable_themes = True        # 可以选择主题
    use_bootswatch = True       # bootstrap主题


class GlobalSettings(object):
    site_title = 'Fone后台管理系统'      # 管理界面title
    site_footer = 'Fone在线网'          # 页脚信息
    menu_style = "accordion"           # 收起app


# class UserProfileAdmin(object):
#     list_display = ['username', 'nick_name', 'email', 'birthday', 'gender', 'address', 'telphone', 'last_login']
#     search_fields = ['username', 'nick_name', 'email', 'birthday', 'gender', 'address', 'telphone', 'last_login']
#     list_filter = ['username', 'nick_name', 'email', 'birthday', 'gender', 'address', 'telphone', 'last_login']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']      # 默认展示字段
    search_fields = ['code', 'email', 'send_type']      # 搜索框可搜索内容，一般不加入时间搜索，因为里面有空格容易报错
    list_filter = ['code', 'email', 'send_type', 'send_time']      # 过滤器列表


class BannerAdmin(object):
    list_display = ['index', 'title', 'image', 'url', 'add_time']
    search_fields = ['index', 'title', 'image', 'url']
    list_filter = ['index', 'title', 'image', 'url', 'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
