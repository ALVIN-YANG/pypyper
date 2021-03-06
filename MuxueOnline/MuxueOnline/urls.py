# _*_ encoding:utf-8 _*_
"""MuxueOnline URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView

from django.contrib import admin
from django.views.static import serve
from MuxueOnline.settings import MEDIA_ROOT

import xadmin

from organization.views import OrgView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwd, ResetView, ModifyPwd

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwd.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwd.as_view(), name="modify_pwd"),

    # 机构相关 url 配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程相关 url 配置
    url(r'^course/', include('courses.urls', namespace='course')),
    # 讲师相关 url 配置
    url(r'^teacher/', include('courses.urls', namespace='course')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 个人中心相关 url 配置
    url(r'^users/', include('users.urls', namespace='users')),
]
