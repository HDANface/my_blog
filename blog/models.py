from django.db import models
from users.models import User


class Article(models.Model):
    choice_status = {
        ('draft', '草稿'),
        ('published', '已发布'),
        ('private', '私密'),
        ('archive', '归档'),
    }

    # 基础模型
    title = models.CharField(null=False,max_length=100,verbose_name='文章名称')
    content = models.TextField(blank=True,max_length=3000,verbose_name='文章内容')
    create_author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='创作者')
    Cover = models.ImageField(null=True,blank=True,verbose_name='封面')
    status = models.CharField(choices=choice_status,max_length=10,default='draft',verbose_name='文章状态')

    # 时间相关
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_date = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    # 互动性
    likes = models.IntegerField(default=0,verbose_name='点赞数')
    comments = models.IntegerField(default=0,verbose_name='评论数')
    views = models.IntegerField(default=0,verbose_name='观看数')

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title

# 分类
class Category(models.Model):
    name = models.CharField(unique=True,max_length=100,verbose_name='分类名')
    description = models.TextField(max_length=200,verbose_name='对于这个分类的描述')
    create_date = models.DateTimeField(auto_now=True,verbose_name='创建这个标签的时间')

    class Meta:
        db_table = 'blog_category'


    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField(unique=True,max_length=100,verbose_name='标签的名称')
    create_date = models.DateTimeField(auto_now=True,verbose_name='标签创建的时间')

    class Meta:
        db_table = 'blog_tag'

    def __str__(self):
        return self.name