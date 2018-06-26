from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.

class CityInfo(models.Model):
    name=models.CharField(max_length=10,verbose_name='城市名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '城市信息'
        verbose_name_plural = verbose_name

class OrgInfo(models.Model):
    name=models.CharField(max_length=20,verbose_name='机构名称')
    image=models.ImageField(max_length=200,upload_to='org/%y/%m',verbose_name='机构图片')
    study_num=models.IntegerField(verbose_name='学习人数',default=0)
    flag=models.CharField(max_length=10,verbose_name='学校品牌',default='知名学校')
    address=models.CharField(max_length=50,verbose_name='机构地址')
    desc=models.CharField(max_length=200,verbose_name='机构描述')
    detail=UEditorField(verbose_name='机构详情',width=700,height=400,toolbars='full',imagePath='ueditor/images/',filePath='ueditor/files/',upload_settings={'imageMaxSizing':1024000},default='')
    category=models.CharField(choices=(('jg','机构'),('gx','高校'),('gr','个人')),max_length=5,null=True,blank=True,verbose_name='机构分类')
    click_num=models.IntegerField(default=0,verbose_name='点击量')
    course_num=models.IntegerField(default=0,verbose_name='课程数')
    love_num=models.IntegerField(default=0,verbose_name='点赞数')
    cityid=models.ForeignKey(CityInfo,verbose_name='所属城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机构信息'
        verbose_name_plural = verbose_name

class TeacherInfo(models.Model):
    name=models.CharField(max_length=20,verbose_name='讲师姓名')
    age=models.IntegerField(verbose_name='年龄')
    image=models.ImageField(upload_to='teacher/%y/%m',max_length=200,verbose_name='讲师头像',null=True,blank=True)
    work_year=models.IntegerField(verbose_name='工作年限')
    work_company=models.CharField(max_length=20,null=True,blank=True,verbose_name='就职公司')
    work_position=models.CharField(max_length=20,null=True,blank=True,verbose_name='工作职位')
    work_style=models.CharField(max_length=10,null=True,blank=True,verbose_name='教学特点')
    click_num=models.IntegerField(default=0,verbose_name='点击量')
    love_num=models.IntegerField(default=0,verbose_name='点赞量')
    orgid=models.ForeignKey(OrgInfo,verbose_name='所属机构')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '讲师信息'
        verbose_name_plural = verbose_name
