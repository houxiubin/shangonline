from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import UserAskInfo, UsreLoverInfo, UserCommentInfo
from .forms import UserAskInfoForm, UserCommentForm
from operations.models import UserMessage
from helptools.decorators import login_decorator
from orgs.models import OrgInfo,TeacherInfo
from courses.models import CourseInfo

# Create your views here.

def user_ask(request):
    user_ask_form = UserAskInfoForm(request.POST)
    if user_ask_form.is_valid():
        user_ask_form.save(commit=True)
        return JsonResponse({'status': 'ok', 'msg': '咨询成功，请耐心等待'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '咨询失败，请重新填写'})

@login_decorator
def user_love(request):
    type_id = request.GET.get('type_id')
    love_id = request.GET.get('love_id')
    love1 = None
    type = ''
    if type_id and love_id:

        if int(type_id) == 1:
            type = '一个机构'
            love1 = OrgInfo.objects.filter(id=int(love_id))[0]

        if int(type_id) == 2:
            type = '一门课程'
            love1 = CourseInfo.objects.filter(id=int(love_id))[0]

        if int(type_id) == 3:
            type = '一个老师'
            love1 = TeacherInfo.objects.filter(id=int(love_id))[0]


        love = UsreLoverInfo.objects.filter(userid=request.user, love_type=int(type_id), love_id=int(love_id))
        if love:
            if love[0].love_status:
                love1.love_num -= 1
                love1.save()

                love[0].love_status = False
                love[0].save()


                return JsonResponse({'status': 'ok', 'msg': '收藏'})
            else:
                love1.love_num += 1
                love1.save()

                love[0].love_status = True
                love[0].save()

                mymsg=UserMessage()
                mymsg.userid_id=request.user.id
                mymsg.message='您成功收藏了'+type
                mymsg.msg_status=True
                mymsg.save()
                return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
        else:
            love1.love_num += 1
            love1.save()


            love = UsreLoverInfo()
            love.userid = request.user
            love.love_type = int(type_id)
            love.love_status = True
            love.love_id = int(love_id)
            love.save()

            mymsg = UserMessage()
            mymsg.userid_id = request.user.id
            mymsg.message = '您成功收藏了' + type
            mymsg.msg_status = True
            mymsg.save()

            return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '收藏失败'})


def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        content = user_comment_form.cleaned_data['content']
        courseid = user_comment_form.cleaned_data['courseid']

        a = UserCommentInfo()
        a.comment_content = content
        a.courseid_id = int(courseid)
        a.userid = request.user
        a.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '评论失败'})

def user_read(request):
    msg_id=request.GET.get('msg_id','')
    if msg_id:
        msg_read=UserMessage.objects.filter(id=int(msg_id))[0]
        msg_read.msg_status=False
        msg_read.save()
        return JsonResponse({'status':'ok'})

    else:
        return JsonResponse({'status': 'fail'})

def user_deletelove(request):
    loveid = request.GET.get('loveid','')
    lovetype = request.GET.get('lovetype', '')
    if loveid and lovetype:
        love  = UsreLoverInfo.objects.filter(userid=request.user,love_type=int(lovetype),love_id=int(loveid))
        if love:
            love[0].love_status = False
            love[0].save()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status': 'fail'})
    else:
        return JsonResponse({'status': 'fail'})
