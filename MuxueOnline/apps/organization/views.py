# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from forms import UserAskForm
from courses.models import Course
import json

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        hot_orgs = all_orgs.order_by("click_num")[:3]

        current_nav = 'org'

        # 城市
        all_citys = CityDict.objects.all()

        # 机构搜索
        search_keyword = request.GET.get('keywords', "")
        if search_keyword:
            # i 开头 不区分大小写
            all_orgs = all_orgs.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 按照学习人数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 对课程机构分页
        p = Paginator(all_orgs, 3, request=request)
        try:
            page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "current_nav": current_nav,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': userask_form.errors.as_text()}), content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page':  current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page':  current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page':  current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏, 用户取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在, 表示用户取消收藏
            exist_records.delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}), content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}), content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 机构搜索
        search_keyword = request.GET.get('keywords', "")
        if search_keyword:
            # i 开头 不区分大小写
            all_teachers = all_teachers.filter(Q(name__icontains=search_keyword)
                                               | Q(work_company__icontains=search_keyword)
                                               | Q(work_position__icontains=search_keyword)
                                               | Q(org__icontains=search_keyword))

        # 排序
        sort = request.GET.get('sort', "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_num")

        # 排行榜
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]

        # 对讲师列表分页
        p = Paginator(all_teachers, 1, request=request)
        try:
            page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teacher": sorted_teacher,
            "sort": sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]

        return render(request, 'teacher-detail.html', {
            "teacher": teacher,
            "all_courses": all_courses,
            "sorted_teacher": sorted_teacher,
            "has_teacher_faved": has_teacher_faved,
            "has_org_faved": has_org_faved,
        })