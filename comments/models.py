from django.db import models
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_comments',verbose_name='评论用户')
    comment = models.TextField(null=False,blank=True,help_text='请输入你的评论',verbose_name='评论内容')

    # 这里让blog里面的文章和评论进行关联
    article = models.ForeignKey('blog.Article',on_delete=models.CASCADE,related_name='article_comments',verbose_name='关联文章')

    creat_at = models.DateTimeField(auto_now=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    is_article = models.BooleanField(default=False,verbose_name='是否有效')

    class Meta:
        db_table = 'comment'
        verbose_name = '用户评论'
        ordering = ['-creat_at']
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户{self.user}在{self.creat_at}创建了评论.状态:{self.is_article}'

    # 获得用户信息
    def get_user_info(self):
        return {
            'id':self.user.id,
            'username':self.user.username,
            'avtar':self.user.avtar.url
        }

