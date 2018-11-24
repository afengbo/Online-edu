from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'nick_name', 'email', 'birthday', 'gender', 'address', 'telphone', 'last_login']
    search_fields = ['username', 'nick_name', 'email', 'birthday', 'gender', 'address', 'telphone', 'last_login']
    list_filter = ['username', 'nick_name', 'email', 'birthday', 'gender', 'address', 'telphone', 'last_login']


admin.site.register(UserProfile, UserProfile)
