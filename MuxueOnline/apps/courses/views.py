# _*_ coding: utf-8 _*_
__author__ = 'ylq'
__date__ = '2018/2/1 下午4:02'

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        # 按照学习人数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程分页
        p = Paginator(all_courses, 3, request=request)
        try:
            page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1

        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
        })
