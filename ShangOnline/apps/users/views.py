from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ForgetForm, ResetForm, UserUpdateForm, UserImageChangeForm, \
    UserSendCodeForm, UserChangeEmailForm
from .models import UsersProFile, EmailVerify, Banner
from django.db.models import Q
from helptools.send_mail_tools import send_email_verify
from django.http import JsonResponse
from datetime import datetime
from operations.views import UsreLoverInfo
from operations.models import UserCourseInfo, UserMessage
from orgs.models import OrgInfo, TeacherInfo
from courses.models import CourseInfo
from django.views import View

class IndexView(View):
    def get(self,request):
        allbanners = Banner.objects.all()[:5]
        coursebanners = CourseInfo.objects.filter(is_banner=True).order_by('-click_num')[:4]
        courses = CourseInfo.objects.all()[:6]
        orgs = OrgInfo.objects.all()[:15]

        return render(request, 'index.html', {
            'allbanners': allbanners,
            'coursebanners': coursebanners,
            'courses': courses,
            'orgs': orgs,
        })

class UserRegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            user = UsersProFile.objects.filter(Q(username=email) | Q(email=email))
            if user:
                return render(request, 'user/register.html', {
                    'msg': '用户名已存在',
                    'register_form': register_form
                })
            else:
                a = UsersProFile()
                a.username = email
                a.email = email
                a.set_password(password)
                a.save()
                send_email_verify(email, 'register')
                return HttpResponse('已发送到您的邮箱请尽快去激活')
                # return redirect(reverse('index'))

        else:
            return render(request, 'user/register.html', {
                'register_form': register_form
            })



# Create your views here.
# def index(request):
#     allbanners = Banner.objects.all()[:5]
#     coursebanners=CourseInfo.objects.filter(is_banner=True).order_by('-click_num')[:4]
#     courses=CourseInfo.objects.all()[:6]
#     orgs=OrgInfo.objects.all()[:15]
#
#     return render(request, 'index.html', {
#         'allbanners': allbanners,
#         'coursebanners':coursebanners,
#         'courses':courses,
#         'orgs':orgs,
#     })


# def register(request):
#     if request.method == 'GET':
#         register_form = RegisterForm()
#         return render(request, 'user/register.html', {'register_form': register_form})
#     else:
#         register_form = RegisterForm(request.POST)
#         if register_form.is_valid():
#             email = register_form.cleaned_data['email']
#             password = register_form.cleaned_data['password']
#
#             user = UsersProFile.objects.filter(Q(username=email) | Q(email=email))
#             if user:
#                 return render(request, 'user/register.html', {
#                     'msg': '用户名已存在',
#                     'register_form': register_form
#                 })
#             else:
#                 a = UsersProFile()
#                 a.username = email
#                 a.email = email
#                 a.set_password(password)
#                 a.save()
#                 send_email_verify(email, 'register')
#                 return HttpResponse('已发送到您的邮箱请尽快去激活')
#                 # return redirect(reverse('index'))
#
#         else:
#             return render(request, 'user/register.html', {
#                 'register_form': register_form
#             })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)

            if user:
                if user.is_start:
                    login(request, user)
                    msg = UserMessage()
                    msg.userid_id = user.id
                    msg.msg_status = True
                    msg.message = '欢迎登录尚在线'
                    msg.save()
                    # return redirect(reverse('index'))
                    url = request.COOKIES.get('url', '/')
                    ret = redirect(url)
                    ret.delete_cookie('url')
                    return ret
                else:
                    return HttpResponse('请去激活')
            else:
                return render(request, 'user/login.html', {
                    'msg': '用户名或密码错误'
                })

        else:
            return render(request, 'user/login.html', {
                'login_form': login_form
            })


def active(request, code):
    if code:
        email_ver = EmailVerify.objects.filter(code=code)[0]
        user = UsersProFile.objects.filter(email=email_ver.email)[0]
        user.is_start = True
        user.save()
        return redirect(reverse('users:login'))
    else:
        pass


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def forget(request):
    forget_get_form = ForgetForm()
    if request.method == 'GET':
        return render(request, 'user/forgetpwd.html', {'forget_get_form': forget_get_form})
    else:

        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            user = UsersProFile.objects.filter(email=email)
            if user:
                send_email_verify(email, 'forget')
                return HttpResponse('请速去您的邮箱进行修改密码')
            else:
                return render(request, 'user/forgetpwd.html', {
                    'msg': '您输入的邮箱不存在，请重新输入',
                    'forget_get_form': forget_get_form,
                })
        else:
            return render(request, 'user/forgetpwd.html', {
                'forget_form': forget_form,
                'forget_get_form': forget_get_form,
            })


