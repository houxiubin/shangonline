from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UsersProFile(AbstractUser):
    nike_name = models.CharField(max_length=18, verbose_name='用户昵称', default='')
    age = models.IntegerField(default=30, verbose_name='用户年龄')
    birthday = models.DateField(null=True, blank=True, verbose_name='用户生日')
    gender = models.CharField(max_length=5, choices=(('girl', '女'), ('man', '男')), default='girl', verbose_name='用户性别')
    address = models.CharField(max_length=50, verbose_name='用户地址')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='用户手机')
    image = models.ImageField(max_length=100, upload_to='users/%y/%m', null=True, blank=True, verbose_name='用户头像')
    is_start=models.BooleanField(default=False,verbose_name='是否激活')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.username

    def get_msg_cont(self):
        from operations.models import UserMessage
        msg_cont=UserMessage.objects.filter(userid=self.id,msg_status=True).count()
        return msg_cont

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name


class EmailVerify(models.Model):
    email=models.EmailField(max_length=50,verbose_name='邮箱')
    code=models.CharField(max_length=20,verbose_name='邮箱验证')
    send_type=models.CharField(choices=(('register','注册'),('forget','修改'),('changeemail','更改邮箱')),default='register',max_length=12,verbose_name='验证类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

class Banner(models.Model):
    image=models.ImageField(upload_to='banner/%y/%m',max_length=100,verbose_name='轮播图')
    url=models.URLField(max_length=100,verbose_name='链接地址',default='http://www.atguigu.com/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name
