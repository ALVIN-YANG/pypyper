# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 城市
        all_citys = CityDict.objects.all()

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
        })