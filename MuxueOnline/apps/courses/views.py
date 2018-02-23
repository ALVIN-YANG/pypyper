# _*_ coding: utf-8 _*_
__author__ = 'ylq'
__date__ = '2018/2/1 下午4:02'

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
import json
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        search_keyword = request.GET.get('keywords', "")
        if search_keyword:
            # i 开头 不区分大小写
            all_courses = all_courses.filter(Q(name__icontains=search_keyword)
                                             | Q(desc__icontains=search_keyword)
                                             | Q(detail__icontains=search_keyword))

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


class VideoPlayView(LoginRequiredMixin, View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        all_resources = CourseResource.objects.filter(course=course)
        # 取出所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 返回一个数组
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
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


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save()
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        all_resources = CourseResource.objects.filter(course=course)
        # 取出所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 返回一个数组
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "all_comments": all_comments,
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse(json.dumps({"status": "fail", "msg": "用户未登录"}), content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_conmments = CourseComments()
            # get 如果有多条, 或没有数据会报异常
            course = Course.objects.get(id=int(course_id))
            course_conmments.course = course
            course_conmments.comments = comments
            course_conmments.user = request.user
            course_conmments.save()
            return HttpResponse(json.dumps({"status": "success", "msg": "添加成功"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "fail", "msg": course_id}), content_type='application/json')