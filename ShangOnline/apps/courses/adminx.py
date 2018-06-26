import xadmin

# Register your models here.
from courses.models import CourseInfo, LessonInfo, VideoInfo, SourceInfo


class CourseInfoXadmin(object):
    list_display=['name','desc','detail','level','stunum','study_time','image','lesson_num','category','click_num','love_num','orgid','teacherid','add_time']
    style_fields = {'detail': 'ueditor'}


class LessonInfoXadmin(object):
    list_display=['name','courseid','add_time']



class VideoInfoXadmin(object):
    list_display=['name','study_time','url','lessonid','add_time']


class SourceInfoXadmin(object):
    list_display=['name','file_addr','courseid','add_time']\


xadmin.site.register(CourseInfo,CourseInfoXadmin)
xadmin.site.register(LessonInfo,LessonInfoXadmin)
xadmin.site.register(VideoInfo,VideoInfoXadmin)
xadmin.site.register(SourceInfo,SourceInfoXadmin)
