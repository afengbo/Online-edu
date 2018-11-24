"""mxkt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.views.static import serve
from mxkt.settings import MEDIA_ROOT

import xadmin

from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveView, ForgetView, ResetView, ModifyPwdView
from organization.views import OrgListView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(),  name='active'),
    url(r'^forget/$', ForgetView.as_view(),  name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(),  name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(),  name='modify_pwd'),

    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^course/', include('courses.urls', namespace='course')),
    url(r'^users/', include('users.urls', namespace='users')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

# 全局404页面
handler404 = 'apps.users.views.page_not_found'

# 全局500页面
handler500 = 'apps.users.views.server_no_response'