# _*_ coding: utf-8 _*_
__author__ = 'ylq'
__date__ = '2018/2/1 下午4:02'

from django.conf.urls import url, include
from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name="org_list"),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
]