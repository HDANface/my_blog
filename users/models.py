from django.db import models
from django.contrib.auth.models import AbstractUser,models
from datetime import datetime

class User(AbstractUser):
    # 基础信息
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名称')
    email = models.EmailField(verbose_name='邮件')
    password = models.CharField(max_length=128, verbose_name='密码')
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, default='', verbose_name='头像')
    bio = models.TextField(max_length=500, default='', verbose_name='简介')

    # 社交信息
    github = models.URLField(default='https://github.com/', verbose_name='github链接')

    # 为避免冲突，需要指定 related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # 自定义 related_name
        blank=True,
        verbose_name='用户组'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # 自定义 related_name
        blank=True,
        verbose_name='用户权限'
    )

    # 日期相关
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='用户对账号更新操作时间')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


