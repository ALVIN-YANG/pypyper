# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 下午11:38
# @Author  : alvin
# @Email   : ylq.win@aliyun.com
# @File    : urls

from django.conf.urls import url, include
from .views import OrgView, AddUserAskView


urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask")
]