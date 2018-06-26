from django.shortcuts import render
from orgs.models import OrgInfo, CityInfo, TeacherInfo
from operations.models import UsreLoverInfo, UserCourseInfo
from courses.models import CourseInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate
from django.db.models import Q


# Create your views here.
def org_list(request):
    all_org = OrgInfo.objects.all()
    citys = CityInfo.objects.all()

    keywords = request.GET.get('keywords', '')
    if keywords:
        all_org = all_org.filter(
            Q(name__icontains=keywords) | Q(desc__contains=keywords) | Q(detail__contains=keywords))

    cityid = request.GET.get('cityid', '')
    if cityid:
        all_org = all_org.filter(cityid_id=int(cityid))

    category = request.GET.get('category', '')
    if category:
        all_org = all_org.filter(category=category)

    if category and cityid:
        all_org = all_org.filter(category=category, cityid_id=int(cityid))

    sort = request.GET.get('sort', '')
    if sort == 'study_num':
        all_org = all_org.order_by('-study_num')
    elif sort == 'course':
        all_org = all_org.order_by('-course_num')

    else:
        all_org = all_org.order_by('-add_time')

    click_sort = all_org.order_by('-click_num')

    pagenum = request.GET.get('pagenum', 1)
    pa = Paginator(all_org, 3)

    try:
        page_list = pa.page(pagenum)

    except PageNotAnInteger:
        page_list = pa.page(1)

    except EmptyPage:

        page_list = pa.page(pa.num_pages)

    return render(request, 'org/org_list.html', {
        'all_org': all_org,
        'page_list': page_list,
        'citys': citys,
        'cityid': cityid,
        'category': category,
        'sort': sort,
        'click_sort': click_sort,
        'keywords': keywords,
    })


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        org.click_num += 1
        org.save()
        is_love = False
        if request.user.is_authenticated():
            love = UsreLoverInfo.objects.filter(userid=request.user, love_type=1, love_id=int(org_id))
            if love:
                is_love = love[0].love_status
            else:
                pass

        return render(request, 'org/org_detail_homepage.html', {
            'org': org,
            'org_type': 'home',
            'is_love': is_love
        })


def org_detail_course(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        is_love = False
        if request.user.is_authenticated():
            love = UsreLoverInfo.objects.filter(userid=request.user, love_type=1, love_id=int(org_id))
            if love:
                is_love = love[0].love_status
            else:
                pass
        return render(request, 'org/org-detail-course.html', {
            'org': org,
            'org_type': 'course',
            'is_love': is_love
        })


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        is_love = False
        if request.user.is_authenticated():
            love = UsreLoverInfo.objects.filter(userid=request.user, love_type=1, love_id=int(org_id))
            if love:
                is_love = love[0].love_status
            else:
                pass
        return render(request, 'org/org-detail-desc.html', {
            'org': org,
            'org_type': 'desc',
            'is_love': is_love
        })


def org_detail_teacher(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        is_love = False
        if request.user.is_authenticated():
            love = UsreLoverInfo.objects.filter(userid=request.user, love_type=1, love_id=int(org_id))
            if love:
                is_love = love[0].love_status
            else:
                pass
        return render(request, 'org/org-detail-teachers.html', {
            'org': org,
            'org_type': 'teacher',
            'is_love': is_love
        })


def teacher_list(request):
    all_teacher = TeacherInfo.objects.all()

    keywords = request.GET.get('keywords', '')
    if keywords:
        all_teacher = TeacherInfo.objects.filter(name__icontains=keywords)

    sort_type = request.GET.get('sort', '')
    if sort_type == 'hot':
        all_teacher = TeacherInfo.objects.order_by('-love_num')

    rec_teacher = TeacherInfo.objects.order_by('-click_num')[:3]
    pa = Paginator(all_teacher, 3)
    pagenum = request.GET.get('pagenum')

    try:
        page_list = pa.page(pagenum)
    except PageNotAnInteger:
        page_list = pa.page(1)
    except EmptyPage:
        page_list = pa.page(pa.num_pages)

    return render(request, 'org/teachers-list.html', {
        'all_teacher': all_teacher,
        'page_list': page_list,
        'sort_type': sort_type,
        'rec_teacher': rec_teacher,
        'keywords': keywords,
    })


def teacher_detail(request, teacher_id):
    if teacher_id:
        teacher = TeacherInfo.objects.filter(id=int(teacher_id))[0]

        teacher.click_num+=1
        teacher.save()

        rec_teacher = TeacherInfo.objects.order_by('-click_num')[:3]

        is_love = False
        is_love1 = False
        if request.user.is_authenticated():
            love = UsreLoverInfo.objects.filter(userid=request.user, love_id=teacher.orgid.id, love_type=1)
            love1 = UsreLoverInfo.objects.filter(userid=request.user, love_id=teacher.id, love_type=3)
            if love:
                is_love = love[0].love_status
            if love1:
                is_love1 = love1[0].love_status

        return render(request, 'org/teacher-detail.html', {
            'teacher': teacher,
            'rec_teacher': rec_teacher,
            'is_love': is_love,
            'is_love1': is_love1,
        })
