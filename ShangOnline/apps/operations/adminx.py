import xadmin


# Register your models here.
from operations.models import UserAskInfo, UsreLoverInfo, UserCourseInfo, UserMessage, UserCommentInfo


class UserAskInfoXadmin(object):
    list_display = ['name', 'phone', 'course', 'add_time']


class UsreLoverInfoXadmin(object):
    list_display = ['userid', 'love_id', 'love_type', 'love_status', 'add_time']


class UserCourseInfoXadmin(object):
    list_display = ['userid', 'courseid', 'add_time']


class UserMessageXadmin(object):
    list_display = ['userid', 'message', 'msg_status', 'add_time']


class UserCommentInfoXadmin(object):
    list_display = ['userid', 'courseid','comment_content' ,'add_time']


xadmin.site.register(UserAskInfo, UserAskInfoXadmin)
xadmin.site.register(UsreLoverInfo, UsreLoverInfoXadmin)
xadmin.site.register(UserCourseInfo, UserCourseInfoXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
xadmin.site.register(UserCommentInfo, UserCommentInfoXadmin)