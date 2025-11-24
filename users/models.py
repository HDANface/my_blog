from django.db import models
from django.contrib.auth.models import User,AbstractUser
from datetime import datetime


class User(AbstractUser):

    # 基础信息
    username = models.CharField(max_length=10, unique=True,verbose_name='用户名称')
    email = models.EmailField(verbose_name='邮件')
    password = models.CharField(max_length=128,verbose_name='密码')
    avatar = models.ImageField(upload_to='avatar/',null=True,blank=True,default='',verbose_name='头像')
    bio = models.TextField(max_length=500,default='简介',verbose_name='简介')

    #社交信息
    github = models.URLField(default='https://github.com/',verbose_name='github链接')

    #日期相关
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='用户创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='用户对账号更新操作时间')

    def str(self):
        return self.username

    class Meta:
        db_table = 'user'


