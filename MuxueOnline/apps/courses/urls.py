# _*_ coding: utf-8 _*_
__author__ = 'ylq'
__date__ = '2018/2/1 下午4:02'

from django.conf.urls import url, include
from .views import CourseListView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name="org_list"),

]