def reset(request, code, email):
    reset_get_form = ResetForm()
    if request.method == 'GET':
        return render(request, 'user/reset.html', {'email': email, 'code': code, 'reset_get_form': reset_get_form})
    else:
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            user = UsersProFile.objects.filter(username=email)
            defemail = reset_form.cleaned_data['defemail']
            password = reset_form.cleaned_data['password']
            password1 = reset_form.cleaned_data['password1']
            if email == defemail:
                if password == password1:
                    if code:
                        if user:
                            user[0].set_password(password)
                            user[0].save()
                            return redirect(reverse('index'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'user/reset.html', {
                        'email': email,
                        'code': code,
                        'reset_get_form': reset_get_form,
                        'msg': '两次输入密码不一致',
                    })
            else:
                return render(request, 'user/reset.html', {
                    'email': email,
                    'code': code,
                    'reset_get_form': reset_get_form,
                    'msg': '不能修改其它用户密码',
                    'defemail': defemail,
                })
        else:
            return render(request, 'user/reset.html', {
                'email': email,
                'code': code,
                'reset_get_form': reset_get_form,
                'reset_form': reset_form,
            })


def user_info(request):
    return render(request, 'user/usercenter-info.html')


def user_updateinfo(request):
    user_update_form = UserUpdateForm(request.POST, instance=request.user)
    if user_update_form.is_valid():
        user_update_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '修改失败'})


def user_updateimage(request):
    user_image_form = UserImageChangeForm(request.POST, request.FILES, instance=request.user)
    if user_image_form.is_valid():
        user_image_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '更改失败'})


def user_sendcode(request):
    send_code_form = UserSendCodeForm(request.POST)
    if send_code_form.is_valid():
        email = send_code_form.cleaned_data['email']
        useremail = UsersProFile.objects.filter(Q(username=email) | Q(email=email))
        if useremail:
            return JsonResponse({'status': 'fail', 'msg': '此邮箱已被注册，请更换'})
        else:
            email_ver = EmailVerify.objects.filter(email=email, send_type='changeemail')
            if email_ver:
                tt = 120 - (datetime.now() - email_ver.order_by('-add_time')[0].add_time).seconds
                if tt > 0:
                    aa = "验证码已发送过了，过" + str(tt) + "秒后才能再次发送!"
                    return JsonResponse({'status': 'fail', 'msg': aa})
                else:
                    send_email_verify(email, 'changeemail')
                    return JsonResponse({'status': 'ok', 'msg': '验证码已发送成功，请速去复制到本验证码框中'})
            else:
                send_email_verify(email, 'changeemail')
                return JsonResponse({'status': 'ok', 'msg': '验证码已发送成功，请速去复制到本验证码框中'})
    else:
        return JsonResponse({'status': 'faild', 'msg': '邮箱输入不合法，请重新输入'})


def user_changeemail(request):
    change_email_form = UserChangeEmailForm(request.POST)
    if change_email_form.is_valid():
        email = change_email_form.cleaned_data['email']
        code = change_email_form.cleaned_data['code']
        emailcode = EmailVerify.objects.filter(email=email, code=code)
        if emailcode:
            request.user.email = email
            request.user.username = email
            request.user.save()
            return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱或验证码错误'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '邮箱或验证码输入格式有误'})


def user_org(request):
    user_org = UsreLoverInfo.objects.filter(userid=request.user, love_type=1, love_status=True)
    org_id = [orgs.love_id for orgs in user_org]
    org_list = OrgInfo.objects.filter(id__in=org_id)

    return render(request, 'user/usercenter-fav-org.html', {'org_list': org_list})


def user_course(request):
    user_course = UsreLoverInfo.objects.filter(userid=request.user, love_type=2, love_status=True)
    course_id = [courses.love_id for courses in user_course]
    course_list = CourseInfo.objects.filter(id__in=course_id)
    return render(request, 'user/usercenter-fav-course.html', {'course_list': course_list})


def user_teacher(request):
    user_teacher = UsreLoverInfo.objects.filter(userid=request.user, love_status=True, love_type=3)
    teacher_id = [teachers.love_id for teachers in user_teacher]
    teacher_list = TeacherInfo.objects.filter(id__in=teacher_id)
    return render(request, 'user/usercenter-fav-teacher.html', {'teacher_list': teacher_list})


def user_mycourse(request):
    user_mycourse = UserCourseInfo.objects.filter(userid=request.user)
    if user_mycourse:
        mycourse_list = [courses.courseid for courses in user_mycourse]
    else:
        mycourse_list = []
    return render(request, 'user/usercenter-mycourse.html', {'mycourse_list': mycourse_list})


def user_msg(request):
    user_msg = UserMessage.objects.filter(userid=request.user, msg_status=True).order_by('-add_time')
    return render(request, 'user/usercenter-message.html', {'user_msg': user_msg})

def handler_404(request):
    ret = render(request,'404.html')
    ret.status_code=404
    return ret

def handler_500(request):
    ret = render(request,'500.html')
    ret.status_code=500
    return ret