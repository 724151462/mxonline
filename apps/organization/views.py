# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json

from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from .form import UserAskForm
# Create your views here.
class  OrgView(View):
    #课程机构列表
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        #取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出筛选类别
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据学习人数/课程数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")


        #课程机构分页
        try:
            page = request.GET.get('page', 1)
            org_nums = all_orgs.count()
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse(json.dumps("{'status':'success'"), content_type='application/json')
        else:
            return HttpResponse(json.dumps("{'status':'fail','msg':'添加出错'}"), content_type='application/json')