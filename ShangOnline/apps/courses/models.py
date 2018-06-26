from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.
from orgs.models import OrgInfo,TeacherInfo


class CourseInfo(models.Model):
    name=models.CharField(max_length=20,verbose_name='课程名称')
    desc=models.CharField(max_length=200,verbose_name='课程描述')
    detail=UEditorField(verbose_name='课程详情',width=700,height=400,toolbars='full',imagePath='ueditor/images/',filePath='ueditor/files/',upload_settings={'imageMaxSizing':1024000},default='')
    level=models.CharField(choices=(('初级','初级'),('中级','中级'),('高级','高级')),default='初级',max_length=5,verbose_name='课程难度')
    stunum=models.IntegerField(default=0,verbose_name='学习人数')
    study_time=models.IntegerField(default=0,verbose_name='学习时长')
    lesson_num=models.IntegerField(default=0,verbose_name='章节数')
    category=models.CharField(max_length=10,choices=(('前端','前端'),('后端','后端')),default='前端',verbose_name='课程类别')
    click_num=models.IntegerField(default=0,verbose_name='点击量')
    love_num=models.IntegerField(default=0,verbose_name='点赞数')
    image=models.ImageField(upload_to='course/%y/%m',verbose_name='课程图片',max_length=200,null=True,blank=True)
    orgid=models.ForeignKey(OrgInfo,verbose_name='所属机构')
    teacherid=models.ForeignKey(TeacherInfo,verbose_name='所属讲师')
    teacher_say=models.CharField(default='好好学习，一定能找到好工作',max_length=200,verbose_name='讲师告知')
    need_know=models.CharField(default='学这门课程要努力努力再努力',max_length=100,verbose_name='课程须知')
    is_banner = models.BooleanField(default=True, verbose_name="是否轮播")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class LessonInfo(models.Model):
    name=models.CharField(max_length=50,verbose_name='章节名称')
    courseid=models.ForeignKey(CourseInfo,verbose_name='所属课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name


class VideoInfo(models.Model):
    name=models.CharField(max_length=50,verbose_name='视频名称')
    study_time=models.IntegerField(default=0,verbose_name='视频时长')
    url=models.URLField(max_length=200,default='http://video.atguigu.com/ce182d3e92d24c08ada798ed75236efe/64240d5f98c849d7a48a701646314ef0-abb0a550e0a4e1bd89390a178f91a577-ld.mp4',verbose_name='视频链接')
    lessonid=models.ForeignKey(LessonInfo,verbose_name='所属章节')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name

class SourceInfo(models.Model):
    name=models.CharField(max_length=50,verbose_name='资源名称')
    file_addr=models.FileField(upload_to='source/%y/%m',verbose_name='资源地址',max_length=200)
    courseid=models.ForeignKey(CourseInfo,verbose_name='所属课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '资源信息'
        verbose_name_plural = verbose_name
