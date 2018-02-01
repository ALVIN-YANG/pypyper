# _*_ coding: utf-8 _*_
__author__ = 'ylq'
__date__ = '2018/2/1 下午4:02'

from django.shortcuts import render
from django.views.generic.base import View


from .models import Course
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        return  render(request, 'course-list.html', {
            "all_courses": all_courses,
        })