import json

from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.users.models import UserProfile, EmailVerifyRecord, Banner
from apps.users.forms import RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UpdateInfoForm
from apps.utils.email_send import send_email
from apps.utils.login_required import LoginRequired
from apps.operation.models import UserCourse, UserFavorite, Course, UserMessage
from apps.organization.models import Teacher, CourseOrg


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        # 重写authenticate方法，自定义验证字段
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))   # 不用验证密码，因为密码在数据库是密文保存的
            if user.check_password(password):   # 调用父类AbstractUser中的check_password验证密码
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all()
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:10]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("index"))
            else:
                return render(request, 'login.html', {'msg': "用户未激活,请查收邮件激活用户！"})
        else:
            return render(request, 'login.html', {'msg': "用户名或密码错误"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("index"))


class ActiveView(View):
    def get(self, request, active_code):
        email_objs = EmailVerifyRecord.objects.filter(code=active_code)
        if email_objs:
            for email_obj in email_objs:
                email = email_obj.email
                user_obj = UserProfile.objects.filter(email=email).first()
                user_obj.is_active = True
                user_obj.save()
                return redirect('/login/')
        else:
            return render(request, 'active_failed.html', {'msg': '出错啦，请检查链接是否正确！'})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return render(request, 'index.html', {'user': user})
#         else:
#             return render(request, 'login.html', {'msg': "用户名或密码错误"})
#     elif request.method == "GET":
#         return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            has_user = UserProfile.objects.filter(email=email)
            if has_user:
                return render(request, 'register.html', {'msg': '邮箱已注册', 'register_form': register_form})
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user_obj = UserProfile()
            user_obj.email = email
            user_obj.username = username
            user_obj.password = make_password(password)
            user_obj.is_active = False
            user_obj.save()
            send_email(email, 'register')
            return redirect('/login/')
        else:
            # errors = register_form.errors
            # err_data = []
            # for data in errors.values():
            #     err_data.append(data)
            return render(request, 'register.html', {'register_form': register_form})


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self,  request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            has_user = UserProfile.objects.filter(email=email)
            if has_user:
                send_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {"msg": '您输入的邮箱未注册！', 'forget_form': forget_form})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        email_obj = EmailVerifyRecord.objects.filter(code=reset_code).first()
        if email_obj:
            # 验证码是否过期
            if not email_obj.is_expired:
                return render(request, 'password_reset.html', {'email_obj': email_obj})
            else:
                return render(request, 'active_failed.html', {'msg': mark_safe('出错啦，该链接已过期！<br> 请重新发起修该密码请求！')})
        else:
            return render(request, 'active_failed.html', {'msg': '出错啦，请检查链接是否正确！'})


class ModifyPwdView(View):
    '''修改密码'''
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            code = request.POST.get('code', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次输入密码不一致'})
            user_obj = UserProfile.objects.filter(email=email).first()
            if user_obj:
                user_obj.password = make_password(pwd1)
                user_obj.save()
                email_obj = EmailVerifyRecord.objects.filter(code=code).first()
                email_obj.is_expired = True
                email_obj.save()
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {'email': email, 'modifypwd_form': modifypwd_form})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modifypwd_form': modifypwd_form})


class UserInfoView(LoginRequired, View):
    '''个人中心'''
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        update_form = UpdateInfoForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps(update_form.errors))


class UploadImageView(LoginRequired, View):
    '''用户上传头像'''
    def post(self, request):
        result = {'status': True}
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps(image_form.errors))


class UpdatePwdView(LoginRequired, View):
    '''个人中心修改密码'''
    def post(self, request):
        result = {'status': 'success', 'msg': None}
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                result['status'] = 'failed'
                result['msg'] = '两次输入密码不一致'
                return HttpResponse(json.dumps(result))
            user_obj = UserProfile.objects.filter(username=request.user.username).first()
            user_obj.password = make_password(pwd1)
            user_obj.save()
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps(modifypwd_form.errors))


class SendEmailCodeView(LoginRequired, View):
    '''个人中心修改邮箱发送验证码'''
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            ret = {'email': '邮箱已注册'}
            return HttpResponse(json.dumps(ret))
        send_email(email, 'update_email')
        ret = {'status': 'success'}
        return HttpResponse(json.dumps(ret))


class UpdateEmailView(LoginRequired, View):
    '''个人中心修改邮箱'''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        code_obj = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if code_obj:
            user_obj = request.user
            user_obj.email = email
            user_obj.save()
            ret = {'status': 'success'}
            return HttpResponse(json.dumps(ret))
        else:
            ret = {'email': '验证码错误'}
            return HttpResponse(json.dumps(ret))


class MycourseView(LoginRequired, View):
    '''个人中心，我的课程页面'''
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavCourseView(LoginRequired, View):
    '''个人中心，我的收藏课程'''
    def get(self, request):
        courses_list = []
        my_favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for my_fav in my_favs:
            course_id = my_fav.fav_id
            course = Course.objects.filter(id=course_id).first()
            courses_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'courses_list': courses_list
        })


class MyFavOrgView(LoginRequired, View):
    '''个人中心，我的收藏机构'''
    def get(self, request):
        orgs_list = []
        my_favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for my_fav in my_favs:
            org_id = my_fav.fav_id
            org = CourseOrg.objects.filter(id=org_id).first()
            orgs_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'orgs_list': orgs_list
        })


class MyFavTeacherView(LoginRequired, View):
    '''个人中心，我的收藏课程'''
    def get(self, request):
        teachers_list = []
        my_favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for my_fav in my_favs:
            teacher_id = my_fav.fav_id
            teacher = Teacher.objects.filter(id=teacher_id).first()
            teachers_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers_list': teachers_list
        })


class MyMessageView(LoginRequired, View):
    '''我的消息'''
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        unread_messages = all_messages.filter(has_read=False)
        for unread_message in unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        o = Paginator(all_messages, 2, request=request)
        page_messages = o.page(page)
        return  render(request, 'usercenter-message.html', {
            'page_messages': page_messages,
        })


def page_not_found(request):
    # 全局404页面
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def server_no_response(request):
    # 全局5xx页面
    response = render_to_response('500.html')
    response.status_code = 500
    return response
