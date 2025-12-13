from django.db import models

class Tools(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name='软件名称')
