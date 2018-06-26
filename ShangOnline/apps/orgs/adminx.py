import xadmin

# Register your models here.
from orgs.models import CityInfo, OrgInfo, TeacherInfo

class CityInfoXadmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name']
    list_filter = ['name']


class OrgInfoXadmin(object):
    list_display = ['name', 'image', 'study_num', 'address', 'desc', 'detail','category', 'click_num', 'love_num', 'cityid',
                    'add_time']
    search_fields = ['name', 'address', 'cityid','category']
    list_filter = ['name', 'address', 'cityid','category']
    style_fields={'detail':'ueditor'}


class TeacherInfoXadmin(object):
    list_display = ['name', 'age', 'image', 'work_year', 'work_company', 'work_position', 'work_style', 'click_num',
                    'love_num', 'orgid', 'add_time']
    search_fields = ['name', 'orgid']
    list_filter = ['name', 'orgid']


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
