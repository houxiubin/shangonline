from django.shortcuts import render
from courses.models import CourseInfo
from operations.models import UsreLoverInfo,UserCourseInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate
from helptools.decorators import login_decorator
from django.db.models import Q
# Create your views here.
def course_list(request):
    all_course = CourseInfo.objects.all()
    rec_course = CourseInfo.objects.order_by('-love_num')[:2]

    keywords = request.GET.get('keywords', '')
    if keywords:
        all_course = CourseInfo.objects.filter(
            Q(name__icontains=keywords) | Q(desc__contains=keywords) | Q(detail__contains=keywords))

    sort_type = request.GET.get('sort_type', '')
    if sort_type == 'hot':
        all_course = CourseInfo.objects.order_by('-click_num')
    if sort_type == 'students':
        all_course = CourseInfo.objects.order_by('-stunum')

    pa = Paginator(all_course, 2)
    pagenum = request.GET.get('pagenum', 1)
    try:
        pagelist = pa.page(pagenum)
    except PageNotAnInteger:
        pagelist = pa.page(1)
    except EmptyPage:
        pagelist = pa.page(pa.num_pages)

    return render(request, 'courses/course-list.html', {
        'all_course': all_course,
        'pagelist': pagelist,
        'sort_type': sort_type,
        'rec_course': rec_course,
        'keywords': keywords,
    })


def course_detail(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]

        course.click_num+=1
        course.save()
        rec_course = CourseInfo.objects.filter(name__icontains=course.name[:4])[:2]
        is_love = False
        is_love1 = False
        if request.user.is_authenticated():
            love = UsreLoverInfo.objects.filter(userid=request.user, love_type=1, love_id=course.orgid_id)
            love1 = UsreLoverInfo.objects.filter(userid=request.user, love_type=2, love_id=course_id)
            if love:
                is_love = love[0].love_status
            if love1:
                is_love1 = love1[0].love_status

        return render(request, 'courses/course-detail.html', {
            'course': course,
            'rec_course': rec_course,
            'is_love': is_love,
            'is_love1':is_love1,
        })

@login_decorator
def course_video(request,course_id):
    if course_id:
        course=CourseInfo.objects.filter(id=int(course_id))[0]
        usercourse=UserCourseInfo.objects.filter(userid=request.user,courseid_id=int(course_id))
        if not usercourse:
            a=UserCourseInfo()
            a.userid_id=request.user.id
            a.courseid_id=course_id
            a.save()

            course.stunum += 1
            course.save()
            # 课程的学习人数加1，那么这个课程所属机构学习人数就加1
            course.orgid.study_num += 1
            course.orgid.save()

        courseuser_list=UserCourseInfo.objects.filter(courseid_id=int(course_id))
        user_list=[user.userid_id for user in courseuser_list]
        usercourse_list=UserCourseInfo.objects.filter(userid_id__in=user_list)
        course_list=[course.courseid for course in usercourse_list]
        course_list=list(set(course_list))



        return render(request,'courses/course-video.html',{
            'course':course,
            'course_list':course_list,
        })


def course_comment(request,course_id):
    if course_id:
        course=CourseInfo.objects.filter(id=int(course_id))[0]

        courseuser_list = UserCourseInfo.objects.filter(courseid_id=int(course_id))
        user_list = [user.userid_id for user in courseuser_list]
        usercourse_list = UserCourseInfo.objects.filter(userid_id__in=user_list)
        course_list = [course.courseid for course in usercourse_list]
        course_list = list(set(course_list))

        return render(request, 'courses/course-comment.html', {
            'course': course,
            'course_list': course_list,
        })

