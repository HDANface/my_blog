from django.db import models
from django.conf import settings  # 导入settings
from datetime import datetime


class Media(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="用户")
    image = models.ImageField(blank=True,null=True,upload_to='images/%Y/%m/%d/',verbose_name="上传图片")
    video = models.FileField(blank=True,null=True,upload_to='video/%Y/%m/%d/',verbose_name="上传视频")

    title = models.CharField(blank=True,null=True,max_length=100,verbose_name="名称")
    description = models.TextField(blank=True,null=True,max_length=100,verbose_name="描述")
    create_date = models.DateTimeField(default=datetime.now,verbose_name="创建时间")


    class Meta:
        db_table = 'media'
        verbose_name = '媒体'        #接口添加修改页名称
        verbose_name_plural = '媒体' #后台标题名称
        ordering = ['-create_date'] #排序,按照创建时间进行排序


    def __str__(self):
        return f'{self.title}在{self.create_date}添加完成'