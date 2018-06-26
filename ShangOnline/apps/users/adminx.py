import xadmin
from .models import UsersProFile,EmailVerify,Banner
from xadmin import views


# class UsersProFileXadmin(object):
#     list_display = ['username', 'nike_name', 'age', 'birthday', 'gender', 'address', 'phone', 'image', 'add_time']
#     search_fields = ['username', 'nike_name', 'phone']
#     list_filter = ['username', 'nike_name', 'phone']

#
class EmailVerifyXadmin(object):
    list_display=['email','code','send_type','add_time']
    search_fields=['email','code','send_type']
    list_filter=['send_type']
#
#
class BannerXadmin(object):
    list_display=['image','url','add_time']
    search_fields=['image','url']
    list_filter=['image','url']

class GlobaSiteSettiong(object):
    site_title='尚在线教育后台管理系统'
    site_footer='尚硅谷IT教育'
    menu_style='accordion'


# xadmin.site.register(UsersProFile,UsersProFileXadmin)
xadmin.site.register(EmailVerify,EmailVerifyXadmin)
xadmin.site.register(Banner,BannerXadmin)
xadmin.site.register(views.CommAdminView,GlobaSiteSettiong)