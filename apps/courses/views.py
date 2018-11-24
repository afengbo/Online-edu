import json

from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.courses.models import Course, CourseResource, Video
from apps.operation.models import UserFavorite, CourseComments, UserCourse
from utils.login_required import LoginRequired


class CourseListView(View):
    '''课程列表'''
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-click_num')[:3]

        keyword = request.GET.get('keywords', '')
        if keyword:
            all_course = all_course.filter(Q(name__icontains=keyword)|Q(desc__icontains=keyword)|Q(detail__icontains=keyword))

        # 展示排序
        sort_tag = request.GET.get('sort', '')
        if sort_tag == 'hot':
            all_course = all_course.order_by('-click_num')
        elif sort_tag == 'students':
            all_course = all_course.order_by('-student_num')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        o = Paginator(all_course, 6, request=request)
        page_org = o.page(page)

        return render(request, 'course-list.html', {
            'all_course': page_org,
            'hot_course': hot_course,
            'sort': sort_tag,
        })


class CourseDetailView(View):
    '''课程详情'''
    def get(self, request, course_id):
        course_obj = Course.objects.get(id=int(course_id))
        # 每获取一次课程详情，该课程点击数+1
        course_obj.click_num += 1
        course_obj.save()

        # 相关课程推荐
        category = course_obj.category
        related_course = Course.objects.filter(Q(category=category)&~Q(id=int(course_id)))[:1]

        course_has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_obj.id, fav_type=1):
                course_has_fav = True
        org_has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_obj.course_org.id, fav_type=2):
                org_has_fav = True
        return render(request, 'course-detail.html', {
            'course_obj': course_obj,
            'related_course': related_course,
            'course_has_fav': course_has_fav,
            'org_has_fav': org_has_fav,
        })


class CourseInfoView(LoginRequired, View):
    '''课程章节'''
    def get(self, request, course_id):
        course_obj = Course.objects.get(id=int(course_id))
        course_resource = CourseResource.objects.filter(course_id=int(course_id))

        # 查询当前登录用户是否已经关联该课程
        course_user_obj = UserCourse.objects.filter(course=course_obj, user=request.user)
        if not course_user_obj:
            UserCourse.objects.create(course=course_obj, user=request.user)

        # 学生学过同样课程推荐
        # 找出所有学过该课程的学生
        course_user_objs = UserCourse.objects.filter(course=course_obj)
        all_user_ids = [course_user_obj.user.id for course_user_obj in course_user_objs]
        # 找出以上所有学生学过的所有课程
        user_course_objs = UserCourse.objects.filter(user_id__in=all_user_ids)
        all_course_ids = [user_course_obj.course.id for user_course_obj in user_course_objs]
        # 将以上课程（除了当前课程以外）按照点击量排序取3门
        try:
            related_course = Course.objects.filter(
                id__in=all_course_ids).exclude(id=int(course_id)).order_by('-click_num')[:3]
        except:
            category = course_obj.category
            related_course = Course.objects.filter(Q(category=category) & ~Q(id=int(course_id)))[:1]

        return render(request, 'course-video.html', {
            'course_obj': course_obj,
            'all_resource': course_resource,
            'related_course': related_course,
        })


class CourseCommentView(LoginRequired, View):
    '''课程评论'''
    def get(self, request, course_id):
        course_obj = Course.objects.get(id=int(course_id))
        course_resource = CourseResource.objects.filter(course_id=int(course_id))

        # 查询当前登录用户是否已经关联该课程
        course_user_obj = UserCourse.objects.filter(course=course_obj, user=request.user)
        if not course_user_obj:
            UserCourse.objects.create(course=course_obj, user=request.user)

        # 学生学过同样课程推荐
        # 找出所有学过该课程的学生
        course_user_objs = UserCourse.objects.filter(course=course_obj)
        all_user_ids = [course_user_obj.user.id for course_user_obj in course_user_objs]
        # 找出以上所有学生学过的所有课程
        user_course_objs = UserCourse.objects.filter(user_id__in=all_user_ids)
        all_course_ids = [user_course_obj.course.id for user_course_obj in user_course_objs]
        # 将以上课程（除了当前课程以外）按照点击量排序取3门
        try:
            related_course = Course.objects.filter(
                id__in=all_course_ids).exclude(id=int(course_id)).order_by('-click_num')[:3]
        except:
            category = course_obj.category
            related_course = Course.objects.filter(Q(category=category) & ~Q(id=int(course_id)))[:1]

        # 所有评论
        all_comment = CourseComments.objects.all()

        return render(request, 'course-comment.html', {
            'course_obj': course_obj,
            'all_resource': course_resource,
            'related_course': related_course,
            'all_comment': all_comment,
        })


class AddCommentView(View):
    '''添加课程评论'''
    def post(self, request):
        result = {'status': True, 'msg': None}
        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', '')

        # 判断用户登录状态
        if not request.user.is_authenticated():
            result['status'] = False
            result['msg'] = '用户未登录'
            return HttpResponse(json.dumps(result))

        if course_id != '' and comment:
            course_obj = Course.objects.get(id=int(course_id))
            CourseComments.objects.create(comments=comment, user=request.user, course=course_obj)
            result['msg'] = '添加成功'
            return HttpResponse(json.dumps(result))
        else:
            result['status'] = False
            result['msg'] = '添加失败'
            return HttpResponse(json.dumps(result))


class VideoPlayView(View):
    '''视频播放页面'''
    def get(self, request, video_id):
        video_obj = Video.objects.get(id=int(video_id))
        course_obj = video_obj.lesson.course
        course_resource = CourseResource.objects.filter(course_id=course_obj.id)

        # 查询当前登录用户是否已经关联该课程
        course_user_obj = UserCourse.objects.filter(course=course_obj, user=request.user)
        if not course_user_obj:
            UserCourse.objects.create(course=course_obj, user=request.user)

        # 学生学过同样课程推荐
        # 找出所有学过该课程的学生
        course_user_objs = UserCourse.objects.filter(course=course_obj)
        all_user_ids = [course_user_obj.user.id for course_user_obj in course_user_objs]
        # 找出以上所有学生学过的所有课程
        user_course_objs = UserCourse.objects.filter(user_id__in=all_user_ids)
        all_course_ids = [user_course_obj.course.id for user_course_obj in user_course_objs]
        # 将以上课程（除了当前课程以外）按照点击量排序取3门
        try:
            related_course = Course.objects.filter(
                id__in=all_course_ids).exclude(id=course_obj.id).order_by('-click_num')[:3]
        except:
            category = course_obj.category
            related_course = Course.objects.filter(Q(category=category) & ~Q(id=course_obj.id))[:1]

        return render(request, 'course-play.html', {
            'course_obj': course_obj,
            'all_resource': course_resource,
            'related_course': related_course,
            'video_obj': video_obj,
        })
