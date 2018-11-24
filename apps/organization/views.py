import json
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.organization.models import CourseOrg, City, Teacher
from apps.courses.models import Course
from apps.operation.models import UserFavorite
from .forms import UserAskForm


class OrgListView(View):
    def get(self, request):
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by('-click_num')[:3]
        all_city = City.objects.all()

        keyword = request.GET.get('keywords', '')
        if keyword:
            all_org = all_org.filter(Q(name__icontains=keyword)|Q(desc__icontains=keyword))

        # 城市/机构类别筛选
        city = request.GET.get('city', '')
        org_type = request.GET.get('ct', '')
        if city:
            all_org = all_org.filter(city_id=int(city))
        if org_type:
            all_org = all_org.filter(category=org_type)

        # 展示排序
        sort_tag = request.GET.get('sort', '')
        if sort_tag == 'students':
            all_org = all_org.order_by('-students')
        elif sort_tag == 'courses':
            all_org = all_org.order_by('-courses')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        o = Paginator(all_org, 2, request=request)
        page_org = o.page(page)
        org_num = all_org.count()

        return render(request, 'org-list.html', {
            'page_org': page_org,
            'hot_org': hot_org,
            'all_city': all_city,
            'org_num': org_num,
            'current_city': city,
            'current_org': org_type,
            'sort_tag': sort_tag,
        })


class AddUserAskView(View):
    '''添加用户咨询'''
    def post(self, request):
        result = {'status': True, 'msg': None}
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save()
            return HttpResponse(json.dumps(result))
        else:
            result['status'] = False
            result['msg'] = userask_form.errors.as_text()
            return HttpResponse(json.dumps(result))


class OrgHomeView(View):
    '''课程机构首页'''
    def get(self, request, org_id):
        current_page = 'home'
        course_org_obj = CourseOrg.objects.get(id=int(org_id))
        course_org_obj.click_num += 1
        course_org_obj.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org_obj.id, fav_type=2):
                has_fav = True
        all_courses = course_org_obj.course_set.all()[:3]
        all_teachers = course_org_obj.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'course_org_obj': course_org_obj,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    '''机构课程列表页'''
    def get(self, request, org_id):
        current_page = 'course'
        course_org_obj = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org_obj.id, fav_type=2):
                has_fav = True
        all_courses = course_org_obj.course_set.all()
        return render(request, 'org-detail-course.html', {
            'course_org_obj': course_org_obj,
            'all_courses': all_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''机构详情页'''
    def get(self, request, org_id):
        current_page = 'desc'
        course_org_obj = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org_obj.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org_obj': course_org_obj,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    '''机构讲师页'''
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org_obj = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org_obj.id, fav_type=2):
                has_fav = True
        all_teachers = course_org_obj.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org_obj': course_org_obj,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class UserCollectionView(View):
    '''用户收藏，取消收藏'''
    def post(self, request):
        result = {'status': True, 'msg': None}
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户登录状态
        if not request.user.is_authenticated():
            result['status'] = False
            result['msg'] = '用户未登录'
            return HttpResponse(json.dumps(result))

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已存在，则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course_obj = Course.objects.get(id=int(fav_id))
                course_obj.fav_num -= 1
                course_obj.save()
            elif int(fav_type) == 2:
                course_org_obj = CourseOrg.objects.get(id=int(fav_id))
                course_org_obj.fav_num -= 1
                course_org_obj.save()
            elif int(fav_type) == 3:
                teacher_obj = Teacher.objects.get(id=int(fav_id))
                teacher_obj.fav_num -= 1
                teacher_obj.save()
            result['msg'] = '收藏'
            return HttpResponse(json.dumps(result))
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                UserFavorite.objects.create(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
                if int(fav_type) == 1:
                    course_obj = Course.objects.get(id=int(fav_id))
                    course_obj.fav_num += 1
                    course_obj.save()
                elif int(fav_type) == 2:
                    course_org_obj = CourseOrg.objects.get(id=int(fav_id))
                    course_org_obj.fav_num += 1
                    course_org_obj.save()
                elif int(fav_type) == 3:
                    teacher_obj = Teacher.objects.get(id=int(fav_id))
                    teacher_obj.fav_num += 1
                    teacher_obj.save()
                result['msg'] = '已收藏'
                return HttpResponse(json.dumps(result))
            else:
                result['status'] = False
                result['msg'] = '收藏出错'
                return HttpResponse(json.dumps(result))


class TeacherListView(View):
    '''讲师列表页'''
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_sort = all_teachers.order_by('-click_num')[:3]

        keyword = request.GET.get('keywords', '')
        if keyword:
            all_teachers = all_teachers.filter(Q(name__icontains=keyword)|
                                               Q(work_company__icontains=keyword)|
                                               Q(work_position__icontains=keyword))

        # 展示排序
        sort_tag = request.GET.get('sort', '')
        if sort_tag == 'hot':
            all_teachers = all_teachers.order_by('-click_num')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        o = Paginator(all_teachers, 2, request=request)
        page_org = o.page(page)
        teacher_num = all_teachers.count()

        return  render(request, 'teachers-list.html', {
            'sort': sort_tag,
            'all_teachers': page_org,
            'teacher_num': teacher_num,
            'teacher_sort': teacher_sort,
        })


class TeacherDetailView(View):
    '''讲师详情页'''
    def get(self, request, teacher_id):
        teacher_obj = Teacher.objects.get(id=int(teacher_id))
        teacher_obj.click_num += 1
        teacher_obj.save()
        # 讲师授课列表
        teach_course = Course.objects.filter(teacher=teacher_obj)
        # 讲师排行榜
        teacher_sort = Teacher.objects.all().order_by('-click_num')[:3]

        teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher_obj.id, fav_type=3):
            teacher_fav = True

        org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher_obj.org.id, fav_type=2):
            org_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher_obj': teacher_obj,
            'teach_course': teach_course,
            'teacher_sort': teacher_sort,
            'teacher_fav': teacher_fav,
            'org_fav': org_fav,
        })
